from PySide import QtGui 
from PySide import QtCore

class TemperatureWidget(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.gridLayout       = QtGui.QGridLayout()

    self.waterTempLabel   = QtGui.QLabel("Temperature eau :")
    self.ambiaTempLabel   = QtGui.QLabel("Temperature piece :")
    self.waterTemp        = QtGui.QLabel("-")
    self.ambianteTemp     = QtGui.QLabel("-")

    self.labelFontSize    = 13
    self.valueFontSize    = 13
    
  def init(self):
    self.setupGUI()
    self.placeWidgets()
    
  def setupGUI(self):
    self.setLayout(self.gridLayout)
    
    labelTitleFont = QtGui.QFont(self.waterTempLabel.font())
    labelTitleFont.setPointSize(self.labelFontSize)
    valueFont = QtGui.QFont(self.waterTemp.font())
    valueFont.setPointSize(self.valueFontSize)
    
    self.waterTempLabel.setFont(labelTitleFont)
    self.waterTempLabel.setStyleSheet("font-weight: bold; color: black")
    self.ambiaTempLabel.setFont(labelTitleFont)
    self.ambiaTempLabel.setStyleSheet("font-weight: bold; color: black")

    self.waterTemp.setFont(valueFont)
    self.waterTemp.setStyleSheet("font-weight: bold; color: black")
    self.ambianteTemp.setFont(valueFont)
    self.ambianteTemp.setStyleSheet("font-weight: bold; color: black")

  def placeWidgets(self):
    self.gridLayout.addWidget(self.waterTempLabel, 0, 0)
    self.gridLayout.addWidget(self.ambiaTempLabel, 1, 0)
    
    self.gridLayout.addWidget(self.waterTemp,      0, 1)
    self.gridLayout.addWidget(self.ambianteTemp,   1, 1)
    
  def paintEvent(self, event):
    p = QtGui.QPainter(self)
    p.drawRoundedRect(0, 5, self.width()-5, self.height()-7, 3, 3)
      