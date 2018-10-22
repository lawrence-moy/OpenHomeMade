import sys
if sys.version_info[0] < 3:
  import urllib2
  import urllib
else:
  import urllib.request

class HTTPHandler():
  def __init__(self):
    pass
    
  def post(self, urlPath, data, replyCallback):
    try:
      if sys.version_info[0] < 3:
        request = urllib2.Request(urlPath, data)
        response = urllib2.urlopen(request, data=None, timeout=1)
        json = response.read()
      else:
        data = data.encode('utf-8')
        request = urllib.request.Request(urlPath, data)
        response = urllib.request.urlopen(request, data=None, timeout=1)
        #print(response.read())
    except:
      print("HTTPHandler:", sys.exc_info())
      
  def get(self, urlPath):
    try:
      if sys.version_info[0] < 3:
        response = urllib2.urlopen(urlPath, data=None, timeout=2)
        json = response.read()
        response.close()
        return json
      else:
        response = urllib.request.urlopen(urlPath, data=None, timeout=2)
        json = response.read()
        response.close()
        return json
    except:
      print("HTTPHandler:", sys.exc_info()[0])
      return None
