# https://build-system.fman.io/pyqt5-tutorial
# https://forum.qt.io/topic/82420/show-picture-using-qlabel-and-pixmap/4
# https://github.com/pythonguis/15-minute-apps/blob/master/minesweeper/minesweeper.py
# https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtcore/qt.html#CaseSensitivity
# https://doc.qt.io/qt-5/qcompleter.html
# https://zetcode.com/gui/pyqt5/eventssignals/
# https://wiki.python.org/moin/PyQt/Adding%20tab-completion%20to%20a%20QLineEdit

from utils import gl
import sys

#import PyQt5.QtWidgets as qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QCompleter, QLineEdit, QApplication
from PyQt5.QtCore import QEvent, QTimer, Qt
#from time import sleep
#from PyQt5.QtCore import QRect

app = QApplication([])
#window = QtWidgets.QWidget()

print(sys.argv[1])
file = gl(sys.argv[1])[0]

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        w = QWidget()

        self.bitmap = QtGui.QImage(file)
        self.bitmap = self.bitmap.scaledToWidth(500, Qt.SmoothTransformation)

        self.label = QLabel('Hello World!', parent=w)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.bitmap))
        self.label.setAlignment(Qt.AlignTop)

        # scroll
        self.timer = QTimer()
        self.timer.timeout.connect(self.shift)
        QTimer.singleShot(2000, lambda: self.timer.start(10))
        QTimer.singleShot(5000, self.timer.stop)

        self.comp = QCompleter(['pap', 'spacex'])
        self.comp.setCaseSensitivity(Qt.CaseInsensitive)
        #self.comp.setCompletionMode(QCompleter.InlineCompletion)
        self.box = QLineEdit(parent=w)
        self.box.setCompleter(self.comp)
        self.box.installEventFilter(self)

        self.setCentralWidget(w)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
            source is self.box and
            event.key() == Qt.Key_Space):

            print('key press:', (event.key(), event.text()))
        return super(QMainWindow, self).eventFilter(source, event)
    #def keyPressEvent(self, e):
        #if e.key() == Qt.Key_Space:
    #bitmap.scroll(0, -10, bitmap.rect())

    def shift(self):
        x = self.bitmap.width()
        y = self.bitmap.height()
        self.bitmap = self.bitmap.copy(0, 10, x, y)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.bitmap))


window = Window()


window.setWindowTitle('PyQt5 App')
window.resize(500, 1000)
#window.keyPressEvent = keyPressEvent
window.show()
app.exec()