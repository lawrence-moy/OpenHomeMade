from PySide import QtCore

import time
import http_handler

class WebServiceRequester(QtCore.QThread):
  def __init__(self, queue, _parent, url, interval):
    QtCore.QThread.__init__(self, parent=_parent)
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
      #self.queue.put(("water_temp", i))
      self.httpHandler.get(self.url, self.processReply)
      time.sleep(self.interval)

  def processReply(self, reply):
    print(reply)