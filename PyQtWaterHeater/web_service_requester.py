from PySide import QtCore
import threading
import time
import http_handler

class WebServiceRequester(threading.Thread):
  def __init__(self, queue, url, interval):
    threading.Thread.__init__(self)
    self.exiting  = False
    self.url      = url
    self.interval = interval
    self.queue    = queue

  def init(self):
    pass
    
  def stop(self):
    self.exiting = True
    
  def run(self):
    self.httpHandler = http_handler.HTTPHandler()
    while False == self.exiting:
      json = self.httpHandler.get(self.url)
      if None != json:
        self.processReply(json)
      time.sleep(self.interval)

  def processReply(self, reply):
    json = eval(reply)
    for module in json:
      moduleIdStr = module.get("ref")
      if None == moduleIdStr:
        continue
      moduleId = int(moduleIdStr)
      for variableName in module.keys():
        value = module[variableName]
        if "io10" == variableName:
          print("Send:", (moduleId, variableName, value))
        self.queue.put((moduleId, variableName, value))
    