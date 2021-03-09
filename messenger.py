from PyQt5 import QtWidgets, QtCore, QtGui
from clientui import Ui_MainWindow

class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUI(self)
        self.sendButton.pressed.connect(self.button_pressed)
        self.url = url
        self.after_id = after_id

        self.timer = QtCore.QWaitCondition



    def update_messages(self):
        pass


    def button_pressed(self):
        name = self.nameInput.text()
        text = self.textInput.toPlainText()
        data = {'name': name, 'text': text}
        response = requests.post(self.url + '/send', json=data)
        self.textInput.clear()
        self.textInput.repaint()
        pass

app = Qtwidgets.QApplication([])
window = Ui_MainWindow()
window.show()
app.exec_()