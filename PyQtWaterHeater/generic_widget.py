
class GenericWidget(object):
  def __init__(self):
    self._x         = 0
    self._y         = 0
    self._width     = 50
    self._height    = 50
    self.fontSize   = 12
    self.fontColor  = "#000000"
    self.fontWeight = "normal"
    self.fontName   = "arial"
    self.bgColor    = "#FFFFFF"
    self.bgImage    = ""
    
  def init(self):
    pass
    
  def loadXMLConfiguration(self, widget, element):
    subWidgetNode = element.firstChild()
    while not subWidgetNode.isNull():
      subElement = subWidgetNode.toElement()
      if not subElement.isNull():
        if "Geometry" == subElement.tagName():
          self.loadXMLGeometry(subElement)
        elif "Font" == subElement.tagName():
          self.loadXMLFont(subElement)
        elif "Background" == subElement.tagName():
          self.loadXMLBackground(subElement)
        else:
          widget.loadXMLSpecificElement(subElement)
      subWidgetNode = subWidgetNode.nextSibling()
  
  def loadXMLSpecificElement(self, element):
    print("NEED TO WRITE FUNCTION")
    
  def loadXMLGeometry(self, element):
    self._x      = int(element.attribute("x",      "0"))
    self._y      = int(element.attribute("y",      "0"))
    self._width  = int(element.attribute("width",  "50"))
    self._height = int(element.attribute("height", "50"))
    
  def loadXMLFont(self, element):
    self.fontSize   = int(element.attribute("size", "12"))
    self.fontColor  = element.attribute("color",  "#000000")
    self.fontWeight = element.attribute("weight", "normal")
    self.fontName   = element.attribute("name",   "arial")
    
  def loadXMLBackground(self, element):
    self.bgColor = element.attribute("color", "#000000")
    self.bgImage = element.attribute("image", "")
    
  def getX(self):
    return self._x
  
  def getY(self):
    return self._y
    
  def getWidth(self):
    return self._width
    
  def getHeight(self):
    return self._height
