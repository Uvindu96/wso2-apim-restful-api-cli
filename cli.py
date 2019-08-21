import publisher
import store
import json
import pyperclip


clientData = None
viewAccessToken = None
createAccessToken = None
publishAccessToken = None


def start():
    try:
        global clientData
        global viewAccessToken
        global createAccessToken
        global publishAccessToken
        clientData = publisher.registerClient().json()
        viewAccessToken = publisher.generateAccessToken(clientData, 'apim:api_view').json()['access_token']
        createAccessToken = publisher.generateAccessToken(clientData, 'apim:api_create').json()['access_token']
        publishAccessToken = publisher.generateAccessToken(clientData, 'apim:api_publish').json()['access_token']
        return "\033[1;34mClient registration is successful\033[0;37m"
    except:
        return "\033[1;31mClient registration is unsuccessful. Check wheather apim is running\033[0;37m"


def refresh():
    global clientData
    global viewAccessToken
    global createAccessToken
    global publishAccessToken
    clientData = publisher.registerClient().json()
    viewAccessToken = publisher.generateAccessToken(clientData, 'apim:api_view').json()['access_token']
    createAccessToken = publisher.generateAccessToken(clientData, 'apim:api_create').json()['access_token']
    publishAccessToken = publisher.generateAccessToken(clientData, 'apim:api_publish').json()['access_token']
    return "System is refreshed."


def printTokens():
    print("View Access Token: ", viewAccessToken)
    print("Create Access Token: ", createAccessToken)
    print("Publish Access Token: ", publishAccessToken)


print(start())


while True:
    command = input("\033[1;32mexecute: \033[0;37m").strip()
    if command == "exit":
        print("Shutting down cli...")
        break
    elif command == "refresh":
        print(refresh())
    elif command == "print tokens":
        printTokens()
    elif command.startswith("view apis"):
        print(json.dumps(publisher.viewApis(viewAccessToken).json(), indent=4, sort_keys=True))
    elif command.startswith("delete api @"):
        apiId = command.split("@")[1]
        print(publisher.deleteApi(createAccessToken, apiId))
    elif command.startswith("view api @"):
        apiId = command.split("@")[1]
        print(json.dumps(publisher.viewApi(viewAccessToken, apiId).json(), indent=4, sort_keys=True))
    elif command.startswith("update api @"):
        apiId = command.split("@")[1]
        jsonFileName = input("Enter json file name containing the payload: ")
        response = publisher.updateApi(createAccessToken, apiId, jsonFileName)
        print(response)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
    elif command.startswith("view resource policies @"):
        apiId = command.split("@")[1]
        print(publisher.viewResourcePolicyDefinitions(viewAccessToken, apiId).json())
    elif command.startswith("view resource policy @"):
        apiId = command.split("@")[1]
        resourceId = input("Enter resource id: ")
        print(publisher.viewResourcePolicyDefinition(viewAccessToken, apiId, resourceId).json())
    elif command.startswith("update resource policy @"):
        apiId = command.split("@")[1]
        resourceId = input("Enter resource id: ")
        resourcePolicyDefinitionFileName = input("Enter file name containing the resource policy definition: ")
        print(publisher.updateResourcePolicyDefinition(createAccessToken, apiId, resourceId, resourcePolicyDefinitionFileName).json())
    elif command.startswith("view swagger @"):
        apiId = command.split("@")[1]
        print(json.dumps(publisher.viewSwaggerApi(viewAccessToken, apiId), indent=4, sort_keys=True).json())
    elif command.startswith("update swagger @"):
        apiId = command.split("@")[1]
        swaggerDefinitionFileName = input("Enter file name containing the swagger definition: ")
        print(publisher.updateSwaggerDefinition(createAccessToken, apiId, swaggerDefinitionFileName).json())
    elif command.startswith("download thumbnail @"):
        apiId = command.split("@")[1]
        print(publisher.downloadThumbnailImage(viewAccessToken, apiId))
    elif command.startswith("upload thumbnail @"):
        apiId = command.split("@")[1]
        imgFileName = input("Enter image file name: ")
        print(publisher.uploadThumbnailImage(createAccessToken, apiId, imgFileName))
    elif command.startswith("publish api @"):
        apiId = command.split("@")[1]
        print(publisher.changeApiStatus(publishAccessToken, apiId, "Publish"))
    elif command.startswith("create api version @"):
        apiId = command.split("@")[1]
        newVersion = input("Enter version: ")
        print(publisher.createApiVersion(createAccessToken, apiId, newVersion).json())
    elif command.startswith("create api"):
        jsonFileName = input("Enter json file name containing the payload: ")
        response = publisher.createApi(createAccessToken, jsonFileName)
        print(response)
        if response.status_code == 201:
            pyperclip.copy(response.json()['id'])
            print(json.dumps(response.json(), indent=4, sort_keys=True))
    else:
        print("command not found, refer the documentation in https://github.com/binodmx/wso2-apim-restful-api-cli")
    print()
