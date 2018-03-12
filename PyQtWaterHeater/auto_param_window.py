from PySide import QtGui 
from PySide import QtCore
from PySide import QtNetwork
from PySide import QtXml

class AutoControlParamWindow(QtGui.QDialog):
  def __init__(self, _parent):
    QtGui.QDialog.__init__(self, parent=_parent)
    self.gridLayout       = QtGui.QGridLayout()
    self.labelStartTime   = QtGui.QLabel("Horaire d'allumage")
    self.titleFontSize    = 30
    self.labelFontSize    = 25
    self.valueFontSize    = 30
    self.startTime        = QtGui.QTimeEdit()
    self.labelDuration    = QtGui.QLabel("Duree")
    self.duration         = QtGui.QTimeEdit()
    self.durationTime     = None
    self.validateButton   = QtGui.QPushButton("Valider")
    self.onTime           = None
    self.offTime          = None
    
  def init(self):
    self.setupGUI()
    self.placeWidgets()
    
  def parseXMLParameters(self, element):
    hour = element.attribute("hour", "00:00")
    onTime = QtCore.QDateTime.currentDateTime()
    onTime.setTime(QtCore.QTime.fromString(hour, "hh:mm"))
    print("OnTime: ", onTime.toString())
    self.setSwitchOnTime(onTime)
    
    duration = element.attribute("duration", "03:00")
    print("Duration: ", duration)
    self.durationTime = QtCore.QTime.fromString(duration, "hh:mm")
    self.setDurationTime(self.durationTime)
    
  def getXMLConfiguration(self, doc):
    onOffParamNode = doc.createElement("OnOffParameters")
    onOffParamNode.setAttribute("hour", self.getSwitchOnTime().time().toString("hh:mm"))
    onOffParamNode.setAttribute("duration", self.getDurationTime().toString("hh:mm"))
    return onOffParamNode
    
  def setupGUI(self):
    labelFont = QtGui.QFont(self.labelStartTime.font())
    labelFont.setPointSize(self.labelFontSize)
    self.labelStartTime.setFont(labelFont)
    
    self.startTime.setStyleSheet("QTimeEdit::up-button   { subcontrol-position: left;  width: 40px; height: 40px; }"
                                 "QTimeEdit::down-button { subcontrol-position: right; width: 40px; height: 40px; }")
    valueFont = QtGui.QFont(self.startTime.font())
    valueFont.setPointSize(self.valueFontSize)
    self.startTime.setFont(valueFont)
    self.startTime.setAlignment(QtCore.Qt.AlignCenter)
    self.startTime.setDisplayFormat("hh:mm")
    self.startTime.setDateTime(self.onTime)

    self.labelDuration.setFont(labelFont)
    self.duration.setStyleSheet("QTimeEdit::up-button   { subcontrol-position: left;  width: 40px; height: 40px; }"
                                "QTimeEdit::down-button { subcontrol-position: right; width: 40px; height: 40px; }")
    self.duration.setFont(valueFont)
    self.duration.setAlignment(QtCore.Qt.AlignCenter)
    self.duration.setDisplayFormat("hh:mm")
    self.duration.setTime(self.durationTime)
    
    buttonFont = QtGui.QFont(self.validateButton.font())
    buttonFont.setPointSize(30)
    self.validateButton.setFont(buttonFont)
    self.validateButton.setIcon(QtGui.QIcon("ok.png"));
    self.validateButton.setIconSize(QtCore.QSize(50, 50));

    QtCore.QObject.connect(self.validateButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.applyParameters)
    
    self.setLayout(self.gridLayout)
    self.setFixedSize(QtCore.QSize(380, 380))

  def placeWidgets(self):
    self.gridLayout.addWidget(self.labelStartTime,   1, 2)
    self.gridLayout.addWidget(self.startTime,        2, 2)
    self.gridLayout.addWidget(self.labelDuration,    3, 2)
    self.gridLayout.addWidget(self.duration,         4, 2)
    self.gridLayout.addWidget(self.validateButton,   6, 2)
    
  def setSwitchOnTime(self, time):
    self.onTime = time
    self.startTime.setDateTime(self.onTime)
    
  def getSwitchOnTime(self):
    return self.onTime
    
  def setSwitchOffTime(self, time):
    self.offTime = time
    
  def getSwitchOffTime(self):
    return self.offTime
    
  def setDurationTime(self, time):
    self.durationTime = time
    self.duration.setTime(self.durationTime)
    self.processSwitchOffDateTime()
    
  def getDurationTime(self):
    return self.duration.time()
    
  def processSwitchOffDateTime(self):
    tempTime = QtCore.QDateTime(self.onTime)
    self.offTime = tempTime.addSecs((self.durationTime.hour() * 60 * 60) + \
                                     self.durationTime.minute() * 60)  
    
  def applyParameters(self):
    self.onTime = self.startTime.dateTime()
    self.processSwitchOffDateTime()
    self.hide()
    self.parent().applyTimeTableParameters()
      