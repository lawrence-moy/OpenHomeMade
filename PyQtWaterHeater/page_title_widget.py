from PySide import QtGui 
from PySide import QtCore
import generic_widget

class PageTitleWidget(QtGui.QLabel, generic_widget.GenericWidget):
  def __init__(self):
    QtGui.QLabel.__init__(self)
    generic_widget.GenericWidget.__init__(self)

  def init(self):
    self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

  def loadXMLConfiguration(self, element):
    super(PageTitleWidget, self).loadXMLConfiguration(self, element)
    font = self.font()
    font.setPointSize(self.fontSize)
    self.setFont(font)
    self.setStyleSheet("font-weight: " + self.fontWeight + "; color: " + self.fontColor)
    
  def loadXMLSpecificElement(self, element):
    print("NOTHING TO DO")
    
  def paintEvent(self, event):
    qpainter = QtGui.QPainter(self)
    qpainter.drawPixmap(QtCore.QPoint(0,0), QtGui.QPixmap(self.bgImage))
    super(PageTitleWidget, self).paintEvent(event)
    