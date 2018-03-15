from PySide import QtGui 
from PySide import QtCore

class AutoControlWindow(QtGui.QDialog):
  def __init__(self, _parent, autoControlManager):
    QtGui.QDialog.__init__(self, parent=_parent)
    self.autoCtrlManager  = autoControlManager
    self.gridLayout       = QtGui.QGridLayout()
    self.autoCtrlEnabled  = QtGui.QPushButton("Enable auto control")
    self.labelStartTime   = QtGui.QLabel("Time switch on :")
    self.labelFontSize    = 25
    self.valueFontSize    = 30
    self.startTime        = QtGui.QTimeEdit()
    self.labelDuration    = QtGui.QLabel("Duration :")
    self.duration         = QtGui.QTimeEdit()
    self.validateButton   = QtGui.QPushButton("Apply")
    
  def init(self):
    self.setupGUI()
    self.placeWidgets()
    
  def setupGUI(self):
    labelFont = QtGui.QFont(self.labelStartTime.font())
    labelFont.setPointSize(self.labelFontSize)
    self.labelStartTime.setFont(labelFont)
    
    self.autoCtrlEnabled.setFont(labelFont)
    self.autoCtrlEnabled.setCheckable(True)
    QtCore.QObject.connect(self.autoCtrlEnabled, 
                           QtCore.SIGNAL("clicked()"), 
                           self.autoCtrlEnabledEvent)
    
    self.startTime.setStyleSheet("QTimeEdit::up-button   { subcontrol-position: left;  width: 40px; height: 40px; }"
                                 "QTimeEdit::down-button { subcontrol-position: right; width: 40px; height: 40px; }")
    valueFont = QtGui.QFont(self.startTime.font())
    valueFont.setPointSize(self.valueFontSize)
    self.startTime.setFont(valueFont)
    self.startTime.setAlignment(QtCore.Qt.AlignCenter)
    self.startTime.setDisplayFormat("hh:mm")

    self.labelDuration.setFont(labelFont)
    self.duration.setStyleSheet("QTimeEdit::up-button   { subcontrol-position: left;  width: 40px; height: 40px; }"
                                "QTimeEdit::down-button { subcontrol-position: right; width: 40px; height: 40px; }")
    self.duration.setFont(valueFont)
    self.duration.setAlignment(QtCore.Qt.AlignCenter)
    self.duration.setDisplayFormat("hh:mm")
    
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
    self.gridLayout.addWidget(self.autoCtrlEnabled,  0, 2)
    self.gridLayout.addWidget(self.labelStartTime,   1, 2)
    self.gridLayout.addWidget(self.startTime,        2, 2)
    self.gridLayout.addWidget(self.labelDuration,    3, 2)
    self.gridLayout.addWidget(self.duration,         4, 2)
    self.gridLayout.addWidget(self.validateButton,   6, 2)
    
  def _show(self):
    self.autoCtrlEnabled.setChecked(self.autoCtrlManager.isEnabled())
    self.autoCtrlEnabledEvent()
    self.startTime.setDateTime(self.autoCtrlManager.getSwitchOnTime())
    self.duration.setTime(self.autoCtrlManager.getDurationTime())
    self.show()
    
  def autoCtrlEnabledEvent(self):
    state = self.autoCtrlEnabled.isChecked()
    self.startTime.setEnabled(state)
    self.duration.setEnabled(state)
    
  def applyParameters(self):
    self.autoCtrlManager.setEnabled(self.autoCtrlEnabled.isChecked())
    self.autoCtrlManager.setSwitchOnTime(self.startTime.dateTime())
    self.autoCtrlManager.setDurationTime(self.duration.time())
    self.hide()
    self.autoCtrlManager.newConfigEvent()
      