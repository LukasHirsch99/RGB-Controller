import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
import serial
from time import sleep

# opening serial port to comunicate to arduino
arduino = serial.Serial('COM3', 9600)

# lineEidit for the rgb values
class RGBvalue(QLineEdit):
  def __init__(self, window, objectName, defaultVal, pos):
    super().__init__()
    self.setParent(window)
    self.setDisabled(True)
    self.setObjectName(objectName)
    self.setText(defaultVal)
    self.setGeometry(*pos, 40, 20)
    self.setInputMask('000')
    self.textEdited.connect(window.changePreview)

# main class
class Window(QWidget):
  def __init__(self):
    super().__init__()
    self.myInit()
  
  # changes the rgb values when color is picked
  def changeRgbCode(self):
    self.rVal.setText(str(self.color[0]))
    self.gVal.setText(str(self.color[1]))
    self.bVal.setText(str(self.color[2]))
    self.setPreview(tuple(self.color))

  # changes the speed for fade or party
  def changeSpeed(self, speed):
    if self.mode == 'fade':
      self.fadeSpeed = speed
      self.speedVal.setText(str(speed))
    elif self.mode == 'party':
      self.partySpeed = speed
      self.speedVal.setText(str(speed))

  # converts rgb color code to hex color code
  def toHEX(self, rgb): return "#%02x%02x%02x" % rgb

  # checks if the entered rgb values are valid
  def changePreview(self):
    sender = self.sender()
    if sender.text() == '': return
    val = int(sender.text())
    if val > 255:
      sender.setStyleSheet('background-color : red')
      return
    else: sender.setStyleSheet('')

    if sender.objectName() == 'Redval': self.color[0] = val
    elif sender.objectName() == 'Greenval': self.color[1] = val
    elif sender.objectName() == 'Blueval': self.color[2] = val

    self.setPreview(tuple(self.color))
  
  # changes the color of the preview button
  def setPreview(self, rgb): self.preview.setStyleSheet('background-color : %s; border-radius : 60px' %  self.toHEX(rgb))

  # when pickColorbut is pressed
  def pickColor(self):
    self.colorPicker = QColorDialog.getColor()
    if QColor.isValidColor(self.colorPicker.name()):
      self.color = list(self.colorPicker.getRgb()[:-1])
      self.changeRgbCode()

  # when user changes the light mode this function sets the gui to the proper state
  def changeMode(self, i):
    self.mode = self.modesMenu.currentText()
    if self.mode == 'static':
      self.preview.setIcon(QIcon())
      self.setPreview(tuple(self.color))
      self.rVal.setDisabled(False)
      self.gVal.setDisabled(False)
      self.bVal.setDisabled(False)
      self.speedSlider.setHidden(True)
      self.speedVal.setHidden(True)
      self.speedTxt.setHidden(True)
      self.pickColorBut.setDisabled(False)

    elif self.mode == 'white':
      self.color = [255, 255, 255]
      self.preview.setIcon(QIcon())
      self.changeRgbCode()
      self.rVal.setDisabled(True)
      self.gVal.setDisabled(True)
      self.bVal.setDisabled(True)
      self.speedSlider.setHidden(True)
      self.speedVal.setHidden(True)
      self.speedTxt.setHidden(True)

    elif self.mode == 'fade' or self.mode == 'party':
      self.preview.setStyleSheet('border-radius : 60px; background-color : white;')
      self.preview.setIcon(QIcon('images\\gradient3.png'))
      self.preview.setIconSize(QSize(120, 120))
      self.rVal.setDisabled(True)
      self.gVal.setDisabled(True)
      self.bVal.setDisabled(True)
      self.speedSlider.setHidden(False)
      self.speedVal.setHidden(False)
      self.speedTxt.setHidden(False)
      self.pickColorBut.setDisabled(True)

    elif self.mode == 'off':
      self.rVal.setDisabled(True)
      self.gVal.setDisabled(True)
      self.bVal.setDisabled(True)
      self.speedSlider.setHidden(True)
      self.speedVal.setHidden(True)
      self.speedTxt.setHidden(True)
      self.pickColorBut.setDisabled(True)

  # writes data to the arduino via serial port
  def apply(self):
    if self.mode == 'static':
      arduino.write(('applyColor %s %s %s' % tuple(self.color)).encode())
    elif self.mode == 'fade':
      arduino.write(('f %s' % self.fadeSpeed).encode())
    elif self.mode == 'party':
      arduino.write(('p %s' % self.partySpeed).encode())
    if self.mode == 'white':
      arduino.write('w'.encode())
    elif self.mode == 'off':
      arduino.write('0'.encode())
  
  # gets called when the rgb values are changed to change check if the values are valid
  def speedValChanged(self, text):
    if text == 'ms': return 
    speed = int(text[:-2])
    if speed > 100:
      self.speedVal.setStyleSheet('background-color : red')
      return
    else: self.speedVal.setStyleSheet('')
    self.speedSlider.setValue(speed)
    if self.mode == 'fade':
      self.fadeSpeed = speed
    elif self.mode == 'party':
      self.partySpeed = speed
      
  # when return or enter is pressed apply the current mode to the arduino
  def keyPressEvent(self, QKeyEvent):
    if QKeyEvent.key() == Qt.Key_Enter or QKeyEvent.key() == Qt.Key_Return:
      self.apply()

  # own init-function for window
  def myInit(self):
    self.speedSlider = QSlider(self)
    self.speedSlider.setOrientation(Qt.Horizontal)
    self.speedSlider.setFixedSize(100, 10)
    self.speedSlider.sliderMoved.connect(self.changeSpeed)
    self.speedSlider.setMinimum(0)
    self.speedSlider.setMaximum(100)
    self.speedSlider.setValue(25)

    # value of the speed for party and fading mode
    self.speedVal = QLineEdit(self)
    self.speedVal.setFixedSize(40, 20)
    self.speedVal.setInputMask('000ms')
    self.speedVal.setText('25')
    self.speedVal.textEdited.connect(self.speedValChanged)
    self.speedTxt = QLabel('Speed', self)

    # a button because you can easy set an icon for the preview of the color
    self.preview = QPushButton(self)
    self.preview.setFixedSize(120, 120)
    self.preview.setIcon(QIcon('images\\gradient3.png'))
    self.preview.setIconSize(QSize(120, 120))
    self.preview.setStyleSheet('border-radius : 60px; background-color : white;')

    #the different modes for the light
    self.mode = 'fade'
    self.modesMenu = QComboBox(self)
    self.modesMenu.addItems(['fade', 'static', 'party', 'white', 'off'])
    self.modesMenu.currentIndexChanged.connect(self.changeMode)
    modesTxt = QLabel('Mode', self)

    # apply-button
    applyBut = QPushButton('Apply', self)
    applyBut.clicked.connect(self.apply)

    # the fade and party speed and the color wich will be applied to the arduino
    self.color = [255, 0, 0]
    self.fadeSpeed = 25
    self.partySpeed = 25

    # button to pick a color
    self.pickColorBut = QPushButton(self)
    self.pickColorBut.setFixedSize(30, 30)
    self.pickColorBut.setIconSize(QSize(30, 30))
    self.pickColorBut.setStyleSheet('border-radius : 15')
    self.pickColorBut.setIcon(QIcon('images\\ColorPicker.png'))
    self.pickColorBut.clicked.connect(self.pickColor)
    self.pickColorBut.setDisabled(True)

    # the rgb values
    self.rVal = RGBvalue(self, 'Redval', '255', (60, 30))
    self.gVal = RGBvalue(self, 'Greenval', '0', (60, 60))
    self.bVal = RGBvalue(self, 'Blueval', '0', (60, 90))
    rTxt = QLabel('Red', self)
    rTxt.setStyleSheet('color : red')
    gTxt = QLabel('Green', self)
    gTxt.setStyleSheet('color : green')
    bTxt = QLabel('Blue', self)
    bTxt.setStyleSheet('color : blue')

    # move all widgets to their position
    rTxt.move(25, 33)
    gTxt.move(25, 63)
    bTxt.move(25, 93)

    applyBut.move(240, 250)
    self.preview.move(140, 30)
    self.pickColorBut.move(255, 120)
    self.modesMenu.move(150, 170)
    modesTxt.move(110, 174)
    self.speedTxt.move(106, 210)
    self.speedSlider.move(150, 215)
    self.speedVal.move(260, 209)

    self.setGeometry(1000, 300, 330, 290)
    self.setWindowTitle("RGB Controller")
    self.setWindowIcon(QIcon("images\\icon891.png"))
    self.show()

# defines the app
app = QApplication(sys.argv)

# makes instance of window
window = Window()

# when ecit button is pressed app closes
sys.exit(app.exec_())