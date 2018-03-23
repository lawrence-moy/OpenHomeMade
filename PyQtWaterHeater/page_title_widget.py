from PySide import QtGui 
from PySide import QtCore
import generic_widget

class PageTitleWidget(QtGui.QLabel, generic_widget.GenericWidget):
  def __init__(self):
    QtGui.QLabel.__init__(self)
    generic_widget.GenericWidget.__init__(self)
    self.bgImage = ""

  def init(self):
    self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

  def loadXMLConfiguration(self, element):
    super(PageTitleWidget, self).loadXMLConfiguration(element)
    font = self.font()
    font.setPointSize(int(element.attribute("fontSize", "12")))
    self.setFont(font)
    fontColor  = element.attribute("fontColor", "#000000")
    fontWeight = element.attribute("fontWeight", "normal")
    self.setStyleSheet("font-weight: " + fontWeight + "; color: " + fontColor)
    self.bgImage = element.attribute("bgImage", "")
    
  def paintEvent(self, event):
    qpainter = QtGui.QPainter(self)
    qpainter.drawPixmap(QtCore.QPoint(0,0), QtGui.QPixmap(self.bgImage))
    super(PageTitleWidget, self).paintEvent(event)
    