# https://build-system.fman.io/pyqt5-tutorial
# https://forum.qt.io/topic/82420/show-picture-using-qlabel-and-pixmap/4
# https://github.com/pythonguis/15-minute-apps/blob/master/minesweeper/minesweeper.py
# https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtcore/qt.html#CaseSensitivity
# https://doc.qt.io/qt-5/qcompleter.html
# https://zetcode.com/gui/pyqt5/eventssignals/
# https://wiki.python.org/moin/PyQt/Adding%20tab-completion%20to%20a%20QLineEdit

from os import path, read
from glob import glob

#import PyQt5.QtWidgets as qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QCompleter, QLineEdit, QApplication, QFileDialog 
from PyQt5.QtCore import QEvent, QTimer, Qt
#from time import sleep
#from PyQt5.QtCore import QRect


def gl(s):
  return sorted(glob(s))

def read_cfg(filename):
    cfg = {}

    if path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                kv = line.strip().split('=',1)
                cfg[kv[0]] = kv[1]
    else:
        with open(filename, 'w') as f:
            pass
    
    return cfg

def save_cfg(cfg, filename):
    with open(filename, 'w') as f:
        for k, v in cfg.items():
            f.write(k + '=' + v + '\n')

cfg_file = 'config.txt'
cfg = read_cfg(cfg_file)


app = QApplication([])
#window = QtWidgets.QWidget()

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        w = QWidget()

        if 'source' not in cfg:
            cfg['source'] = QFileDialog.getExistingDirectory(self, "Choose a source folder", None, QFileDialog.ShowDirsOnly)
        if 'destination' not in cfg:
            cfg['destination'] = QFileDialog.getExistingDirectory(self, "Choose a destination folder", None, QFileDialog.ShowDirsOnly)

        save_cfg(cfg, cfg_file)
        print(cfg)

        file = gl(cfg['source']+"\*.jpg")[0]

        self.bitmap = QtGui.QImage(file)
        self.bitmap = self.bitmap.scaledToWidth(500, Qt.SmoothTransformation)

        self.label = QLabel('Hello World!', parent=w)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.bitmap))
        self.label.setAlignment(Qt.AlignTop)


        # scroll
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.shift)
        #QTimer.singleShot(2000, lambda: self.timer.start(10))
        #QTimer.singleShot(5000, self.timer.stop)

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