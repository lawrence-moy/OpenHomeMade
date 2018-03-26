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
    super(ButtonWidget, self).loadXMLConfiguration(self, element)
    font = self.font()
    font.setPointSize(self.fontSize)
    self.setFont(font)
    self.setStyleSheet("font-weight: " + self.fontWeight + "; color: " + self.fontColor)
      
  def loadXMLSpecificElement(self, element):
    if "Text" == element.tagName():
      self.setText(element.attribute("value", ""))
    elif "HTTPPostRequest" == element.tagName():
      url  = element.attribute("url", "")
      body = element.attribute("body", "")
      self.requestList.append((url, body))
    elif "ModuleEvent" == element.tagName():
      moduleName = element.attribute("module", "")
      event      = element.attribute("event", "")
      module = self.parent.getModule(moduleName)
      if None != module:
        callback = module.getCallback(event)
        QtCore.QObject.connect(self, 
                               QtCore.SIGNAL("clicked()"), 
                               callback)
                               
  def clickedEvent(self):
    for request in self.requestList:
      url, body = request
      self.httpHandler.post(url, body, self.replyCallback)
  
  def replyCallback(self, reply):
    print(reply.readAll())
