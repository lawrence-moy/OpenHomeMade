from PySide import QtCore
from PySide import QtNetwork

class HTTPHandler(QtCore.QObject):
  def __init__(self):
    QtCore.QObject.__init__(self)
    self.onRequestParam   = (None, None)
    self.offRequestParam  = (None, None)
    
    self.postManager = QtNetwork.QNetworkAccessManager(self)
    self.getManager = QtNetwork.QNetworkAccessManager(self)
    
    #self.comStateCumulusLabel = QtGui.QLabel("Etat COM Cumulus :")
    #self.comStateCounterLabel = QtGui.QLabel("Etat COM Compteur :")
    #self.comStatePylierLabel  = QtGui.QLabel("Etat COM Pylier :")
    
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
    url = QtCore.QUrl(urlPath)
    request = QtNetwork.QNetworkRequest(url)
    request.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json")
    print("POST:", replyCallback)
    self.postManager.finished[QtNetwork.QNetworkReply].connect(replyCallback)
    self.postManager.post(request, data)
    
  def get(self, urlPath, replyCallback):
    url = QtCore.QUrl(urlPath)
    request = QtNetwork.QNetworkRequest(url)
    print("GET:", urlPath)
    self.getManager.finished[QtNetwork.QNetworkReply].connect(replyCallback)
    self.postManager.get(request)
