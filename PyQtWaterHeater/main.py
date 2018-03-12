from PySide import QtGui 
from PySide import QtCore
from PySide import QtXml
import auto_param_window
import network_handler
import request_manager
import electrical_counter_widget
import temperature_widget
import delay_widget

class CumulusManager(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.gridLayout       = QtGui.QGridLayout()
    self.logoPixmap       = QtGui.QPixmap("cumulus.png")
    self.waterHeaterImg   = QtGui.QLabel(self)
    self.labelTitle       = QtGui.QLabel("Water-heater Manager", self)

    self.titleFontSize    = 30

    self.labelCurrentTime = QtGui.QLabel("00:00:00")
    self.forceOnButton    = QtGui.QPushButton("Force ON")
    self.forceOffButton   = QtGui.QPushButton("Force OFF")
    self.configAutoButton = QtGui.QPushButton("Config")

    self.autoCtrlParamWin = auto_param_window.AutoControlParamWindow(self)
    self.networkHandler   = network_handler.NetworkHandler()
    self.requestManager   = request_manager.RequestManager(self)

    self.electricalCounterWidget = electrical_counter_widget.ElectricalCounterWidget()
    self.temperatureWidget       = temperature_widget.TemperatureWidget()
    self.delayWidget             = delay_widget.DelayWidget()
    
    self.relayStateLabel  = QtGui.QLabel("Etat du relais :")
    self.tcStateLabel     = QtGui.QLabel("Etat du TC :")
    
  def init(self):
    self.autoCtrlParamWin.init()
    self.electricalCounterWidget.init()
    self.temperatureWidget.init()
    self.delayWidget.init()
    
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
    self.waterHeaterImg.setPixmap(self.logoPixmap)

    labelTitleFont = QtGui.QFont(self.labelTitle.font())
    labelTitleFont.setPointSize(self.titleFontSize)
    self.labelTitle.setFont(labelTitleFont)
    self.labelTitle.setStyleSheet("font-weight: bold; color: blue")
    
    valueFont = QtGui.QFont(self.labelCurrentTime.font())
    valueFont.setPointSize(self.titleFontSize)
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
    self.gridLayout.addWidget(self.labelTitle,        0, 0, 1, 2)
    self.gridLayout.addWidget(self.labelCurrentTime,  0, 2, 1, 1, QtCore.Qt.AlignRight)
    
    self.gridLayout.addWidget(self.temperatureWidget, 1, 0, 1, 1)

    self.gridLayout.addWidget(self.waterHeaterImg,    1, 1, 3, 1, QtCore.Qt.AlignCenter)
    
    self.gridLayout.addWidget(self.delayWidget,             1, 2, 1, 1)
    self.gridLayout.addWidget(self.electricalCounterWidget, 2, 2, 1, 1)

    self.gridLayout.addWidget(self.forceOnButton,    4, 0, 1, 1)
    self.gridLayout.addWidget(self.forceOffButton,   4, 1, 1, 1)
    self.gridLayout.addWidget(self.configAutoButton, 4, 2, 1, 1)

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