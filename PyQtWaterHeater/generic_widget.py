
class GenericWidget(object):
  def __init__(self):
    self._x      = 0
    self._y      = 0
    self._width  = 50
    self._height = 50

  def init(self):
    pass
    
  def loadXMLConfiguration(self, element):
    self._x      = int(element.attribute("x", "0"))
    self._y      = int(element.attribute("y", "0"))
    self._width  = int(element.attribute("width", "50"))
    self._height = int(element.attribute("height", "50"))
    
  def getX(self):
    return self._x
  
  def getY(self):
    return self._y
    
  def getWidth(self):
    return self._width
    
  def getHeight(self):
    return self._height
    
