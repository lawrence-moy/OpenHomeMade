from PySide import QtGui

class Page(QtGui.QWidget):
  def __init__(self, title):
    QtGui.QWidget.__init__(self)
    self.title      = title
    self.gridLayout = QtGui.QGridLayout()
    
  def init(self):
    self.setLayout(self.gridLayout)
    
  def addWidget(self, widget, row, column, rowSpan, columnSpan):
    self.gridLayout.addWidget(widget, row, column, rowSpan, columnSpan)

  def getTitle(self):
    return self.title
    
