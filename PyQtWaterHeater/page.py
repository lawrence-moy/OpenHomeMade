from PySide import QtGui

class Page():
  def __init__(self, parent, title):
    self.title      = title
    self.gridLayout = QtGui.QGridLayout()
    self.widgetList = []
    self.parent     = parent
    
  def init(self):
    pass
    
  def show(self):
    for widget in self.widgetList:
      widget.show()
  
  def hide(self):
    for widget in self.widgetList:
      widget.hide()
    
  def loadXMLConfiguration(self, element):
    widgetNode = element.firstChild()
    while not widgetNode.isNull():
      widgetElement = widgetNode.toElement()
      if not widgetElement.isNull():
        if "Widget" == widgetElement.tagName():
          type = widgetElement.attribute("type", "")
          widget = None
          if "label" == type:
            text   = widgetElement.attribute("text", "")
            widget = QtGui.QLabel(text)
          elif "image" == type:
            path   = widgetElement.attribute("path", "")
            pixmap = QtGui.QPixmap(path)
            widget = QtGui.QLabel(text)
            widget.setPixmap(pixmap)
            
          x    = int(widgetElement.attribute("x", "0"))
          y    = int(widgetElement.attribute("y", "0"))
          widget.setParent(self.parent)
          widget.move(x, y)
          widget.show()
          self.widgetList.append(widget)
      widgetNode = widgetNode.nextSibling()
  
  def getWidgets(self):
    return self.widgetList
    
  def getTitle(self):
    return self.title
    