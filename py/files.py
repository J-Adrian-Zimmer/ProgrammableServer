import json

def read(path):
  try:
    with open(path,'rb') as fi:
       return fi.read()
  except:
    return False

def write(path,string):
  try:
    with open(path,'wb') as fo:
       fo.write(string)
    return True
  except:
    return False

def readJSON(path):
  try:
     return tobytes( json.loads( read(path) ) )
  except:
     return False

def writeJSON(path,jsonstr):
  try:
     write(path, json.dumps(jsonstr))
     return True
  except:
     return False

def tobytes(obj):
    if isinstance(obj, dict):
        return {
           tobytes(key):tobytes(value) 
             for key,value in obj.iteritems()
        }
    elif isinstance(obj, list):
        return [tobytes(element) for element in obj]
    elif isinstance(obj, unicode):
        return obj.encode('utf-8')
    else:
        return obj

