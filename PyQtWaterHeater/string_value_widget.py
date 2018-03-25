from PySide import QtGui 
from PySide import QtCore
import generic_widget

class StringValueWidget(QtGui.QLabel, generic_widget.GenericWidget):
  def __init__(self, dataRetrievingManager):
    QtGui.QLabel.__init__(self)
    generic_widget.GenericWidget.__init__(self)
    self.variableName          = ""
    self.dataRetrievingManager = dataRetrievingManager
    
  def init(self):
    self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    
  def loadXMLConfiguration(self, element):
    super(StringValueWidget, self).loadXMLConfiguration(element)
    self.moduleId     = int(element.attribute("moduleId", ""))
    self.variableName = element.attribute("variable", "")
    self.dataRetrievingManager.registerConsumer(self, self.moduleId, self.variableName)
    font = self.font()
    font.setPointSize(int(element.attribute("fontSize", "12")))
    self.setFont(font)
    fontColor  = element.attribute("fontColor", "#000000")
    fontWeight = element.attribute("fontWeight", "normal")
    self.setStyleSheet("font-weight: " + fontWeight + "; color: " + fontColor)
    
  def getVariable(self):
    return self.variableName
    
  def setValue(self, value):
    self.setText(str(value))
    
  def paintEvent(self, event):
    super(StringValueWidget, self).paintEvent(event)
    qpainter = QtGui.QPainter(self)
    qpainter.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
    