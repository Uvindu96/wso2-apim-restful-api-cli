from publisher import *


def start():
    try:
        registerClient()
        generateAccessToken('apim:api_view')['access_token']
        generateAccessToken('apim:api_create')['access_token']
        generateAccessToken('apim:api_publish')['access_token']
        return "\033[1;34mClient registration is successful\033[0;37m"
    except:
        return "\033[1;31mClient registration is unsuccessful. Check wheather apim is running\033[0;37m"


def refresh():
    global clientData
    global viewAccessToken
    global createAccessToken
    global publishAccessToken
    clientData = registerClient()
    viewAccessToken = generateAccessToken('apim:api_view')
    createAccessToken = generateAccessToken('apim:api_create')
    publishAccessToken = generateAccessToken('apim:api_publish')
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
        print()
        break
    elif command == "refresh":
        print(refresh())
        print()
    elif command == "print tokens":
        printTokens()
        print()
    elif command == "view apis":
        print(json.dumps(viewApis(), indent=4, sort_keys=True))
        print()
    elif command == "create api":
        print(json.dumps(createApi(), indent=4, sort_keys=True))
        print()
    elif command.startswith("view api"):
        apiId = command.split("@")[1]
        print(json.dumps(viewApi(apiId), indent=4, sort_keys=True))
        print()
    elif command.startswith("update api"):
        print()
    elif command.startswith("delete api"):
        apiId = command.split("@")[1]
        print(deleteApi(apiId))
        print()
    elif command.startswith("publish api"):
        apiId = command.split("@")[1]
        publishApi(apiId)
        print()
    elif command.startswith("view swagger api"):
        apiId = command.split("@")[1]
        print(json.dumps(viewSwaggerApi(apiId), indent=4, sort_keys=True))
        print()
    else:
        print("command not found, refer the documentation in https://github.com/binodmx/wso2-apim-restful-api-cli\n")