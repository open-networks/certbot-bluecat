'''Certbot BlueCat plugin.'''

# extern libs
import time
from certbot.plugins import dns_common
import logging
from dns import resolver

from .bluecat import Bluecat
from . import constants


# Logging
logger = logging.getLogger(__name__)
logger.info(('logger initialized: {0}').format(__name__))


class BluecatAuthenticator(dns_common.DNSAuthenticator):
    '''Base class for DNS Authenticators'''

    description = 'Bluecat Authenticator Plugin'

    def __init__(self, *args, **kwargs):
        '''Initialize an BlueCat Configurator'''
        super(BluecatAuthenticator, self).__init__(*args, **kwargs)

    @classmethod
    def add_parser_arguments(cls, add):
        # parameter from constants.py
        add('api', metavar='API', default=constants.CLI_DEFAULTS['bluecat_api'],
            help='FQDN of the Bluecat Address Manager')
        add('username', metavar='USERNAME', default=constants.CLI_DEFAULTS['bluecat_username'],
            help='Bluecat API Username')
        add('password', metavar='PASSWORD', default=constants.CLI_DEFAULTS['bluecat_password'],
            help='Bluecat API Password')
        add('viewid', metavar='viewid', default=constants.CLI_DEFAULTS['bluecat_viewid'],
            help='entityId of the DNS View from Bluecat API')
        # delay after deploying txt record. this differs from the dns default variable propagation-seconds
        # as its continously trying to check if the deployment has been executed and asap returns
        add('propagation-seconds', default=60, type=int,
            help='Time waiting for DNS to propagate before asking the ACME server')
        add('verify-ssl', default=False, type=bool,
            help="enable or disable SSL verification of the API")

    # Initialize bluecat object and get session token from bluecat API
    def prepare(self):
        '''Prepare the authenticator/installer'''

        # TODO: Error Handling
        # viewid exists?

        # Initialize Bluecat Object
        self.bluecat = Bluecat(self.conf('api'), self.conf('username'), self.conf('password'), self.conf('viewid'), self.conf('verify-ssl'))

        # Get RestAPI Session Token from Bluecat
        self.bluecat.get_token()
        logger.info(f'prepared: {self.bluecat}')

    # Add TXT-Record in Bluecat Adress Manager
    def _perform(self, domain, validation_domain_name, validation):
        '''
        Performs a dns-01 challenge by creating a DNS TXT record.
        :param str domain: The domain being validated.
        :param str validation_domain_name: The validation record domain name.
        :param str validation: The validation record content.
        :raises errors.PluginError: If the challenge cannot be performed
        '''

        logger.info('_perform: adding txt record to bluecat')
        logger.info(f'  domain: {domain}')
        logger.info(f'  validation_domain_name: {validation_domain_name}')
        logger.info(f'  validation: {validation}')

        # add_txt_record
        logger.info('add_txt_record')
        self.objectId = self.bluecat.add_txt_record(domain, validation_domain_name, validation)

        # quickdeploy
        logger.info('quickdeploy')
        code = self.bluecat.quickdeploy()

    # cleanup/delete txt record after validation
    def _cleanup(self, domain, validation_domain_name, validation):
        self.bluecat.delete_txt_record()
        logger.info('_clean: cleaning done')

    # mandatory methods - just ignore
    def more_info(self):
        logger.info('more_info: just info')

    def _setup_credentials(self):
        logger.info('_setup_credentials: just info')
