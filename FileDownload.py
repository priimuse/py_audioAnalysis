import requests #v2.31.0
import time
import os
import sys

def GetRequest(url=None, retries=1, auth=None, headers=None, timeout=None, params=None):
    failed = False

    if url is None:
        failed = True
    elif type(url) != str:
        failed = True
    if timeout is not None and type(timeout) != int: failed = True
    if params is not None and type(params) != dict: failed = True
    if failed:
        raise ValueError('GetRequest() failed!: incoming args errors!')

    res = None
    for i in range(retries):
        try:
            authSes = requests.Session()
            if auth is not None: authSes.auth = auth
            if headers is not None: authSes.headers = headers
            if params is not None: authSes.params = params
            print("get attempt %i of %i:\n%s" % (i + 1, retries, url))
            if timeout == None:
                res = authSes.get(url)
            else:
                res = authSes.get(url, timeout=timeout)
            if res is None: raise ValueError("res is None!")
            if res.status_code == 200:
                break
            else:
                raise ValueError(res.status_code, res.headers)
        except:
            print("GetRequest() failed!:", sys.exc_info())
    return res

def AuthInitial(url, auth):
    failed = False
    if url == None:
        failed = True
    elif type(url) != str:
        failed = True
    if auth == None: failed = True
    if failed:
        raise ValueError("authinit() missing args!")

    authRes = GetRequest(
        url=url,
        auth=auth,
        retries=3).json()

    if authRes is not None and type(authRes) == dict:
        return (
            {
                "ts": int(time.time()),  # int
                "url": authRes["apiUrl"],  # str
                "token": authRes["authorizationToken"],  # str
                "recPartSize": authRes["recommendedPartSize"],  # int
                "absMinPartSize": authRes["absoluteMinimumPartSize"]  # int
            })

def GetInitialAuth():
	outObj = AuthInitial(
		url='https://api.backblazeb2.com/b2api/v3/b2_authorize_account',
        auth=(INITAUTHCREDS[0], INITAUTHCREDS[1]) )

	print("GetInitialAuth(): returning auth ts ", outObj["ts"])
	return outObj

def main(argsList):
    #given an infile, download from b2 storage
    inBlobName = argsList[3]
    INITAUTHCREDS = (argsList[1], argsList[2])
    _INITAUTHOBJ = GetInitialAuth()
    authTokenStr = _INITAUTHOBJ["token"]
    authorizedUrl = _INITAUTHOBJ["url"]
    fileInfoRes_header = {
        "Content-Type": "application/json",
        "Authorization": authTokenStr
    }

    extension = inBlobName.split(".")[-1].lower()
    outFileSavePath = os.path.join(os.getcwd(), "temp", "out", extension)

    dlObj_bytes = GetRequest(url=authorizedUrl + '/file/' + argsList[4] + '/' + inBlobName, retries=3, timeout=30, headers=fileInfoRes_header, params={})
    if dlObj_bytes.ok:
        print("bytes returned: ", len(dlObj_bytes.content))
        with open(outFileSavePath, "wb") as f:
            f.write(dlObj_bytes.content)
    else:
        print("failed blob download!")
        return None
    return outFileSavePath

ret = main(sys.argv)
print("file dowloaded to ", ret)
