from PySide import QtGui 
from PySide import QtCore
import generic_widget

class ImageWidget(QtGui.QLabel, generic_widget.GenericWidget):
  def __init__(self):
    QtGui.QLabel.__init__(self)
    generic_widget.GenericWidget.__init__(self)

  def loadXMLConfiguration(self, element):
    super(ImageWidget, self).loadXMLConfiguration(element)
    path   = element.attribute("path", "")
    pixmap = QtGui.QPixmap(path)
    self.setPixmap(pixmap)
    
  def paintEvent(self, event):
    super(ImageWidget, self).paintEvent(event)
    #p = QtGui.QPainter(self)
    #p.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
    
