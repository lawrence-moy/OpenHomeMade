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
    super(LabelWidget, self).loadXMLConfiguration(self, element)
    font = self.font()
    font.setPointSize(self.fontSize)
    self.setFont(font)
    self.setStyleSheet("font-weight: " + self.fontWeight + "; color: " + self.fontColor)
    
  def loadXMLSpecificElement(self, element):
    if "Text" == element.tagName():
      self.setText(element.attribute("value", ""))
      
  def paintEvent(self, event):
    p = QtGui.QPainter(self)
    p.drawRoundedRect(0, 0, self.width()+1, self.height()+1, 3, 3)
    super(LabelWidget, self).paintEvent(event)
    