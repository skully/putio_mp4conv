import requests, json, os


def config():
    confDict = dict()
    try:
        print("Config file found!")
        with open(".config", "r") as confFile:
            for confLine in confFile:
                listOfConf = confLine.replace(" ", "").split(":",1)
                confDict.update({listOfConf[0]:listOfConf[1]})

    except IOError:
        print("No .config file! Let's make one!")
        confFile = open(".config", "w")

        oAuthToken = raw_input("OAuthToken: ")
        confFile.write("oauth: "+oAuthToken)
        confDict.update({"oauth":oAuthToken})

    confFile.close()
    
    return confDict


def get_filelist(confDict, id):
    payload = {'oauth_token':confDict['oauth']}

    if id != 0:
        payload.update({'parent_id': id})

    result = requests.get("https://api.put.io/v2/files/list", params=payload)

    parsed = json.loads(result.text)
    return parsed


def search(confDict, word):
    payload = {'oauth_token':confDict['oauth']}
    query = "from:me " + word
    payload["query"] = query

    result = requests.get("https://api.put.io/v2/files/search/", params=payload)

    parsed = json.loads(result.text)
    return parsed


def get_infos(confDict,id):
    payload = {'oauth_token':confDict['oauth']}
    result = requests.get("https://api.put.io/v2/files/"+ str(id) , params=payload)
    parsed = json.loads(result.text)
    if parsed['status'] ==  'OK':
        return parsed['file']
    else:
        return "ERR"


def download_file(confDict, id, path = "."):
    payload = {'oauth_token':confDict['oauth']}
    url = "https://api.put.io/v2/files/" + str(id) + "/download"

    try:
        local_file = get_infos(confDict,id)
    except requests.exceptions.ConnectionError:
        return -1
    
    local_filename = local_file['name'] 
    
    if not os.path.exists(path):
            os.makedirs(path)

    r = requests.get(url, params = payload,stream = True)
    with open((path+"/"+local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: 
                f.write(chunk)
                f.flush()
    
    return local_filename

def upload_file(confDict, path_to_file = ".", parent_id=0): 
    payload = {'oauth_token' : confDict['oauth']}
    payload["parent_id"] = parent_id

    try:
        files = {'file' : open(path_to_file,'rb')}
        url = 'https://upload.put.io/v2/files/upload'
        
        result = requests.post(url, params=payload, files= files )

        files['file'].close
        parsed = json.loads(result.text)
        return parsed
    except NameError:
        return None    

def move_file(confDict, file_id, parent_id):
    url = 'https://api.put.io/v2/files/move'
    payload = {'oauth_token' : confDict['oauth']}
    payload.update( {'file_ids': str(file_id), 'parent_id': str(parent_id)})
    result = requests.post(url, data=payload)
    parsed = json.loads(result.text)
    return parsed


