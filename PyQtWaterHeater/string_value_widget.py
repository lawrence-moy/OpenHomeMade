from PySide import QtGui 
from PySide import QtCore

class StringValueWidget(QtGui.QLabel):
  def __init__(self, variableName):
    QtGui.QLabel.__init__(self)
    self.fontSize     = 13
    self.variableName = variableName
    
  def init(self):
    self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    #valueFont = self.font()
    #valueFont.setPointSize(self.fontSize)
    #self.setFont(labelTitleFont)
    #self..setStyleSheet("font-weight: bold; color: black")
    
  def setValue(self, value):
    self.setText(str(value))
    
  def paintEvent(self, event):
    p = QtGui.QPainter(self)
    p.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
    super(StringValueWidget, self).paintEvent(event)
