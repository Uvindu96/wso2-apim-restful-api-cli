import publisher
import store
import admin
import json


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

# publisher ============================================================================================================
    elif command.startswith("view apis"):
        response = publisher.viewApis(viewAccessToken)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    elif command.startswith("delete api @"):
        apiId = command.split("@")[1]
        response = publisher.deleteApi(createAccessToken, apiId)
        print(response)

    elif command.startswith("view api @"):
        apiId = command.split("@")[1]
        response = publisher.viewApi(viewAccessToken, apiId)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    elif command.startswith("update api @"):
        apiId = command.split("@")[1]
        jsonFileName = input("Enter json file name containing the payload: ")
        response = publisher.updateApi(createAccessToken, apiId, jsonFileName)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    elif command.startswith("view resource policies @"):
        apiId = command.split("@")[1]
        response = publisher.viewResourcePolicyDefinitions(viewAccessToken, apiId)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    elif command.startswith("view resource policy @"):
        apiId = command.split("@")[1]
        resourceId = input("Enter resource id: ")
        response = publisher.viewResourcePolicyDefinition(viewAccessToken, apiId, resourceId)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    elif command.startswith("update resource policy @"):
        apiId = command.split("@")[1]
        resourceId = input("Enter resource id: ")
        resourcePolicyDefinitionFileName = input("Enter file name containing the resource policy definition: ")
        response = publisher.updateResourcePolicyDefinition(createAccessToken, apiId, resourceId, resourcePolicyDefinitionFileName)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    elif command.startswith("view swagger @"):
        apiId = command.split("@")[1]
        response = publisher.viewSwaggerDefinition(viewAccessToken, apiId)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    elif command.startswith("update swagger @"):
        apiId = command.split("@")[1]
        swaggerDefinitionFileName = input("Enter file name containing the swagger definition: ")
        response = publisher.updateSwaggerDefinition(createAccessToken, apiId, swaggerDefinitionFileName)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    elif command.startswith("download thumbnail @"):
        apiId = command.split("@")[1]
        response = publisher.downloadThumbnailImage(viewAccessToken, apiId)
        print(response)

    elif command.startswith("upload thumbnail @"):
        apiId = command.split("@")[1]
        imgFileName = input("Enter image file name: ")
        response = publisher.uploadThumbnailImage(createAccessToken, apiId, imgFileName)
        print(response)

    elif command.startswith("change api status @"):
        apiId = command.split("@")[1]
        action = input("Enter status: ")
        response = publisher.changeApiStatus(publishAccessToken, apiId, action)
        print(response)

    elif command.startswith("create api version @"):
        apiId = command.split("@")[1]
        newVersion = input("Enter version: ")
        response = publisher.createApiVersion(createAccessToken, apiId, newVersion)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    elif command.startswith("create api"):
        jsonFileName = input("Enter json file name containing the payload: ")
        response = publisher.createApi(createAccessToken, jsonFileName)
        if response.status_code == 201:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        else:
            print(response)

    else:
        print("command not found, refer the documentation in https://github.com/binodmx/wso2-apim-restful-api-cli")
    print()
