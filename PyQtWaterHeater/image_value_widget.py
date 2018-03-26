from PySide import QtGui 
import generic_widget

class ImageValueWidget(QtGui.QLabel, generic_widget.GenericWidget):
  def __init__(self, dataRetrievingManager):
    QtGui.QLabel.__init__(self)
    generic_widget.GenericWidget.__init__(self)
    self.animations            = {}
    self.currentAnimation      = None
    self.dataRetrievingManager = dataRetrievingManager
    self.currentValue          = None
    
  def loadXMLConfiguration(self, element):
    super(ImageValueWidget, self).loadXMLConfiguration(self, element)
    
  def loadXMLSpecificElement(self, element):
    if "Image" == element.tagName():
      onValue   = int(element.attribute("onValue", "1"))
      animation = QtGui.QMovie(element.attribute("path", ""))
      if not animation.isValid():
        print("ImageValueWidget animation not valid!")
        return
      self.animations[onValue] = animation
      self.setMovie(animation)
      #animation.start()
    elif "Value" == element.tagName():
      self.moduleId     = int(element.attribute("moduleId", ""))
      self.variableName = element.attribute("variable", "")
      self.dataRetrievingManager.registerConsumer(self, self.moduleId, self.variableName)
      
  def setValue(self, value):
    self.currentValue = value
    self.update()
      
  def paintEvent(self, event):
    super(ImageValueWidget, self).paintEvent(event)
    if self.animations.get(self.currentValue):
      self.currentAnimation = self.animations[self.currentValue]
      self.setMovie(self.animations[self.currentValue])
      self.animations[self.currentValue].start()
      self.show()
    else:
      if None != self.currentAnimation:
        self.currentAnimation.stop()
        self.hide()
    #p = QtGui.QPainter(self)
    #p.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
    