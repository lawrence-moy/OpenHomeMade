from PySide import QtGui 
from PySide import QtCore

class ButtonWidget(QtGui.QPushButton):
  def __init__(self, httpHandler):
    QtGui.QPushButton.__init__(self)
    self.fontSize     = 13
    self.requestList  = []
    self.httpHandler  = httpHandler
    
  def init(self):
    QtCore.QObject.connect(self, 
                           QtCore.SIGNAL("clicked()"), 
                           self.clickedEvent)
    
    #buttonFont = QtGui.QFont(button.font())
    #buttonFont.setPointSize(30)
    #button.setFont(buttonFont)
    #button.setFixedSize(300, 100)
    
  def loadXMLConfiguration(self, element):
    self.setText(element.attribute("text", ""))
    requestNode = element.firstChild()
    while not requestNode.isNull():
      requestElement = requestNode.toElement()
      if not requestElement.isNull():
        if "HTTPPostRequest" == requestElement.tagName():
          url  = requestElement.attribute("url", "")
          body = requestElement.attribute("body", "")
          self.requestList.append((url, body))
      requestNode = requestNode.nextSibling()
    
  def clickedEvent(self):
    for request in self.requestList:
      url, body = request
      self.httpHandler.post(url, body, self.replyCallback)
  
  def replyCallback(self, reply):
    print(reply)
