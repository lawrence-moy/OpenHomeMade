from PySide import QtGui 
from PySide import QtCore
from PySide import QtXml
import auto_control_manager
import general_config_manager
import data_retrieving_manager
import http_handler
import electrical_counter_widget
import temperature_widget
import delay_widget
import electric_control_widget
import page

class CumulusManager(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.labelTitle       = QtGui.QLabel("Water-heater Manager", self)
    self.titleFontSize    = 30

    self.labelCurrentTime    = QtGui.QLabel("00:00:00", self)
    self.forceOnButton       = QtGui.QPushButton("Force ON")
    self.forceOffButton      = QtGui.QPushButton("Force OFF")
    self.configAutoButton    = QtGui.QPushButton("Timetable")
    self.configGeneralButton = QtGui.QPushButton("General")
    self.configNetworkButton = QtGui.QPushButton("Network")
    
    self.navRightButton = QtGui.QPushButton(u"\u25b6", self)
    self.navLeftButton  = QtGui.QPushButton(u"\u25c0", self)

    self.httpHandler           = http_handler.HTTPHandler()
    self.autoControlManager    = auto_control_manager.AutoControlManager(self)
    self.generalConfigManager  = general_config_manager.GeneralConfigManager(self)
    self.dataRetrievingManager = data_retrieving_manager.DataRetrievingManager(self)

    self.electricalCounterWidget = electrical_counter_widget.ElectricalCounterWidget()
    #self.temperatureWidget       = temperature_widget.TemperatureWidget()
    self.delayWidget             = delay_widget.DelayWidget()
    self.electricControlWidget   = electric_control_widget.ElectricControlWidget()

    self.pagesList = []
    
  def init(self):
    self.generalConfigManager.init()
    
    self.electricalCounterWidget.init()
    #self.temperatureWidget.init()
    self.delayWidget.init()
    self.electricControlWidget.init()
    
    self.initPages()
    
    self.loadXMLConfiguration()
    self.setupGUI()
    self.placeWidgets()
    
    self.autoControlManager.init()
    self.dataRetrievingManager.init()
    
  def initPages(self):
    configPage = page.Page(self, "Configuration")
    #configPage.init()
    #configPage.addWidget(self.forceOnButton,           0, 0, 1, 1)
    #configPage.addWidget(self.forceOffButton,          0, 1, 1, 1)
    #configPage.addWidget(self.configAutoButton,        1, 0, 1, 1)
    #configPage.addWidget(self.configGeneralButton,     1, 1, 1, 1)
    #configPage.addWidget(self.configNetworkButton,     2, 0, 1, 1)

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
    mainNode = docElem.firstChild()
    while not mainNode.isNull():
      element = mainNode.toElement()
      if not element.isNull():
        if "Network" == element.tagName():
          subNetworkNode = element.firstChild()
          while not subNetworkNode.isNull():
            subElement = subNetworkNode.toElement()
            if not subElement.isNull():
              if "Commands" == subElement.tagName():
                self.httpHandler.parseXMLParameters(subElement)
              elif "DataRetrieving" == subElement.tagName():
                self.dataRetrievingManager.parseXMLParameters(subElement)
            subNetworkNode = subNetworkNode.nextSibling()
        elif ("AutoControlParameters" == element.tagName()):
          self.autoControlManager.parseXMLParameters(element)
        elif ("Pages" == element.tagName()):
          self.loadPages(element)
      mainNode = mainNode.nextSibling()
      
  def loadPages(self, element):
    self.pagesList = []
    pageNode = element.firstChild()
    while not pageNode.isNull():
      pageElement = pageNode.toElement()
      if not pageElement.isNull():
        if "Page" == pageElement.tagName():
          title   = pageElement.attribute("title", "")
          newPage = page.Page(self, title)
          newPage.loadXMLConfiguration(pageElement)
          self.pagesList.append(newPage)
      pageNode = pageNode.nextSibling()

    self.currentPageIndex = 0
    self.pagesList[self.currentPageIndex].show()
      
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
    labelTitleFont = QtGui.QFont(self.labelTitle.font())
    labelTitleFont.setPointSize(self.titleFontSize)
    self.labelTitle.setFont(labelTitleFont)
    self.labelTitle.setStyleSheet("font-weight: bold; color: blue")
    
    valueFont = QtGui.QFont(self.labelCurrentTime.font())
    valueFont.setPointSize(self.titleFontSize)
    self.labelCurrentTime.setFont(valueFont)
    self.labelCurrentTime.setAlignment(QtCore.Qt.AlignCenter)
    self.labelCurrentTime.setStyleSheet("font-weight: bold; color: blue")
                               
    self.configureButton(self.forceOnButton, 
                         self.forceOnCommand)                         
    self.configureButton(self.forceOffButton, 
                         self.forceOffCommand)                           
    self.configureButton(self.configAutoButton, 
                         self.openAutoCtrlCfgWindow)
    self.configureButton(self.configGeneralButton, 
                         self.openCfgGeneralWindow)
    self.configureButton(self.configNetworkButton, 
                         self.openCfgNetworkWindow)

    self.setFixedSize(QtCore.QSize(800, 480))
    
  def configureButton(self, button, callback):
    buttonFont = QtGui.QFont(button.font())
    buttonFont.setPointSize(30)
    button.setFont(buttonFont)
    button.setFixedSize(300, 100)
    QtCore.QObject.connect(button, 
                           QtCore.SIGNAL("clicked()"), 
                           callback)
                           
  def openCfgGeneralWindow(self):
    self.generalConfigManager.show()
    
  def openCfgNetworkWindow(self):
    pass
    
  def getHTTPHandler(self):
    return self.httpHandler
    
  def getDataRetrievingManager(self):
    return self.dataRetrievingManager
  
  def openAutoCtrlCfgWindow(self):
    self.autoControlManager.show()
  
  def placeWidgets(self):
    self.labelTitle.move(0, 0)
    self.labelCurrentTime.move(600, 0)
    
    self.navLeftButton.setFixedSize(45, 400)
    arrowFont = QtGui.QFont(self.navLeftButton.font())
    arrowFont.setPointSize(50)
    self.navLeftButton.setFont(arrowFont)
    QtCore.QObject.connect(self.navLeftButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.previousPage)
    self.navLeftButton.move(5, 50)

    self.navRightButton.setFixedSize(45, 400)
    arrowFont = QtGui.QFont(self.navRightButton.font())
    arrowFont.setPointSize(50)
    self.navRightButton.setFont(arrowFont)
    QtCore.QObject.connect(self.navRightButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.nextPage)
    self.navRightButton.move(750, 50)

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

  def closeEvent(self, event):
    self.dataRetrievingManager.finish()
    event.accept()
    
app = QtGui.QApplication([])

cumulusManager = CumulusManager()
cumulusManager.init()
cumulusManager.show()

app.exec_()