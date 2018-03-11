from PySide import QtCore

class RequestManager(QtCore.QObject):
  def __init__(self, _parent):
    QtCore.QObject.__init__(self, parent=_parent)
    
  def init(self):
    self.autoCtrlParamHandler = self.parent().getAutoControlParametersHandler()
    self.networkHandler       = self.parent().getNetworkHandler()
    
  def processRequest(self):
    onTime  = self.autoCtrlParamHandler.getSwitchOnTime()
    offTime = self.autoCtrlParamHandler.getSwitchOffTime()
    if (QtCore.QDateTime.currentDateTime().__ge__(onTime) ):
      self.switchOnCommand()
      self.autoCtrlParamHandler.setSwitchOnTime(onTime.addDays(1))
      print("ON !!!!")
    elif (QtCore.QDateTime.currentDateTime().__ge__(offTime) ):
      self.switchOffCommand()
      self.autoCtrlParamHandler.setSwitchOffTime(offTime.addDays(1))
      print("OFF !!!")

  def switchOnCommand(self):
    switchOnParam = self.networkHandler.getSwitchOnParameters()
    url  = switchOnParam[0]
    body = switchOnParam[1]
    self.networkHandler.sendRequest(url, body)

  def switchOffCommand(self):
    switchOffParam = self.networkHandler.getSwitchOffParameters()
    url  = switchOffParam[0]
    body = switchOffParam[1]
    self.networkHandler.sendRequest(url, body)