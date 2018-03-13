from PySide import QtGui 
from PySide import QtCore
from PySide import QtXml

class ElectricalCounterWidget(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.gridLayout       = QtGui.QGridLayout()

    self.totalPowerLabel  = QtGui.QLabel("Puissance cumulee :")
    self.powerLabel       = QtGui.QLabel("Puissance actuelle :")
    self.voltageLabel     = QtGui.QLabel("Voltage :")
    self.currentLabel     = QtGui.QLabel("Amperage :")
    self.totalPower       = QtGui.QLabel("-")
    self.power            = QtGui.QLabel("-")
    self.voltage          = QtGui.QLabel("-")
    self.current          = QtGui.QLabel("-")
    
    self.labelFontSize    = 13
    self.valueFontSize    = 13
    
  def init(self):
    self.setupGUI()
    self.placeWidgets()
    
  def setupGUI(self):
    self.setLayout(self.gridLayout)
    #self.setFixedSize(QtCore.QSize(200, 100))
    
    labelTitleFont = QtGui.QFont(self.totalPowerLabel.font())
    labelTitleFont.setPointSize(self.labelFontSize)
    valueFont = QtGui.QFont(self.totalPower.font())
    valueFont.setPointSize(self.valueFontSize)
  
    self.totalPowerLabel.setFont(labelTitleFont)
    self.totalPowerLabel.setStyleSheet("font-weight: bold; color: black")
    self.powerLabel.setFont(labelTitleFont)
    self.powerLabel.setStyleSheet("font-weight: bold; color: black")
    self.voltageLabel.setFont(labelTitleFont)
    self.voltageLabel.setStyleSheet("font-weight: bold; color: black")
    self.currentLabel.setFont(labelTitleFont)
    self.currentLabel.setStyleSheet("font-weight: bold; color: black")

    self.totalPower.setFont(valueFont)
    self.totalPower.setStyleSheet("font-weight: bold; color: black")
    self.power.setFont(valueFont)
    self.power.setStyleSheet("font-weight: bold; color: black")
    self.voltage.setFont(valueFont)
    self.voltage.setStyleSheet("font-weight: bold; color: black")
    self.current.setFont(valueFont)
    self.current.setStyleSheet("font-weight: bold; color: black")
    
  def placeWidgets(self):
    self.gridLayout.addWidget(self.totalPowerLabel, 0, 0)
    self.gridLayout.addWidget(self.powerLabel,      1, 0)
    self.gridLayout.addWidget(self.voltageLabel,    2, 0)
    self.gridLayout.addWidget(self.currentLabel,    3, 0)
    
    self.gridLayout.addWidget(self.totalPower,      0, 1)
    self.gridLayout.addWidget(self.power,           1, 1)
    self.gridLayout.addWidget(self.voltage,         2, 1)
    self.gridLayout.addWidget(self.current,         3, 1)
    
  def paintEvent(self, event):
    p = QtGui.QPainter(self)
    p.drawRoundedRect(0, 5, self.width()-5, self.height()-7, 3, 3)
