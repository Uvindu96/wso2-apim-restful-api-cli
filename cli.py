import requests
import json
import base64

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

clientData = None
viewAccessToken = None
createAccessToken = None
publishAccessToken = None
allApis = None

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


def generateAccessToken(clientId, clientSecret, scope):
    url = "https://localhost:8243/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(str(clientId + ":" + clientSecret).encode()).decode("utf-8")
    }
    params = {
        "grant_type": "password",
        "username": "admin",
        "password": "admin",
        "scope": scope
    }
    response = requests.post(url, headers=headers, params=params, verify=False)
    return response.json()['access_token']


def getAllApis(viewAccessToken):
    url = "https://localhost:9443/api/am/publisher/v0.14/apis"
    headers = {
        "Authorization": 'Bearer %s'%viewAccessToken,
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


def start():
    global clientData
    global viewAccessToken
    global createAccessToken
    global publishAccessToken
    global allApis
    clientData = registerClient()
    viewAccessToken = generateAccessToken(clientData['clientId'], clientData['clientSecret'], 'apim:api_view')
    createAccessToken = generateAccessToken(clientData['clientId'], clientData['clientSecret'], 'apim:api_create')
    publishAccessToken = generateAccessToken(clientData['clientId'], clientData['clientSecret'], 'apim:api_publish')
    allApis = getAllApis(viewAccessToken)


def printTokens():
    print("View Access Token: ", viewAccessToken)
    print("Create Access Token: ", createAccessToken)
    print("Publish Access Token: ", publishAccessToken)


def printApis():
    for api in allApis["list"]:
        print(api)


while True:
    command = input("execute: ")
    if command == "exit":
        print("shutting down executor...")
        print()
        break
    elif command == "start":
        start()
        print("Client registration is successful")
        print()
    elif command == "print tokens":
        printTokens()
        print()
    elif command == "print apis":
        printApis()
        print()