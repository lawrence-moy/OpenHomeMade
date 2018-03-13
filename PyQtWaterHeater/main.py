from PySide import QtGui 
from PySide import QtCore
from PySide import QtXml
import auto_control_manager
import http_handler
#import request_manager
import electrical_counter_widget
import temperature_widget
import delay_widget
import electric_control_widget
import page

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
    self.configAutoButton = QtGui.QPushButton("Configure")
    
    self.navRightButton = QtGui.QPushButton(u"\u25b6")
    self.navLeftButton  = QtGui.QPushButton(u"\u25c0")

    self.httpHandler        = http_handler.HTTPHandler()
    self.autoControlManager = auto_control_manager.AutoControlManager(self)

    self.electricalCounterWidget = electrical_counter_widget.ElectricalCounterWidget()
    self.temperatureWidget       = temperature_widget.TemperatureWidget()
    self.delayWidget             = delay_widget.DelayWidget()
    self.electricControlWidget   = electric_control_widget.ElectricControlWidget()
    
  def init(self):
    self.autoControlManager.init()
    self.electricalCounterWidget.init()
    self.temperatureWidget.init()
    self.delayWidget.init()
    self.electricControlWidget.init()
    
    self.initPages()
    
    self.loadXMLConfiguration()
    self.setupGUI()
    self.placeWidgets()
    self.autoControlManager.init()
    
  def initPages(self):
    mainPage = page.Page("General view")
    mainPage.init()
    mainPage.addWidget(self.temperatureWidget,       1, 1, 1, 1)
    mainPage.addWidget(self.delayWidget,             2, 1, 1, 1)
    mainPage.addWidget(self.waterHeaterImg,          1, 2, 3, 1)#, QtCore.Qt.AlignCenter)
    mainPage.addWidget(self.electricalCounterWidget, 1, 3, 1, 1)
    
    historyPage = page.Page("History")
    historyPage.init()
    
    self.pagesList = []
    self.pagesList.append(mainPage)
    self.pagesList.append(historyPage)
    
    self.currentPageIndex = 0 

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
          self.httpHandler.parseXMLParameters(element)
        elif ("AutoControlParameters" == element.tagName()):
          self.autoControlManager.parseXMLParameters(element)
      n = n.nextSibling()
      
  def saveXMLConfiguration(self):
    doc = QtXml.QDomDocument("Configuration")
    rootNode = doc.createElement("Config")

    networkNode = self.httpHandler.getXMLConfiguration(doc)
    rootNode.appendChild(networkNode)
    onOffParamNode = self.autoControlManager.getXMLConfiguration(doc)
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
    
  def getHTTPHandler(self):
    return self.httpHandler
  
  def openAutoCtrlCfgWindow(self):
    self.autoControlManager.show()
  
  def placeWidgets(self):
    self.gridLayout.addWidget(self.labelTitle,              0, 0, 1, 3)
    self.gridLayout.addWidget(self.labelCurrentTime,        0, 3, 1, 2, QtCore.Qt.AlignRight)
    
    self.navLeftButton.setFixedSize(45, 340)
    arrowFont = QtGui.QFont(self.navLeftButton.font())
    arrowFont.setPointSize(50)
    self.navLeftButton.setFont(arrowFont)
    self.gridLayout.addWidget(self.navLeftButton,           1, 0, 3, 1)
    QtCore.QObject.connect(self.navLeftButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.previousPage)

    self.gridLayout.addWidget(self.pagesList[0],          1, 1, 3, 3, QtCore.Qt.AlignCenter)
    self.gridLayout.addWidget(self.pagesList[1],          1, 1, 3, 3, QtCore.Qt.AlignCenter)

    self.navRightButton.setFixedSize(45, 340)
    arrowFont = QtGui.QFont(self.navRightButton.font())
    arrowFont.setPointSize(50)
    self.navRightButton.setFont(arrowFont)
    self.gridLayout.addWidget(self.navRightButton,          1, 4, 3, 1)
    QtCore.QObject.connect(self.navRightButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.nextPage)

    self.gridLayout.addWidget(self.forceOnButton,           4, 1, 1, 1)
    self.gridLayout.addWidget(self.forceOffButton,          4, 2, 1, 1)
    self.gridLayout.addWidget(self.configAutoButton,        4, 3, 1, 1)

    self.updateTimeTimer = QtCore.QTimer()
    QtCore.QObject.connect(self.updateTimeTimer, QtCore.SIGNAL("timeout()"), self.update)
    self.updateTimeTimer.start(1000)
    
  def update(self):
    self.labelCurrentTime.setText(QtCore.QDateTime.currentDateTime().toString("hh:mm:ss"))
    self.autoControlManager.processRequest()
    
  def forceOnCommand(self):
    self.autoControlManager.switchOnCommand()

  def forceOffCommand(self):
    self.autoControlManager.switchOffCommand()
    
  def nextPage(self):
    if self.currentPageIndex >= len(self.pagesList)-1:
        return
    self.pagesList[self.currentPageIndex].hide()
    self.currentPageIndex += 1
    self.pagesList[self.currentPageIndex].show()
    self.labelTitle.setText(self.pagesList[self.currentPageIndex].getTitle())
    
  def previousPage(self):
    if self.currentPageIndex <= 0:
        return
    self.pagesList[self.currentPageIndex].hide()
    self.currentPageIndex -= 1
    self.pagesList[self.currentPageIndex].show()
    self.labelTitle.setText(self.pagesList[self.currentPageIndex].getTitle())

app = QtGui.QApplication([])

cumulusManager = CumulusManager()
cumulusManager.init()
cumulusManager.show()
#cumulusManager.showFullScreen()

app.exec_()