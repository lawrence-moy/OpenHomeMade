from PySide import QtCore
from PySide import QtNetwork
import sys
if sys.version_info[0] < 3:
  import urllib2
  import urllib
else:
  import urllib.request

class HTTPHandler(QtCore.QObject):
  def __init__(self):
    QtCore.QObject.__init__(self)
    self.onRequestParam   = (None, None)
    self.offRequestParam  = (None, None)

  def setupGUI(self):
    pass
    
  def getXMLConfiguration(self, doc):
    networkNode    = doc.createElement("Network")
    onRequestNode  = doc.createElement("OnRequest")
    onRequestNode.setAttribute("url",  self.onRequestParam[0])
    onRequestNode.setAttribute("body", self.onRequestParam[1])
    offRequestNode = doc.createElement("OffRequest")
    offRequestNode.setAttribute("url",  self.offRequestParam[0])
    offRequestNode.setAttribute("body", self.offRequestParam[1])
    networkNode.appendChild(onRequestNode)
    networkNode.appendChild(offRequestNode)
    return networkNode

  def parseXMLParameters(self, element):
    subNetworkNode = element.firstChild()
    while not subNetworkNode.isNull():
      subNetworkElement = subNetworkNode.toElement()
      if not subNetworkElement.isNull():
        if "OnRequest" == subNetworkElement.tagName():
           urlOn = subNetworkElement.attribute("url", "")
           bodyOn = subNetworkElement.attribute("body", "")
           self.onRequestParam = (urlOn, bodyOn)
        elif "OffRequest" == subNetworkElement.tagName():
           urlOff  = subNetworkElement.attribute("url", "")
           bodyOff = subNetworkElement.attribute("body", "")
           self.offRequestParam = (urlOff, bodyOff)
      subNetworkNode = subNetworkNode.nextSibling()
      
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
        print(json)
      else:
        x = urllib.request.urlopen(urlPath)
        print(x.read())
    except:
      print("Ooops")
      
  def get(self, urlPath):
    try:
      if sys.version_info[0] < 3:
        response = urllib2.urlopen(urlPath)
        #print(response.info())
        json = response.read()
        #print(json)
        response.close()
        return json
      else:
        response = urllib.request.urlopen(urlPath)
        print(response.read())
    except:
      print("Ooops")
      return None