import sys
if sys.version_info[0] < 3:
  import urllib2
  import urllib
else:
  import urllib.request

class HTTPHandler():
  def __init__(self):
    pass

  def setupGUI(self):
    pass
      
  def getSwitchOnParameters(self):
    return self.onRequestParam
    
  def getSwitchOffParameters(self):
    return self.offRequestParam
    
  def post(self, urlPath, data, replyCallback):
    try:
      if sys.version_info[0] < 3:
        request = urllib2.Request(urlPath, data)
        response = urllib2.urlopen(request)
        json = response.read()
      else:
        data = data.encode('utf-8')
        request = urllib.request.Request(urlPath, data)
        response = urllib.request.urlopen(request)
        #print(response.read())
    except:
      print("Error:", sys.exc_info()[0])
      
  def get(self, urlPath):
    try:
      if sys.version_info[0] < 3:
        response = urllib2.urlopen(urlPath)
        json = response.read()
        response.close()
        return json
      else:
        response = urllib.request.urlopen(urlPath)
        json = response.read()
        response.close()
        return json
    except:
      print("Error:", sys.exc_info()[0])
      return None
