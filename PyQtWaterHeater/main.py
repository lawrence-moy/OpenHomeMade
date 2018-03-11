from PySide import QtGui 
from PySide import QtCore
from PySide import QtXml
import auto_param_window
import network_handler
import request_manager

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
    self.forceOnButton    = QtGui.QPushButton("Forcer \n allumage")
    self.forceOffButton   = QtGui.QPushButton("Forcer \n arret")
    self.configAutoButton = QtGui.QPushButton("Programmation \n horaire")

    self.autoCtrlParamWin = auto_param_window.AutoControlParamWindow(self)
    self.networkHandler   = network_handler.NetworkHandler()
    self.requestManager   = request_manager.RequestManager(self)

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
    self.requestManager.init()

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
          self.networkHandler.parseXMLParameters(element)
        elif ("OnOffParameters" == element.tagName()):
          self.autoCtrlParamWin.parseXMLParameters(element)
      n = n.nextSibling()
      
  def saveXMLConfiguration(self):
    doc = QtXml.QDomDocument("Configuration")
    rootNode = doc.createElement("Config")

    networkNode = self.networkHandler.getXMLConfiguration(doc)
    rootNode.appendChild(networkNode)
    onOffParamNode = self.autoCtrlParamWin.getXMLConfiguration(doc)
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

  def getAutoControlParametersHandler(self):
    return self.autoCtrlParamWin
    
  def getNetworkHandler(self):
    return self.networkHandler  
  
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
    self.requestManager.processRequest()
      
  def applyTimeTableParameters(self):
    self.saveXMLConfiguration()
    
  def forceOnCommand(self):
    self.requestManager.switchOnCommand()

  def forceOffCommand(self):
    self.requestManager.switchOffCommand()

app = QtGui.QApplication([])

cumulusManager = CumulusManager()
cumulusManager.init()
cumulusManager.show()
#cumulusManager.showFullScreen()

app.exec_()