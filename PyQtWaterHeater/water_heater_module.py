from PySide import QtCore
from PySide import QtXml
import auto_control_window

class WaterHeaterModule(QtCore.QObject):
  def __init__(self, _parent):
    QtCore.QObject.__init__(self, parent=_parent)
    self.autoControlWindow = auto_control_window.AutoControlWindow(_parent, self)
    self.httpHandler       = _parent.getHTTPHandler()
    self.onTime            = None
    self.offTime           = None
    self.durationTime      = None
    self.autoCtrlEnabled   = True
    
  def init(self):
    self.autoControlWindow.init()
    
  def getName(self):
    return "water_heater"
    
  def getCallback(self, name):
    if "config_dialog" == name:
      return self.show
    
  def parseXMLParameters(self, element):
    autoCtrlEnabled = element.attribute("enabled", "True")
    if "True" == autoCtrlEnabled:
      self.autoCtrlEnabled = True
    elif "False" == autoCtrlEnabled:
      self.autoCtrlEnabled = False
  
    hour = element.attribute("hour", "00:00")
    self.onTime = QtCore.QDateTime.currentDateTime()
    self.onTime.setTime(QtCore.QTime.fromString(hour, "hh:mm"))
    print("OnTime: ", self.onTime.toString())
    
    duration = element.attribute("duration", "03:00")
    print("Duration: ", duration)
    self.durationTime = QtCore.QTime.fromString(duration, "hh:mm")
    self.processSwitchOffDateTime()
    
  def getXMLConfiguration(self, doc):
    onOffParamNode = doc.createElement("AutoControlParameters")
    bool = "False"
    if True == self.isEnabled():
      bool = "True"
    onOffParamNode.setAttribute("enabled", bool)
    onOffParamNode.setAttribute("hour", self.getSwitchOnTime().time().toString("hh:mm"))
    onOffParamNode.setAttribute("duration", self.getDurationTime().toString("hh:mm"))
    return onOffParamNode
    
  def processRequest(self):
    if False == self.autoCtrlEnabled:
      return
    if (QtCore.QDateTime.currentDateTime().__ge__(self.onTime) ):
      self.switchOnCommand()
      self.onTime = self.onTime.addDays(1)
      print("ON !!!!")
    elif (QtCore.QDateTime.currentDateTime().__ge__(self.offTime) ):
      self.switchOffCommand()
      self.offTime = self.offTime.addDays(1)
      print("OFF !!!")

  def switchOnCommand(self):
    switchOnParam = self.httpHandler.getSwitchOnParameters()
    url  = switchOnParam[0]
    body = switchOnParam[1]
    self.httpHandler.post(url, body, self.processReply)

  def switchOffCommand(self):
    switchOffParam = self.httpHandler.getSwitchOffParameters()
    url  = switchOffParam[0]
    body = switchOffParam[1]
    self.httpHandler.post(url, body, self.processReply)
    
  def processReply(self, reply):
    pass
    
  def getSwitchOnTime(self):
    return self.onTime
    
  def setSwitchOnTime(self, time):
    self.onTime = time

  def getSwitchOffTime(self):
    return self.offTime
    
  def getDurationTime(self):
    return self.durationTime
    
  def setDurationTime(self, time):
    self.durationTime = time
    self.processSwitchOffDateTime()
  
  def isEnabled(self):
    return self.autoCtrlEnabled
    
  def setEnabled(self, state):
    self.autoCtrlEnabled = state
  
  def processSwitchOffDateTime(self):
    tempTime = QtCore.QDateTime(self.onTime)
    self.offTime = tempTime.addSecs((self.durationTime.hour() * 60 * 60) + \
                                     self.durationTime.minute() * 60) 
   
  def newConfigEvent(self):
    self.parent().saveXMLConfiguration()
    
  def show(self):
    self.autoControlWindow._show()
    