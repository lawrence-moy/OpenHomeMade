from PySide import QtGui
import string_value_widget
import button_widget

class Page():
  def __init__(self, parent, title):
    self.title      = title
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
          elif "value" == type:
            variable = widgetElement.attribute("variable", "")
            widget = string_value_widget.StringValueWidget(variable)
            self.parent.getDataRetrievingManager().registerConsumer(widget, variable)
            widget.init()
          elif "button" == type:
            widget = button_widget.ButtonWidget(self.parent)
            widget.loadXMLConfiguration(widgetElement)
            widget.init()
            
          x      = int(widgetElement.attribute("x", "0"))
          y      = int(widgetElement.attribute("y", "0"))
          width  = int(widgetElement.attribute("width", "50"))
          height = int(widgetElement.attribute("height", "50"))
          widget.setParent(self.parent)
          widget.move(x, y)
          widget.setFixedSize(width, height)
          widget.hide()
          self.widgetList.append(widget)
      widgetNode = widgetNode.nextSibling()
  
  def getWidgets(self):
    return self.widgetList
    
  def getTitle(self):
    return self.title
    