import requests
import json
import base64

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


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
    return response.json()


# return json
def generateAccessToken(clientData, scope):
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
    return response.json()


# return json
def viewApis(viewAccessToken):
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
def createApi(createAccessToken):
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
        "apiDefinition":  "{\"paths\":{\"/get-random-num\":{\"post\":{\"amznResourceName\":\"arn:aws:lambda:us-east-2:572100981605:function:random-number-generator\",\"x-auth-type\":\"Application & Application User\",\"x-throttling-tier\":\"Unlimited\",\"description\":\"Get a random number\",\"parameters\":[{\"schema\":{\"type\":\"object\",\"properties\":{\"payload\":{\"min\":\"\", \"max\":\"\"}}},\"description\":\"Define min and max\",\"name\":\"body\",\"required\":true,\"in\":\"body\"}],\"responses\":{\"200\":{\"description\":\"Generated.\"}}}}, \"/get-rand-num\":{\"post\":{\"amznResourceName\":\"arn:aws:lambda:us-east-2:572100981605:function:random-number-generator\",\"x-auth-type\":\"Application & Application User\",\"x-throttling-tier\":\"Unlimited\",\"description\":\"Get a random number\",\"parameters\":[{\"schema\":{\"type\":\"object\",\"properties\":{\"payload\":{\"min\":\"\", \"max\":\"\"}}},\"description\":\"Define min and max\",\"name\":\"body\",\"required\":true,\"in\":\"body\"}],\"responses\":{\"200\":{\"description\":\"Generated.\"}}}}},\"swagger\":\"2.0\",\"info\":{\"title\":\"PizzaShackAPI2\",\"version\":\"1.0.0\"}}",
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
def viewApi(viewAccessToken, apiId):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis/%s" % apiId
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken
    }
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


# return json
def deleteApi(createAccessToken, apiId):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis/%s" % apiId
    headers = {
        "Authorization": "Bearer %s" % createAccessToken
    }
    response = requests.delete(url, headers=headers, verify=False)
    return response.json()


# return response code
def publishApi(publishAccessToken, apiId):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis/change-lifecycle"
    headers = {
        "Authorization": "Bearer %s" % publishAccessToken
    }
    params = {
        "apiId": apiId,
        "action": "Publish"
    }
    response = requests.post(url, headers=headers, params=params, verify=False)
    return response


# return json
def viewSwaggerApi(viewAccessToken, apiId):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis/%s/swagger" % apiId
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken
    }
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


