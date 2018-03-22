from PySide import QtGui 
from PySide import QtCore
import generic_widget

class ButtonWidget(QtGui.QPushButton, generic_widget.GenericWidget):
  def __init__(self, parent):
    QtGui.QPushButton.__init__(self)
    generic_widget.GenericWidget.__init__(self)
    self.parent       = parent
    self.httpHandler  = parent.getHTTPHandler()
    self.requestList  = []
    
  def init(self):
    QtCore.QObject.connect(self, 
                           QtCore.SIGNAL("clicked()"), 
                           self.clickedEvent)
    
  def loadXMLConfiguration(self, element):
    super(ButtonWidget, self).loadXMLConfiguration(element)
    self.setText(element.attribute("text", ""))
    font = self.font()
    font.setPointSize(int(element.attribute("fontSize", "12")))
    self.setFont(font)
    
    fontColor  = element.attribute("fontColor", "#000000")
    fontWeight = element.attribute("fontWeight", "normal")
    self.setStyleSheet("font-weight: " + fontWeight + "; color: " + fontColor)
    
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
