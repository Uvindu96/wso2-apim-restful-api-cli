import requests
import json
import base64

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

clientData = None
viewAccessToken = None
createAccessToken = None
publishAccessToken = None


# return json
def registerClient():
    url = "https://localhost:9443/client-registration/v0.14/register"
    headers = {
        "Authorization": "Basic YWRtaW46YWRtaW4=",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "callbackUrl": "www.google.lk",
        "clientName": "rest_api_publisher",
        "owner": "admin",
        "grantType": "password refresh_token",
        "saasApp": True
    })
    response = requests.post(url, headers=headers, data=payload, verify=False)
    global clientData
    clientData = response
    return response.json()


# return json
def generateAccessToken(scope):
    url = "https://localhost:8243/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(str(clientData['clientId'] + ":" + clientData['clientSecret']).encode()).decode("utf-8")
    }
    params = {
        "grant_type": "password",
        "username": "admin",
        "password": "admin",
        "scope": scope
    }
    response = requests.post(url, headers=headers, params=params, verify=False)
    global viewAccessToken
    global createAccessToken
    global publishAccessToken
    if scope == 'apim:api_view':
        viewAccessToken = response.json()['access_token']
    elif scope == 'apim:api_create':
        createAccessToken = response.json()['access_token']
    elif scope == 'apim:api_publish':
        publishAccessToken = response.json()['access_token']
    return response.json()


# return json
def viewApis():
    url = "https://localhost:9443/api/am/publisher/v0.14/apis"
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "If-None-Match": ""
    }
    params = {
        "limit": 25,
        "offset": 0
    }
    response = requests.get(url, headers=headers, params=params, verify=False)
    return response.json()


# return json
def createApi():
    name = input("\tName: ")
    context = input("\tContext: ")

    url = "https://localhost:9443/api/am/publisher/v0.14/apis"
    headers = {
        "Authorization": "Bearer %s" % createAccessToken,
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "name": name,
        "description": "This document describe a RESTFul API for AWS Lambda function invocations.\r\n",
        "context": "/%s" % context,
        "version": "1.0.0",
        "provider": "admin",
        "apiDefinition":  "{\"paths\":{\"/order\":{\"post\":{\"amznResourceName\":\"arn:aws:lambda:us-east-2:572100981605:function:random-number-generator\",\"x-auth-type\":\"Application & Application User\",\"x-throttling-tier\":\"Unlimited\",\"description\":\"Create a new Order\",\"parameters\":[{\"schema\":{\"$ref\":\"#/definitions/Order\"},\"description\":\"Order object that needs to be added\",\"name\":\"body\",\"required\":true,\"in\":\"body\"}],\"responses\":{\"201\":{\"headers\":{\"Location\":{\"description\":\"The URL of the newly created resource.\",\"type\":\"string\"}},\"schema\":{\"$ref\":\"#/definitions/Order\"},\"description\":\"Created.\"}}}},\"/menu\":{\"get\":{\"x-auth-type\":\"Application & Application User\",\"x-throttling-tier\":\"Unlimited\",\"description\":\"Return a list of available menu items\",\"parameters\":[],\"responses\":{\"200\":{\"headers\":{},\"schema\":{\"title\":\"Menu\",\"properties\":{\"list\":{\"items\":{\"$ref\":\"#/definitions/MenuItem\"},\"type\":\"array\"}},\"type\":\"object\"},\"description\":\"OK.\"}}}}},\"schemes\":[\"https\"],\"produces\":[\"application/json\"],\"swagger\":\"2.0\",\"definitions\":{\"MenuItem\":{\"title\":\"Pizza menu Item\",\"properties\":{\"price\":{\"type\":\"string\"},\"description\":{\"type\":\"string\"},\"name\":{\"type\":\"string\"},\"image\":{\"type\":\"string\"}},\"required\":[\"name\"]},\"Order\":{\"title\":\"Pizza Order\",\"properties\":{\"customerName\":{\"type\":\"string\"},\"delivered\":{\"type\":\"boolean\"},\"address\":{\"type\":\"string\"},\"pizzaType\":{\"type\":\"string\"},\"creditCardNumber\":{\"type\":\"string\"},\"quantity\":{\"type\":\"number\"},\"orderId\":{\"type\":\"string\"}},\"required\":[\"orderId\"]}},\"consumes\":[\"application/json\"],\"info\":{\"title\":\"PizzaShackAPI\",\"description\":\"This document describe a RESTFul API for Pizza Shack online pizza delivery store.\\n\",\"license\":{\"name\":\"Apache 2.0\",\"url\":\"http://www.apache.org/licenses/LICENSE-2.0.html\"},\"contact\":{\"email\":\"architecture@pizzashack.com\",\"name\":\"John Doe\",\"url\":\"http://www.pizzashack.com\"},\"version\":\"1.0.0\"}}",
        "wsdlUri": None,
        "status": "CREATED",
        "responseCaching": "Disabled",
        "cacheTimeout": 300,
        "destinationStatsEnabled": False,
        "isDefaultVersion": False,
        "type": "HTTP",
        "transport":    [
          "http",
          "https"
        ],
        "tags": ["pizza"],
        "tiers": ["Unlimited"],
        "maxTps":    {
          "sandbox": 5000,
          "production": 1000
        },
        "visibility": "PUBLIC",
        "visibleRoles": [],
        "endpointConfig": "{\"endpoint_type\":\"awslambda\",\"amznAccessKey\":\"AKIAYKM7AGNSTGM76FNK\",\"amznSecretKey\":\"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\"}",
        "endpointSecurity":    {
          "username": "user",
          "type": "basic",
          "password": "pass"
        },
        "gatewayEnvironments": "Production and Sandbox",
        "sequences": [{"name":"json_validator","type": "in"},{"name":"log_out_message","type": "out"}],
        "subscriptionAvailability": None,
        "subscriptionAvailableTenants": [],
        "businessInformation":    {
          "businessOwnerEmail": "marketing@pizzashack.com",
          "technicalOwnerEmail": "architecture@pizzashack.com",
          "technicalOwner": "John Doe",
          "businessOwner": "Jane Roe"
        },
        "corsConfiguration":    {
          "accessControlAllowOrigins": ["*"],
          "accessControlAllowHeaders":       [
             "authorization",
             "Access-Control-Allow-Origin",
             "Content-Type",
             "SOAPAction"
          ],
          "accessControlAllowMethods":       [
             "GET",
             "PUT",
             "POST",
             "DELETE",
             "PATCH",
             "OPTIONS"
          ],
          "accessControlAllowCredentials": False,
          "corsConfigurationEnabled": False
       }
    })
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()


# return json
def viewApi(apiId):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis/%s" % apiId
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken
    }
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


# return json
def deleteApi(apiId):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis/%s" % apiId
    headers = {
        "Authorization": "Bearer %s" % createAccessToken
    }
    response = requests.delete(url, headers=headers, verify=False)
    return response.json()


# return json
def publishApi(apiId):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis/change-lifecycle"
    headers = {
        "Authorization": "Bearer %s" % publishAccessToken
    }
    params = {
        "apiId": apiId,
        "action": "Publish"
    }
    response = requests.post(url, headers=headers, params=params, verify=False)
    return response.json()


# return json
def viewSwaggerApi(apiId):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis/%s/swagger" % apiId
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken
    }
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


