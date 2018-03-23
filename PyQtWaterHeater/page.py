from PySide import QtGui
import string_value_widget
import button_widget
import label_widget
import image_widget
import date_widget
import page_title_widget

class Page():
  def __init__(self, parent):
    self.parent          = parent
    self.title           = ""
    self.widgetList      = []
    self.backgroundImage = "" 

  def init(self):
    pass
    
  def show(self):
    for widget in self.widgetList:
      widget.show()
  
  def hide(self):
    for widget in self.widgetList:
      widget.hide()
    
  def loadXMLConfiguration(self, element):
    self.title           = element.attribute("title", "")
    self.backgroundImage = element.attribute("backgroundImage", "")
    widgetNode = element.firstChild()
    while not widgetNode.isNull():
      widgetElement = widgetNode.toElement()
      if not widgetElement.isNull():
        if "Widget" == widgetElement.tagName():
          type = widgetElement.attribute("type", "")
          widget = None
          if "label" == type:
            widget = label_widget.LabelWidget()
          elif "image" == type:
            widget = image_widget.ImageWidget()
          elif "value" == type:
            widget = string_value_widget.StringValueWidget()
            variable = widget.getVariable()
            self.parent.getDataRetrievingManager().registerConsumer(widget, variable)
          elif "button" == type:
            widget = button_widget.ButtonWidget(self.parent)
          elif "date" == type:
            widget = date_widget.DateWidget()
          elif "page_title" == type:
            widget = page_title_widget.PageTitleWidget()
            self.parent.registerPageTitleConsumer(widget)
            
          widget.loadXMLConfiguration(widgetElement)
          widget.init()
            
          widget.setParent(self.parent)
          widget.move(widget.getX(), widget.getY())
          widget.setFixedSize(widget.getWidth(), widget.getHeight())
          widget.hide()
          self.widgetList.append(widget)
      widgetNode = widgetNode.nextSibling()
  
  def getWidgets(self):
    return self.widgetList
    
  def getTitle(self):
    return self.title
    
  def getBackgroundImage(self):
    return self.backgroundImage
