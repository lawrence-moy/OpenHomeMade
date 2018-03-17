from PySide import QtCore
import time

class WebServiceRequester(QtCore.QThread):
  def __init__(self, _parent, url, interval):
    QtCore.QThread.__init__(self, parent=_parent)
    self.exiting  = False
    self.url      = url
    self.interval = interval
    
  def init(self):
    pass
    
  def stop(self):
    print("STOP")
    self.exiting = True
    
  def run(self):
    while False == self.exiting:
      print("-")
      time.sleep(0.1)
