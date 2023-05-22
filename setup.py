import os

from setuptools import setup
from setuptools import find_packages

if os.environ.get('GITHUB_RELEASE_TAG'):
    version = os.environ['GITHUB_RELEASE_TAG']
elif os.environ.get('CI_JOB_ID'):
    version = os.environ['CI_JOB_ID']
else:
    try:
        with open('PKG-INFO') as f:
            for line in f:
                if line.startswith('Version: '):
                    version = line.split('Version: ')[1].split('\n')[0]
                    break
    except IOError:
        version = 'unkown version'

with open('README.md', 'r') as fh:
    long_description = fh.read()

install_requires = [
    'acme',
    'certbot',
    'setuptools>=1.0',
    'dnspython',
]
DISTNAME = 'certbot-bluecat'

setup(
    name='certbot-bluecat',
    version=version,
    description='Bluecat plugin for Certbot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Certbot Team @ Open Networks',
    author_email='certbot@on.at',
    license='Apache License 2.0',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={},
    entry_points={
        'certbot.plugins': [
            'bluecat = certbot_bluecat.authenticator:BluecatAuthenticator',
        ],
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='certbot_bluecat',
)
