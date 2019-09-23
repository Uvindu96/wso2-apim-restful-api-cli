import publisher
import store
import admin
import json


clientData = None
viewAccessToken = None
createAccessToken = None
publishAccessToken = None
api = "publisher"


def start():
    print("---WSO2 API Manager RESTful API CLI---")
    while True:
        if api == "publisher":
            runPublisher()
        elif api == "store":
            runStore()
        elif api == "admin":
            runAdmin()
        elif api == "exit":
            break
        else:
            break


def runPublisher():
    try:
        global clientData
        global viewAccessToken
        global createAccessToken
        global publishAccessToken
        global api
        clientData = publisher.registerClient().json()
        viewAccessToken = publisher.generateAccessToken(clientData, 'apim:api_view').json()['access_token']
        createAccessToken = publisher.generateAccessToken(clientData, 'apim:api_create').json()['access_token']
        publishAccessToken = publisher.generateAccessToken(clientData, 'apim:api_publish').json()['access_token']
        status = True
        print("\033[1;34mClient registration is successful\033[0;37m")
    except:
        status = False
        api = "wait"
        print("\033[1;31mClient registration is unsuccessful. Check wheather apim is running\033[0;37m")
    while status:
        command = input("\033[1;32mpublisher: \033[0;37m").strip()

        if command == "":
            continue

        elif command == "exit":
            api = "exit"
            break

        elif command == "refresh":
            response = refresh()
            print(response)

        elif command.startswith("view apis"):
            response = publisher.viewApis(viewAccessToken)
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=4, sort_keys=True))
            else:
                print(response)

        elif command.startswith("delete api @"):
            apiId = command.split("@")[1]
            response = publisher.deleteApi('c53b2e64-9df3-36a7', apiId)
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
            response = publisher.updateResourcePolicyDefinition(createAccessToken, apiId, resourceId,
                                                                resourcePolicyDefinitionFileName)
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

        elif command.startswith("view application @"):
            applicationId = command.split("@")[1]
            response = publisher.viewApplication(createAccessToken, applicationId)
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=4, sort_keys=True))
            else:
                print(response)

        elif command.startswith("view certificates"):
            response = publisher.viewCertificates(createAccessToken)
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=4, sort_keys=True))
            else:
                print(response)

        elif command.startswith("view certificate @"):
            alias = command.split("@")[1]
            response = publisher.viewCertificate(createAccessToken, alias)
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=4, sort_keys=True))
            else:
                print(response)

        elif command.startswith("upload certificate @"):
            alias = command.split("@")[1]
            certificate = input("Enter certificate file name: ")
            endpoint = input("Enter endpoint: ")
            response = publisher.uploadCertificate(createAccessToken, alias, certificate, endpoint)
            print(response)

        elif command.startswith("view arns @"):
            apiId = command.split("@")[1]
            response = publisher.viewARNs(viewAccessToken, apiId)
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=4, sort_keys=True))
            else:
                print(response)

        else:
            print("Command is not found, refer the documentation in https://github.com/binodmx/wso2-apim-restful-api-cli")

        print()


def runStore():
    return


def runAdmin():
    return


def refresh():
    try:
        global clientData
        global viewAccessToken
        global createAccessToken
        global publishAccessToken
        clientData = publisher.registerClient().json()
        viewAccessToken = publisher.generateAccessToken(clientData, 'apim:api_view').json()['access_token']
        createAccessToken = publisher.generateAccessToken(clientData, 'apim:api_create').json()['access_token']
        publishAccessToken = publisher.generateAccessToken(clientData, 'apim:api_publish').json()['access_token']
        return "System is refreshed."
    except:
        return "\033[1;31mError while refreshing.. Check wheather apim is running\033[0;37m"


start()



