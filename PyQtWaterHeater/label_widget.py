from PySide import QtGui 
from PySide import QtCore
import generic_widget

class LabelWidget(QtGui.QLabel, generic_widget.GenericWidget):
  def __init__(self):
    QtGui.QLabel.__init__(self)
    generic_widget.GenericWidget.__init__(self)

  def init(self):
    self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

  def loadXMLConfiguration(self, element):
    super(LabelWidget, self).loadXMLConfiguration(element)
    self.setText(element.attribute("text", ""))
    font = self.font()
    font.setPointSize(int(element.attribute("fontSize", "12")))
    self.setFont(font)
    
  def paintEvent(self, event):
    super(LabelWidget, self).paintEvent(event)
    p = QtGui.QPainter(self)
    p.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
    
