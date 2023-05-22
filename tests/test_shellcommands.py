'''
This test the deployment of several integration test
'''

import subprocess
import re
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

email = os.getenv("BLUECAT_EMAIL", "test@test.test")
user = os.getenv("BLUECAT_USERNAME")
password = os.getenv("BLUECAT_PASSWORD")
bluecat = os.getenv("BLUECAT_API")
viewid = os.getenv("BLUECAT_VIEWID")
domain = os.getenv("BLUECAT_DOMAIN")


def validate_certbot_certificate_delivery(stdout: str, stderr: str):
    # from https://www.regextester.com/96683
    regex_date = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
    regex_cert_expire_indicator = '(?<=certificate expires on )'
    regex_check_result = regex_cert_expire_indicator + regex_date
    match = re.search(regex_check_result, stdout)
    if match is not None:
        logger.info(f'New Certificate was created. Expiration Date:{match.group(1)}')
        return True
    else:
        logger.error(f'Certificate aquirement failed: \n stdout:\n{stdout}\n sterr:\n{stderr}')
        return False


def get_certbot_certificate(stdout: str, domain: str):
    file_path = f'/etc/letsencrypt/live/{domain}/cert.pem'

    with open(file_path, 'r') as cert_file:
        return cert_file.read()


def test_certbot_bluecat():
    response = subprocess.run(
        (
            'certbot'
            ' certonly'
            f' -d {domain}'
            ' -a bluecat'
            f' --bluecat-api \'{bluecat}\''
            f' --bluecat-username \'{user}\''
            f' --bluecat-password \'{password}\''
            f' --bluecat-viewid \'{viewid}\''
            ' --agree-tos'
            f' --email {email}'
            ' --no-eff-email'
            ' -v --staging'
            ' --debug'
            ' --force-renewal'
        ),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )

    # check if new certificate was created
    assert validate_certbot_certificate_delivery(
        response.stdout.decode('utf-8'), response.stderr.decode('utf-8')
    )
