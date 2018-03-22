from PySide import QtGui 
from PySide import QtCore

class LabelWidget(QtGui.QLabel):
  def __init__(self):
    QtGui.QLabel.__init__(self)

  def init(self):
    self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

  def loadXMLConfiguration(self, element):
    self.setText(element.attribute("text", ""))
    font = self.font()
    font.setPointSize(int(element.attribute("fontSize", "12")))
    self.setFont(font)
    
  def paintEvent(self, event):
    p = QtGui.QPainter(self)
    p.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
    super(LabelWidget, self).paintEvent(event)
