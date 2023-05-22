'''Module contains classes used by the BlueCat Configurator.'''
import logging
import re
import requests

from urllib3.exceptions import InsecureRequestWarning

# Logging
from certbot import errors

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

logger = logging.getLogger(__name__)
logger.info(f'logger initialized: {__name__}')


class Bluecat(object):
    ''' Object representing a Bluecat API '''

    def __init__(self, api, username, password, viewId, verify_ssl):
        self.api = api
        self.username = username
        self.password = password
        self.viewId = viewId
        self.verify_ssl = verify_ssl
        # vars which will be defined while processing
        self.token = None
        self.record_name = None
        self.zone_id = None

    def __str__(self):
        return f'api: {self.api}'

    def get_token(self):
        '''login and fetch a token'''

        url = f'{self.api}/Services/REST/v1/login?username={self.username}&password={self.password}'
        res = requests.get(url, verify=self.verify_ssl)
        self.token = re.search('(BAMAuthToken: \S*)', res.text).group(0)
        return res.status_code

    def get_record_name_and_zone_id(self, domain):
        '''get record_name and zone_id
        identify viewID manually by api call like
        searchByObjectTypes?types=View&keyword=ong&count=10 or getParent?entityId=...
        '''

        domain_list = domain.split('.')
        parentId = str(self.viewId)

        zone = ''
        for d in reversed(domain_list):
            url = (f'{self.api}/Services/REST/v1/getEntityByName?parentId={parentId}&name={d}&type=Zone')
            res = requests.get(url, headers={'Authorization': self.token}, verify=self.verify_ssl)
            assert res.status_code < 300
            output = res.json()

            if output['type'] == 'Zone':
                zone = '.' + output['name'] + zone
            else:
                record_name = domain.replace(zone, '')
                self.record_name = record_name
                self.zone_id = parentId
                return res.status_code

            parentId = str(output['id'])

        res.raise_for_status()

    def add_txt_record(self, domain, validation_domain_name, validation):
        '''add txt record to dns zone'''

        self.get_record_name_and_zone_id(validation_domain_name)
        self.delete_txt_record_by_name()

        url = self.api + '/Services/REST/v1/addEntity?parentId=' + self.zone_id
        header = {'Authorization': self.token}
        header['Content-Type'] = 'application/json'

        body = {
            "name": f"{self.record_name}",
            "type": "TXTRecord",
            "properties": f"ttl=60|absoluteName={validation_domain_name}|txt={validation}|"
        }

        res = requests.post(url, headers=header, json=body, verify=self.verify_ssl)

        self.objectId = str(res.text)
        res.raise_for_status()

    def quickdeploy(self):
        '''run a quick deploy to push changes to dns server'''

        logger.info('deploying dns record')
        url = f'{self.api}/Services/REST/v1/quickDeploy?entityId={self.zone_id}'
        res = requests.post(url, headers={'Authorization': self.token}, verify=self.verify_ssl)
        if res.status_code != 200:
            message = f'The quick deployment failed with code:{res.status_code}. The Response content was {res.content}'
            raise errors.PluginError(message)
        res.raise_for_status()

    def delete_txt_record(self):
        '''cleanup created txt record'''

        url = f'{self.api}/Services/REST/v1/delete?objectId={self.objectId}'
        res = requests.delete(url, headers={'Authorization': self.token}, verify=self.verify_ssl)
        res.raise_for_status()

    def delete_txt_record_by_name(self):
        '''delete txt record if exists, to avoid duplicate entries'''

        url = f'{self.api}/Services/REST/v1/getEntityByName?parentId={self.zone_id}&name={self.record_name}&type=TXTRecord'
        res = requests.get(url, headers={'Authorization': self.token}, verify=self.verify_ssl)
        if res.json()['id'] > 0:
            self.objectId = str(res.json()['id'])
            self.delete_txt_record()
