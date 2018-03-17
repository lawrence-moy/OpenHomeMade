from PySide import QtGui 
from PySide import QtCore

class ElectricControlWidget(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.gridLayout       = QtGui.QGridLayout()

    self.relayStateLabel = QtGui.QLabel("Etat du relais :")
    self.tcStateLabel    = QtGui.QLabel("Etat du TC :")
    self.relayState      = QtGui.QLabel("-")
    self.tcState         = QtGui.QLabel("-")

    self.labelFontSize    = 13
    self.valueFontSize    = 13
    
  def init(self):
    self.setupGUI()
    self.placeWidgets()
    
  def setupGUI(self):
    self.setLayout(self.gridLayout)
    
    labelTitleFont = QtGui.QFont(self.relayStateLabel.font())
    labelTitleFont.setPointSize(self.labelFontSize)
    valueFont = QtGui.QFont(self.relayState.font())
    valueFont.setPointSize(self.valueFontSize)
    
    self.relayStateLabel.setFont(labelTitleFont)
    self.relayStateLabel.setStyleSheet("font-weight: bold; color: black")
    self.tcStateLabel.setFont(labelTitleFont)
    self.tcStateLabel.setStyleSheet("font-weight: bold; color: black")

    self.relayState.setFont(valueFont)
    self.relayState.setStyleSheet("font-weight: bold; color: black")
    self.tcState.setFont(valueFont)
    self.tcState.setStyleSheet("font-weight: bold; color: black")

  def placeWidgets(self):
    self.gridLayout.addWidget(self.relayStateLabel, 0, 0)
    self.gridLayout.addWidget(self.tcStateLabel, 1, 0)
    
    self.gridLayout.addWidget(self.relayState,      0, 1)
    self.gridLayout.addWidget(self.tcState,   1, 1)
    
  def paintEvent(self, event):
    p = QtGui.QPainter(self)
    p.drawRoundedRect(0, 5, self.width()-5, self.height()-7, 3, 3)
      