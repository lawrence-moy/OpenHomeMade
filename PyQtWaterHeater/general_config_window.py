from PySide import QtGui 
from PySide import QtCore

class GeneralConfigWindow(QtGui.QDialog):
  def __init__(self, _parent, generalConfigManager):
    QtGui.QDialog.__init__(self, parent=_parent)
    self.generalConfigManager  = generalConfigManager
    self.gridLayout       = QtGui.QGridLayout()
    self.fullscreenMode   = QtGui.QPushButton("Fullscreen mode")
    self.labelFontSize    = 25
    self.valueFontSize    = 30
    self.validateButton   = QtGui.QPushButton("Apply")
    
  def init(self):
    self.setupGUI()
    self.placeWidgets()
    
  def setupGUI(self):
    labelFont = QtGui.QFont(self.fullscreenMode.font())
    labelFont.setPointSize(self.labelFontSize)

    self.fullscreenMode.setFont(labelFont)
    self.fullscreenMode.setCheckable(True)
    QtCore.QObject.connect(self.fullscreenMode, 
                           QtCore.SIGNAL("clicked()"), 
                           self.fullscreenEvent)
    
    buttonFont = QtGui.QFont(self.validateButton.font())
    buttonFont.setPointSize(30)
    self.validateButton.setFont(buttonFont)
    self.validateButton.setIcon(QtGui.QIcon("ok.png"));
    self.validateButton.setIconSize(QtCore.QSize(50, 50));

    QtCore.QObject.connect(self.validateButton, 
                           QtCore.SIGNAL("clicked()"), 
                           self.applyParameters)
    self.setLayout(self.gridLayout)
    self.setFixedSize(QtCore.QSize(380, 380))

  def placeWidgets(self):
    self.gridLayout.addWidget(self.fullscreenMode,  0, 2)
    self.gridLayout.addWidget(self.validateButton,   6, 2)
    
  def _show(self):
    #self.autoCtrlEnabled.setChecked(self.autoCtrlManager.isEnabled())
    #self.autoCtrlEnabledEvent()
    self.show()
    
  def fullscreenEvent(self):
    if True == self.fullscreenMode.isChecked():
      self.parent().showFullScreen()
    else:
      self.parent().showNormal()
    
  def applyParameters(self):
    #self.autoCtrlManager.setEnabled(self.autoCtrlEnabled.isChecked())
    #self.autoCtrlManager.setSwitchOnTime(self.startTime.dateTime())
    #self.autoCtrlManager.setDurationTime(self.duration.time())
    self.hide()
    self.autoCtrlManager.newConfigEvent()
      