from PySide import QtCore
from Queue import Queue
import web_service_requester

class DataRetrievingManager(QtCore.QObject):
  def __init__(self, _parent):
    QtCore.QObject.__init__(self, parent=_parent)
    self.service = None
    self.consumers = {}
    self.queue = Queue()

  def init(self):
    self.dataRetrievingTimer = QtCore.QTimer()
    QtCore.QObject.connect(self.dataRetrievingTimer, QtCore.SIGNAL("timeout()"), self.processData)
    self.dataRetrievingTimer.start(100)  
    
  def processData(self):
    while not self.queue.empty():
      key, value = self.queue.get()
      if None == self.consumers.get(key):
        return
      for consumer in self.consumers.get(key):
        consumer.setValue(value)
    
  def finish(self):
    self.service.stop()
    if not self.service.wait(3000):
      self.service.terminate()
      self.service.wait()
      
  def registerConsumer(self, widget, variableName):
    if None == self.consumers.get(variableName):
      self.consumers[variableName] = []
    print("register consumer: ", variableName, widget)
    self.consumers[variableName].append(widget)
    
  def parseXMLParameters(self, element):
    subDataRetrievingNode = element.firstChild()
    while not subDataRetrievingNode.isNull():
      serviceElement = subDataRetrievingNode.toElement()
      if not serviceElement.isNull():
        if "WebService" == serviceElement.tagName():
           url      = serviceElement.attribute("url", "")
           interval = float(serviceElement.attribute("interval", "1"))
           webService = web_service_requester.WebServiceRequester(self.queue, self, url, interval)
           webService.start()
           self.service = webService
      subDataRetrievingNode = subDataRetrievingNode.nextSibling()
    
  def getXMLConfiguration(self, doc):
    pass
    
  def newConfigEvent(self):
    self.parent().saveXMLConfiguration()
    
  def show(self):
    pass
    