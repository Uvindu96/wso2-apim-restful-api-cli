# wso2-apim-restful-api-cli
CLI to call RESTful API for WSO2 API Manager.

Make sure following packages are installed. Otherwise run these commands using pip.

`pip install json`
`pip install base64`
`pip install requests`

Run `python3 cli.py` in Terminal to start the CLI. Access tokens are auto-generated when CLI starts, hence you don't
have to worry about that. If you want to generate new access tokens just type `refresh` and press enter. To close the
CLI type `exit` and press enter.

## Publisher
#### API (Collection)
- `view apis`
#### API (Individual)
- `delete api @apiId`
- `view api @apiId`
- `update api @apiId`
- `view resource policies @apiId`
- `view resource policy @apiId`
- `update resource policy @apiId`
- `view swagger @apiId`
- `update swagger @apiId`
- `download thumbnail @apiId`
- `upload thumbnail @apiId`
- `change api status @apiId`
- `create api version @apiId`
- `create api`
#### Application (Individual)
#### Certificates (Collection)
#### Certificates (Individual)
#### ClientCertificates (Collection)
#### ClientCertificates (Individual)
#### Document (Collection)
#### Document (Individual)
#### Environment (Collection)
#### MediationPolicy (Collection)
#### MediationPolicy (Individual)
#### Subscription (Collection)
#### Subscription (Individual)
#### ThrottlingTier (Collection)
#### ThrottlingTier (Individual)
#### Workflows (Individual)
#### WSDL (Individual)
## Store
## Admin
