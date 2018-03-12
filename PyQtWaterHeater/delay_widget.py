from PySide import QtGui 
from PySide import QtCore
from PySide import QtXml

class DelayWidget(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.gridLayout       = QtGui.QGridLayout()

    self.autoStateLabel   = QtGui.QLabel("Allumage auto :")
    self.delayOnLabel     = QtGui.QLabel("Allumage dans :")
    self.delayOffLabel    = QtGui.QLabel("Arret dans  :")
    self.autoState        = QtGui.QLabel("-")
    self.delayOn          = QtGui.QLabel("-")
    self.delayOff         = QtGui.QLabel("-")
    
    self.labelFontSize    = 15
    self.valueFontSize    = 15
    
  def init(self):
    self.setupGUI()
    self.placeWidgets()
    
  def setupGUI(self):
    self.setLayout(self.gridLayout)

    labelTitleFont = QtGui.QFont(self.autoStateLabel.font())
    labelTitleFont.setPointSize(self.labelFontSize)
    valueFont = QtGui.QFont(self.autoState.font())
    valueFont.setPointSize(self.valueFontSize)
  
    self.autoStateLabel.setFont(labelTitleFont)
    self.autoStateLabel.setStyleSheet("font-weight: bold; color: black")
    self.delayOnLabel.setFont(labelTitleFont)
    self.delayOnLabel.setStyleSheet("font-weight: bold; color: black")
    self.delayOffLabel.setFont(labelTitleFont)
    self.delayOffLabel.setStyleSheet("font-weight: bold; color: black")

    self.autoState.setFont(valueFont)
    self.autoState.setStyleSheet("font-weight: bold; color: black")
    self.delayOn.setFont(valueFont)
    self.delayOn.setStyleSheet("font-weight: bold; color: black")
    self.delayOff.setFont(valueFont)
    self.delayOff.setStyleSheet("font-weight: bold; color: black")

  def placeWidgets(self):
    self.gridLayout.addWidget(self.autoStateLabel, 0, 0)
    self.gridLayout.addWidget(self.delayOnLabel,   1, 0)
    self.gridLayout.addWidget(self.delayOffLabel,  2, 0)
    
    self.gridLayout.addWidget(self.autoState,      0, 1)
    self.gridLayout.addWidget(self.delayOn,        1, 1)
    self.gridLayout.addWidget(self.delayOff,       2, 1)

  def paintEvent(self, event):
    p = QtGui.QPainter(self)
    p.drawRoundedRect(0, 5, self.width()-5, self.height()-7, 3, 3)
