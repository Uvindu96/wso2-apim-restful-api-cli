import requests
import json
import base64


requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


# Introduction


host = "https://localhost:9443"
basePath = "/api/am/publisher/v0.14"


# Getting started


def registerClient():
    url = host + "/client-registration/v0.14/register"
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
    return response


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
    return response


# API (Collection)


def viewApis(viewAccessToken):
    url = host + basePath + "/apis"
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
    return response


# API (Individual)


def deleteApi(createAccessToken, apiId):
    url = host + basePath + "/apis/%s" % apiId
    headers = {
        "Authorization": "Bearer %s" % createAccessToken
    }
    response = requests.delete(url, headers=headers, verify=False)
    return response


def viewApi(viewAccessToken, apiId):
    url = host + basePath + "/apis/%s" % apiId
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken
    }
    response = requests.get(url, headers=headers, verify=False)
    return response


def updateApi(createAccessToken, apiId, jsonFileName):
    url = host + basePath + "/apis/%s" % apiId
    headers = {
        "Authorization": "Bearer %s" % createAccessToken,
        "Content-Type": "application/json"
    }
    try:
        with open(jsonFileName) as jsonFile:
            payload = json.dumps(json.load(jsonFile))
    except:
        payload = "{}"
    response = requests.put(url, headers=headers, data=payload, verify=False)
    return response


def viewResourcePolicyDefinitions(viewAccessToken, apiId):
    url = host + basePath + "/apis/%s/resource-policies" % apiId
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken
    }
    response = requests.get(url, headers=headers, verify=False)
    return response


def viewResourcePolicyDefinition(viewAccessToken, apiId, resourceId):
    url = host + basePath + "/apis/%s/resource-policies/%s" % apiId, resourceId
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken
    }
    response = requests.get(url, headers=headers, verify=False)
    return response


def updateResourcePolicyDefinition(createAccessToken, apiId, resourceId, resourcePolicyDefinitionFileName):
    url = host + basePath + "/apis/%s/resource-policies/%s" % apiId, resourceId
    headers = {
        "Authorization": "Bearer %s" % createAccessToken
    }
    try:
        with open(resourcePolicyDefinitionFileName, "r") as resourcePolicyDefinitionFile:
            files = {"apiDefinition": resourcePolicyDefinitionFile.read()}
    except:
        files = {}
    response = requests.put(url, headers=headers, files=files, verify=False)
    return response


def viewSwaggerDefinition(viewAccessToken, apiId):
    url = host + basePath + "/apis/%s/swagger" % apiId
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken
    }
    response = requests.get(url, headers=headers, verify=False)
    return response


def updateSwaggerDefinition(createAccessToken, apiId, swaggerDefinitionFileName):
    url = host + basePath + "/apis/%s/swagger" % apiId
    headers = {
        "Authorization": "Bearer %s" % createAccessToken
    }
    try:
        with open(swaggerDefinitionFileName, "r") as swaggerDefinitionFile:
            files = {"apiDefinition": swaggerDefinitionFile.read()}
    except:
        files = {}
    response = requests.put(url, headers=headers, files=files, verify=False)
    return response


def downloadThumbnailImage(viewAccessToken, apiId):
    url = host + basePath + "/apis/%s/thumbnail" % apiId
    headers = {
        "Authorization": "Bearer %s" % viewAccessToken
    }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        with open("thumbnail.jpg", 'wb') as imgFile:
            imgFile.write(response.content)
    return response


def uploadThumbnailImage(createAccessToken, apiId, imgFileName):
    url = host + basePath + "/apis/%s/thumbnail" % apiId
    headers = {
        "Authorization": "Bearer %s" % createAccessToken
    }
    try:
        files = {"file": open(imgFileName, "rb")}
    except:
        files = {}
    response = requests.post(url, headers=headers, files=files, verify=False)
    return response


def changeApiStatus(publishAccessToken, apiId, action):
    url = host + basePath + "/apis/change-lifecycle"
    headers = {
        "Authorization": "Bearer %s" % publishAccessToken
    }
    params = {
        "apiId": apiId,
        "action": action
    }
    response = requests.post(url, headers=headers, params=params, verify=False)
    return response


def createApiVersion(createAccessToken, apiId, newVersion):
    url = host + basePath + "/apis/copy-api"
    headers = {
        "Authorization": "Bearer %s" % createAccessToken,
        "Content-Type": "application/json"
    }
    params = {
        "apiId": apiId,
        "newVersion": newVersion
    }
    response = requests.post(url, headers=headers, params=params, verify=False)
    return response


def createApi(createAccessToken, jsonFileName):
    url = host + basePath + "/apis"
    headers = {
        "Authorization": "Bearer %s" % createAccessToken,
        "Content-Type": "application/json"
    }
    try:
        with open(jsonFileName) as jsonFile:
            payload = json.dumps(json.load(jsonFile))
    except:
        payload = "{}"
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response


# Application (Individual)
