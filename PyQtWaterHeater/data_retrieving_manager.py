from PySide import QtCore
import sys
if sys.version_info[0] < 3:
  from Queue import Queue
else:
  import queue
import web_service_requester
import threading
import time

class DataRetrievingManager(threading.Thread):
  def __init__(self, _parent):
    threading.Thread.__init__(self)
    self.service = None
    self.consumers = {}
    if sys.version_info[0] < 3:
      self.queue = Queue()
    else:
      self.queue = queue.Queue()
    self.parent = _parent
    self.exiting = False

  def init(self):
    pass
    
  def run(self):
    while False == self.exiting:
      while not self.queue.empty():
        moduleId, key, value = self.queue.get()
        if None == self.consumers.get(key):
          continue
        for consumer in self.consumers.get(key):
          consumer.setValue(value)
      time.sleep(0.05)

  def finish(self):
    self.service.stop()
    self.service.join()
    self.exiting = True

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
           webService = web_service_requester.WebServiceRequester(self.queue,
                                                                  url, interval)
           webService.start()
           self.service = webService
      subDataRetrievingNode = subDataRetrievingNode.nextSibling()
    
  def getXMLConfiguration(self, doc):
    pass
    
  def newConfigEvent(self):
    self.parent.saveXMLConfiguration()
    
  def show(self):
    pass
    