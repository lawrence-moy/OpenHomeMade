from PySide import QtGui 
from PySide import QtCore
import generic_widget

class StringValueWidget(QtGui.QLabel, generic_widget.GenericWidget):
  def __init__(self, dataRetrievingManager):
    QtGui.QLabel.__init__(self)
    generic_widget.GenericWidget.__init__(self)
    self.moduleId              = None
    self.variableName          = ""
    self.dataRetrievingManager = dataRetrievingManager
    
  def init(self):
    self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    
  def loadXMLConfiguration(self, element):
    super(StringValueWidget, self).loadXMLConfiguration(self, element)
    font = self.font()
    font.setPointSize(self.fontSize)
    self.setFont(font)
    self.setStyleSheet("font-weight: " + self.fontWeight + "; color: " + self.fontColor)
    
  def loadXMLSpecificElement(self, element):
    if "Value" == element.tagName():
      self.moduleId     = int(element.attribute("moduleId", ""))
      self.variableName = element.attribute("variable", "")
      self.dataRetrievingManager.registerConsumer(self, self.moduleId, self.variableName)
    
  def getVariable(self):
    return self.variableName
    
  def setValue(self, value):
    self.setText(str(value))
    
  def paintEvent(self, event):
    qpainter = QtGui.QPainter(self)
    color = QtGui.QColor(self.bgColor)
    color.setAlpha(self.bgAlpha)
    brush = QtGui.QBrush(color)
    qpainter.fillRect(0, 0, self.width(), self.height(), brush)
    super(StringValueWidget, self).paintEvent(event)

    