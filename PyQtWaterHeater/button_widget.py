from PySide import QtGui 
from PySide import QtCore

class ButtonWidget(QtGui.QPushButton):
  def __init__(self, parent):
    QtGui.QPushButton.__init__(self)
    self.fontSize     = 13
    self.requestList  = []
    self.parent       = parent
    self.httpHandler  = parent.getHTTPHandler()
    
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
      eventElement = requestNode.toElement()
      if not eventElement.isNull():
        if "HTTPPostRequest" == eventElement.tagName():
          url  = eventElement.attribute("url", "")
          body = eventElement.attribute("body", "")
          self.requestList.append((url, body))
        elif "ModuleEvent" == eventElement.tagName():
          moduleName = eventElement.attribute("module", "")
          event      = eventElement.attribute("event", "")
          module = self.parent.getModule(moduleName)
          if None != module:
            callback = module.getCallback(event)
            QtCore.QObject.connect(self, 
                                   QtCore.SIGNAL("clicked()"), 
                                   callback)
      requestNode = requestNode.nextSibling()
    
  def clickedEvent(self):
    for request in self.requestList:
      url, body = request
      self.httpHandler.post(url, body, self.replyCallback)
  
  def replyCallback(self, reply):
    print(reply)
