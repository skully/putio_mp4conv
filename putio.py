import requests, json


def config():
    
    confDict = dict()
    try:
        print "Config file found!"
        with open(".config", "r") as confFile:
            for confLine in confFile:
                listOfConf = confLine.replace(" ", "").split(":",1)
                confDict.update({listOfConf[0]:listOfConf[1]})

    except IOError:
        print "No .config file! Let's make one!"
        confFile = open(".config", "w")

        oAuthToken = raw_input("OAuthToken: ")
        confFile.write("oauth: "+oAuthToken)
        confDict.update({"oauth":oAuthToken})

    confFile.close()
    
    return confDict






def get_filelist(confDict, id):
    payload = {'oauth_token':confDict['oauth']}

    if id == 0:
        result = requests.get("https://api.put.io/v2/files/list", params=payload)
    else:
        payload.update({'parent_id': id})
        result = requests.get("https://api.put.io/v2/files/list", params=payload)

    parsed = json.loads(result.text)
    return parsed


