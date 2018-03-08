from PySide import QtGui 
from PySide import QtCore
from PySide import QtNetwork
from PySide import QtXml
import auto_param_window

class CumulusManager(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.gridLayout       = QtGui.QGridLayout()
    self.logoPixmap       = QtGui.QPixmap("cumulus.png")
    self.logo             = QtGui.QLabel()
    self.labelTitle       = QtGui.QLabel("Controle chauffe-eau")

    self.titleFontSize    = 30
    self.labelFontSize    = 25
    self.valueFontSize    = 30

    self.labelCurrentTime = QtGui.QLabel("00:00:00")
    self.validateButton   = QtGui.QPushButton("Valider")
    self.forceOnButton    = QtGui.QPushButton("Forcer \n allumage")
    self.forceOffButton   = QtGui.QPushButton("Forcer \n arret")
    self.configAutoButton = QtGui.QPushButton("Programmation \n horaire")
    self.offTime          = None
    self.onRequestParam   = (None, None)
    self.offRequestParam  = (None, None)
    self.autoCtrlParamWin = auto_param_window.AutoControlParamWindow(self)
    
    self.comStateCumulusLabel = QtGui.QLabel("Etat COM Cumulus :")
    self.comStateCounterLabel = QtGui.QLabel("Etat COM Compteur :")
    self.comStatePylierLabel  = QtGui.QLabel("Etat COM Pylier :")
    
    self.totalPowerLabel  = QtGui.QLabel("Puissance cumulee :")
    self.powerLabel       = QtGui.QLabel("Puissance actuelle :")
    
    self.relayStateLabel  = QtGui.QLabel("Etat du relais :")
    self.tcStateLabel     = QtGui.QLabel("Etat du TC :")
    
    self.waterTempLabel   = QtGui.QLabel("Temperature eau :")
    self.ambiaTempLabel   = QtGui.QLabel("Temperature ambiante :")
    
    self.autoStateLabel   = QtGui.QLabel("Allumage auto :")
    self.delayOnLabel     = QtGui.QLabel("Allumage dans :")
    self.delayOffLabel    = QtGui.QLabel("Arret dans  :")
    
  def init(self):
    self.autoCtrlParamWin.setupGUI()
    self.autoCtrlParamWin.placeWidgets()
    self.loadXMLConfiguration()
    self.setupGUI()
    self.placeWidgets()

  def loadXMLConfiguration(self):
    doc = QtXml.QDomDocument("configuration")
    file = QtCore.QFile("config.xml")
    if not file.open(QtCore.QIODevice.ReadOnly):
      return
    if not doc.setContent(file):
      file.close()
      return
    file.close()
    docElem = doc.documentElement()
    n = docElem.firstChild()
    while not n.isNull():
      element = n.toElement()
      if not element.isNull():
        if "Network" == element.tagName():
          self.parseXMLNetworkParameters(element)
        elif ("OnOffParameters" == element.tagName()):
          self.parseXMLOnOffParameters(element)
      n = n.nextSibling()
      
  def parseXMLNetworkParameters(self, element):
    subNetworkNode = element.firstChild()
    while not subNetworkNode.isNull():
      subNetworkElement = subNetworkNode.toElement()
      if not subNetworkElement.isNull():
        if "OnRequest" == subNetworkElement.tagName():
           urlOn = subNetworkElement.attribute("url", "")
           bodyOn = subNetworkElement.attribute("body", "")
           self.onRequestParam = (urlOn, bodyOn)
        elif "OffRequest" == subNetworkElement.tagName():
           urlOff  = subNetworkElement.attribute("url", "")
           bodyOff = subNetworkElement.attribute("body", "")
           self.offRequestParam = (urlOff, bodyOff)
      subNetworkNode = subNetworkNode.nextSibling()
  
  def parseXMLOnOffParameters(self, element):
    hour = element.attribute("hour", "00:00")
    onTime = QtCore.QDateTime.currentDateTime()
    onTime.setTime(QtCore.QTime.fromString(hour, "hh:mm"))
    print("OnTime: ", onTime.toString())
    self.autoCtrlParamWin.setSwitchOnTime(onTime)
    
    duration = element.attribute("duration", "03:00")
    print("Duration: ", duration)
    self.durationTime = QtCore.QTime.fromString(duration, "hh:mm")
    self.autoCtrlParamWin.setDurationTime(self.durationTime)
      
  def saveXMLConfiguration(self):
    doc = QtXml.QDomDocument("Configuration")
    rootNode = doc.createElement("Config")

    networkNode    = doc.createElement("Network")
    onRequestNode  = doc.createElement("OnRequest")
    onRequestNode.setAttribute("url",  self.onRequestParam[0])
    onRequestNode.setAttribute("body", self.onRequestParam[1])
    offRequestNode = doc.createElement("OffRequest")
    offRequestNode.setAttribute("url",  self.offRequestParam[0])
    offRequestNode.setAttribute("body", self.offRequestParam[1])
    networkNode.appendChild(onRequestNode)
    networkNode.appendChild(offRequestNode)
    rootNode.appendChild(networkNode)
    
    onOffParamNode = doc.createElement("OnOffParameters")
    onOffParamNode.setAttribute("hour", self.startTime.time().toString("hh:mm"))
    onOffParamNode.setAttribute("duration", self.duration.time().toString("hh:mm"))
    rootNode.appendChild(onOffParamNode)
    
    doc.appendChild(rootNode)
    
    outFile = QtCore.QFile("config.xml")
    if not outFile.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Text ):
      print("Failed to open file for writing.")
      return
  
    stream = QtCore.QTextStream(outFile)
    stream << doc.toString()
    outFile.close()
    
  def setupGUI(self):
    self.logo.setPixmap(self.logoPixmap)

    labelTitleFont  = QtGui.QFont(self.labelTitle.font())
    labelTitleFont.setPointSize(self.titleFontSize)
    self.labelTitle.setFont(labelTitleFont)
    self.labelTitle.setStyleSheet("font-weight: bold; color: blue")
    
    valueFont = QtGui.QFont(self.labelCurrentTime.font())
    valueFont.setPointSize(self.valueFontSize)
    self.labelCurrentTime.setFont(valueFont)
    self.labelCurrentTime.setAlignment(QtCore.Qt.AlignCenter)
    self.labelCurrentTime.setStyleSheet("font-weight: bold; color: blue")
    
    buttonFont = QtGui.QFont(self.forceOnButton.font())
    buttonFont.setPointSize(30)
    self.forceOnButton.setFont(buttonFont)
    QtCore.QObject.connect(self.forceOnButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.forceOnCommand)

    buttonFont = QtGui.QFont(self.forceOffButton.font())
    buttonFont.setPointSize(30)
    self.forceOffButton.setFont(buttonFont)
    QtCore.QObject.connect(self.forceOffButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.forceOffCommand)
                         
    buttonFont = QtGui.QFont(self.configAutoButton.font())
    buttonFont.setPointSize(30)
    self.configAutoButton.setFont(buttonFont)
    QtCore.QObject.connect(self.configAutoButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.openAutoCtrlCfgWindow)

    self.setLayout(self.gridLayout)
    self.setFixedSize(QtCore.QSize(800, 480))

  def openAutoCtrlCfgWindow(self):
    self.autoCtrlParamWin.show()
  
  def placeWidgets(self):
    self.gridLayout.addWidget(self.labelTitle,       0, 0, 1, 2)
    self.gridLayout.addWidget(self.labelCurrentTime, 0, 2, 1, 1, QtCore.Qt.AlignRight)
    
    self.gridLayout.addWidget(self.forceOnButton,    1, 0, 1, 1)
    self.gridLayout.addWidget(self.forceOffButton,   2, 0, 1, 1)

    self.gridLayout.addWidget(self.logo,             1, 1, 4, 1, QtCore.Qt.AlignCenter)
    
    self.gridLayout.addWidget(self.configAutoButton, 1, 2)

    self.updateTimeTimer = QtCore.QTimer()
    QtCore.QObject.connect(self.updateTimeTimer, QtCore.SIGNAL("timeout()"), self.update)
    self.updateTimeTimer.start(1000)
    
  def update(self):
    self.labelCurrentTime.setText(QtCore.QDateTime.currentDateTime().toString("hh:mm:ss"))
    onTime  = self.autoCtrlParamWin.getSwitchOnTime()
    offTime = self.autoCtrlParamWin.getSwitchOffTime()
    if (QtCore.QDateTime.currentDateTime().__ge__(onTime) ):
      self.forceOnCommand()
      self.autoCtrlParamWin.setSwitchOnTime(onTime.addDays(1))
      print("ON !!!!")
    elif (QtCore.QDateTime.currentDateTime().__ge__(offTime) ):
      self.forceOffCommand()
      self.autoCtrlParamWin.setSwitchOffTime(offTime.addDays(1))
      print("OFF !!!")
      
  def applyParameters(self):
    self.saveXMLConfiguration()
    
  def sendRequest(self, urlPath, data):
    manager = QtNetwork.QNetworkAccessManager(self)
    manager.finished[QtNetwork.QNetworkReply].connect(self.replyFinished)
    url = QtCore.QUrl(urlPath)
    request = QtNetwork.QNetworkRequest(url)
    request.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json")
    print("POST:", data)
    manager.post(request, data)
    
  def replyFinished(self, reply):
    print(reply.readAll())
    
  def forceOnCommand(self):
    self.sendRequest(self.onRequestParam[0], self.onRequestParam[1])

  def forceOffCommand(self):
    self.sendRequest(self.offRequestParam[0], self.offRequestParam[1])
    
  def generateCommand(self, moduleId, command, value):
    return '{"ref":' + str(moduleId) + ', "' + command + '":' + str(value) + '}'
  
app = QtGui.QApplication([])

cumulusManager = CumulusManager()
cumulusManager.init()
cumulusManager.show()
#cumulusManager.showFullScreen()

app.exec_()