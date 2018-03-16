from PySide import QtCore
from PySide import QtXml
import general_config_window

class GeneralConfigManager(QtCore.QObject):
  def __init__(self, _parent):
    QtCore.QObject.__init__(self, parent=_parent)
    self.generalConfigWindow = general_config_window.GeneralConfigWindow(_parent, self)
    
  def init(self):
    self.generalConfigWindow.init()
    
  def parseXMLParameters(self, element):
    pass
    
  def getXMLConfiguration(self, doc):
    pass
    
  def activeFullscreen(self):
    pass

  def isFullscreen(self):
    pass
    
  def newConfigEvent(self):
    self.parent().saveXMLConfiguration()
    
  def show(self):
    self.generalConfigWindow._show()
    