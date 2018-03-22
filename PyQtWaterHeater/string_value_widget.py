from PySide import QtGui 
from PySide import QtCore
import generic_widget

class StringValueWidget(QtGui.QLabel, generic_widget.GenericWidget):
  def __init__(self):
    QtGui.QLabel.__init__(self)
    generic_widget.GenericWidget.__init__(self)
    self.variableName = ""
    
  def init(self):
    self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    #self.setStyleSheet("font-weight: bold; color: black")
    
  def loadXMLConfiguration(self, element):
    super(StringValueWidget, self).loadXMLConfiguration(element)
    self.variableName = element.attribute("variable", "")
    font = self.font()
    font.setPointSize(int(element.attribute("fontSize", "12")))
    self.setFont(font)
    
  def getVariable(self):
    return self.variableName
    
  def setValue(self, value):
    self.setText(str(value))
    
  def paintEvent(self, event):
    super(StringValueWidget, self).paintEvent(event)
    qpainter = QtGui.QPainter(self)
    qpainter.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
    