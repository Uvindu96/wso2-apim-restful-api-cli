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
def viewApis():
    url = "https://localhost:9443/api/am/store/v0.14/apis"
    response = requests.get(url, verify=False)
    return response.json()


# return json
def viewApi(apiId):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis/%s" % apiId
    response = requests.get(url, verify=False)
    return response.json()