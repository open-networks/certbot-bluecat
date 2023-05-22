# certbot-bluecat-plugin

This certbot plugin authenticates the certbots certificate sign request by deploying a TXT entry in a bluecat DNS server.

## Requirements

see certbot rquirements: <https://certbot.eff.org/docs/install.html#system-requirements>

## Install

`pip install certbot-bluecat`

by installing the plugin you will also install all missing dependencies including certbot.

## Supported Features

* verifies the domain via DNS01 challenge
* adds the TXT record and triggers a quick deploy
* supports the Legacy v1 API

## Usage

```bash
/opt/certbot # certbot plugins --help bluecat
bluecat:
  Bluecat Authenticator Plugin

  --bluecat-api API     FQDN + Path to REST API (default: http://proteus.example.com/Services/REST/v1/)
  --bluecat-username USERNAME
                        Bluecat API Username (default: admin)
  --bluecat-password PASSWORD
                        Bluecat API Password (default: admin)
  --bluecat-viewid viewid
                        entityId of the DNS View from Bluecat API (default: 10)
  --bluecat-propagation-timeout BLUECAT_PROPAGATION_TIMEOUT
                        Time waiting for DNS to propagate before asking the ACME server (default: 300)
  --bluecat-verify-ssl BLUECAT_VERIFY_SSL
                        enable or disable SSL verification of the API (default: False)
```

Example:

```bash
certbot certonly --non-interactive --expand --email 'admin@example.com' --agree-tos \
  -a bluecat
  -v --staging
  --bluecat-api http://bluecat.example.com/Services/REST/v1/
  --bluecat-username admin
  --bluecat-password admin
  --bluecat-viewid 10
  -d example.com
```

## Testing

> :warning: Currently only integration tests are supported. Therefore a BlueCat is needed.

### Prerequisites

1. Connection to the bluecat under test from the machine running the tests
2. Configure the tests using the following environment variables:

| ENV                    | default   | Example                                                      |
| ---------------------- | --------- | ------------------------------------------------------------ |
| BLUECAT_EMAIL          |           | <test@test.test>                                             |
| BLUECAT_API            |           | <http://proteus.example.com/Services/REST/v1/>               |
| BLUECAT_USERNAME       |           | user                                                         |
| BLUECAT_PASSWORD       |           | secret                                                       |
| BLUECAT_VIEWID         |           | 10                                                           |
| BLUECAT_DOMAIN         |           | example.com                                                  |

## Contribute

If you find errors please open a new issue.

Open a pull request if you have made changes you want to add. we will take a look at it and try our best to merge it. Your help is very welcomed.
