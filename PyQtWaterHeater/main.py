from PySide import QtGui 
from PySide import QtCore
from PySide import QtXml
import water_heater_module
import general_config_manager
import data_retrieving_manager
import http_handler
import page

class Versatyle(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.navRightButton        = QtGui.QPushButton(u"\u25b6", self)
    self.navLeftButton         = QtGui.QPushButton(u"\u25c0", self)
    self.httpHandler           = http_handler.HTTPHandler()
    self.waterHeaterModule     = water_heater_module.WaterHeaterModule(self)
    self.generalConfigManager  = general_config_manager.GeneralConfigManager(self)
    self.dataRetrievingManager = data_retrieving_manager.DataRetrievingManager(self)
    self.modulesDict           = {}
    self.pagesList             = []
    self.pageTitleConsumers    = []
    self.currentPageIndex      = 0
    
  def init(self):
    self.generalConfigManager.init()
    self.registerModule(self.generalConfigManager)
    
    self.waterHeaterModule.init()
    self.registerModule(self.waterHeaterModule)
    
    self.loadXMLConfiguration()
    self.setupGUI()
    self.placeWidgets()
    
    self.dataRetrievingManager.init()
    self.dataRetrievingManager.start()

  def loadXMLConfiguration(self):
    doc = QtXml.QDomDocument("configuration")
    file = QtCore.QFile("config/config.xml")
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
          self.waterHeaterModule.parseXMLParameters(element)
        elif ("Pages" == element.tagName()):
          self.loadPages(element)
      mainNode = mainNode.nextSibling()
      
  def registerModule(self, module):
    if None == self.modulesDict.get(module.getName()):
      self.modulesDict[module.getName()] = module
      
  def getModule(self, name):
    return self.modulesDict.get(name)
    
  def registerPageTitleConsumer(self, widget):
    self.pageTitleConsumers.append(widget)
      
  def loadPages(self, element):
    self.pagesList = []
    pageNode = element.firstChild()
    while not pageNode.isNull():
      pageElement = pageNode.toElement()
      if not pageElement.isNull():
        if "Page" == pageElement.tagName():
          newPage = page.Page(self)
          newPage.loadXMLConfiguration(pageElement)
          self.pagesList.append(newPage)
      pageNode = pageNode.nextSibling()
    self.processPageChanged()
    
  def saveXMLConfiguration(self):
    doc = QtXml.QDomDocument("Configuration")
    rootNode = doc.createElement("Config")

    networkNode = self.httpHandler.getXMLConfiguration(doc)
    rootNode.appendChild(networkNode)
    onOffParamNode = self.waterHeaterModule.getXMLConfiguration(doc)
    rootNode.appendChild(onOffParamNode)
    doc.appendChild(rootNode)
    
    outFile = QtCore.QFile("config/config.xml")
    if not outFile.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Text ):
      print("Failed to open file for writing.")
      return
    stream = QtCore.QTextStream(outFile)
    stream << doc.toString()
    outFile.close()
    
  def setupGUI(self):
    self.setFixedSize(QtCore.QSize(800, 480))
                           
  def openCfgGeneralWindow(self):
    self.generalConfigManager.show()
    
  def getHTTPHandler(self):
    return self.httpHandler
    
  def getDataRetrievingManager(self):
    return self.dataRetrievingManager
  
  def placeWidgets(self):
    self.navLeftButton.setFixedSize(45, 400)
    arrowFont = QtGui.QFont(self.navLeftButton.font())
    arrowFont.setPointSize(50)
    self.navLeftButton.setFont(arrowFont)
    QtCore.QObject.connect(self.navLeftButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.previousPage)
    self.navLeftButton.move(5, 60)

    self.navRightButton.setFixedSize(45, 400)
    arrowFont = QtGui.QFont(self.navRightButton.font())
    arrowFont.setPointSize(50)
    self.navRightButton.setFont(arrowFont)
    QtCore.QObject.connect(self.navRightButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.nextPage)
    self.navRightButton.move(750, 60)

    self.updateTimer = QtCore.QTimer()
    QtCore.QObject.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.updateModule)
    self.updateTimer.start(1000)
    
  def updateModule(self):
    self.waterHeaterModule.processRequest()
    
  def nextPage(self):
    if self.currentPageIndex >= len(self.pagesList)-1:
        return
    self.pagesList[self.currentPageIndex].hide()
    self.currentPageIndex += 1
    self.processPageChanged()
    
  def previousPage(self):
    if self.currentPageIndex <= 0:
        return
    self.pagesList[self.currentPageIndex].hide()
    self.currentPageIndex -= 1
    self.processPageChanged()  
    
  def processPageChanged(self):
    self.pagesList[self.currentPageIndex].show()
    title = self.pagesList[self.currentPageIndex].getTitle()
    for consumer in self.pageTitleConsumers:
      consumer.setText(title)
    self.update()

  def closeEvent(self, event):
    self.dataRetrievingManager.finish()
    event.accept()
    
  def paintEvent(self, event):
    super(Versatyle, self).paintEvent(event)
    bgImage = self.pagesList[self.currentPageIndex].getBackgroundImage()
    qpainter = QtGui.QPainter(self)
    qpainter.drawPixmap(QtCore.QPoint(0,0), QtGui.QPixmap(bgImage))
    
app = QtGui.QApplication([])
versatyle = Versatyle()
versatyle.init()
versatyle.show()
app.exec_()