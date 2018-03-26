from PySide import QtGui 
from PySide import QtCore
import generic_widget

class DateWidget(QtGui.QLabel, generic_widget.GenericWidget):
  def __init__(self):
    QtGui.QLabel.__init__(self)
    generic_widget.GenericWidget.__init__(self)
    self.updateTimer = QtCore.QTimer()
    self.format      = "hh:mm:ss"
    self.bgImage     = ""

  def init(self):
    self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    self.updateDate()
    QtCore.QObject.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.updateDate)
    self.updateTimer.start(1000)

  def loadXMLConfiguration(self, element):
    super(DateWidget, self).loadXMLConfiguration(self, element)
    font = self.font()
    font.setPointSize(self.fontSize)
    self.setFont(font)
    self.setStyleSheet("font-weight: " + self.fontWeight + "; color: " + self.fontColor)
    
  def loadXMLSpecificElement(self, element):
    if "Date" == element.tagName():
      self.format = element.attribute("format", "hh:mm:ss")
    
  def updateDate(self):
    self.setText(QtCore.QDateTime.currentDateTime().toString(self.format))
    
  def paintEvent(self, event):
    qpainter = QtGui.QPainter(self)
    qpainter.drawPixmap(QtCore.QPoint(0,0), QtGui.QPixmap(self.bgImage))
    super(DateWidget, self).paintEvent(event)
    