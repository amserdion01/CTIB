import requests
import json

def writeToFile ( path, content ):
    pathB = path

    if pathB [ : -1 ] != '/' :
        pathB += '/'
    else :
        path = path [ : -1 ]

    __URL = "http://localhost:8000/files/"
    print(__URL+pathB)
    requests.put ( __URL + pathB, json = { "path" : path, "content" : json.dumps ( content ) } )

def killFile ( path ) :
    if path [ : -1 ] != '/' :
        path += '/'
    __URL = "http://localhost:8000/files/"
    requests.delete ( __URL + path )

def interogateFile ( path ) :
    if path [ : -1 ] != '/' :
        path += '/'
    __URL = "http://localhost:8000/files/"
    r = requests.get ( __URL + path )
    if r.status_code == 404 :
        return None
    return r.json()

def getSubdb ( db ) :
    if db [ : -1 ] != '/' :
        db += '/'
    __URL = "http://localhost:8000/files/"
    r = requests.get ( __URL + db )
    if r.status_code == 404 :
        return None
    return r.json()

def getAllFiles () :
    __URL = "http://localhost:8000/files/"
    r = requests.get ( __URL )
    if r.status_code == 404 :
        return None
    return r.json()