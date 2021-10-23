# https://build-system.fman.io/pyqt5-tutorial
# https://forum.qt.io/topic/82420/show-picture-using-qlabel-and-pixmap/4
# https://github.com/pythonguis/15-minute-apps/blob/master/minesweeper/minesweeper.py
# https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtcore/qt.html#CaseSensitivity
# https://doc.qt.io/qt-5/qcompleter.html
# https://zetcode.com/gui/pyqt5/eventssignals/
# https://wiki.python.org/moin/PyQt/Adding%20tab-completion%20to%20a%20QLineEdit

import time
from os import path, read, walk, scandir
from glob import glob


#import PyQt5.QtWidgets as qt
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QWidget, QLabel, QCompleter, QLineEdit, QFileDialog
from PySide6.QtWidgets import QBoxLayout
from PySide6.QtCore import QEvent, QTimer, Qt, QPoint
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

def get_all_subdirs(dir):
    dirs = []
    for d in walk(dir):
        p = d[0][len(dir)+1:]
        dirs.append(p.replace('\\','/'))
    return dirs

def get_subdirs_old(dir):
    return next(walk(dir))[1]

def get_subdirs(dir):
    print("get_subdirs(" + dir + ")")
    relative_to = cfg['destination']
    return [f.path[len(relative_to)+1:].replace('\\', '/') for f in scandir(dir) if f.is_dir()]
    #subdirs = []
    #for dir in scandir(dir):
    #    if dir.is_dir():
    #        subdirs.append(dir.path[len(relative_to)+1:].replace('\\', '/'))
    #return subdirs

app = QApplication([])
#window = QtWidgets.QWidget()

w_width = 800
w_height = 1000


class linia(QLineEdit):
    def keyPressEvent(self, e):
        QLineEdit.keyPressEvent(self, e)

class DirCompleter(QCompleter):
    def __init__(self, *args, **kwargs):
        QCompleter.__init__(self, *args, **kwargs)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setMaxVisibleItems(20)

class Window(QMainWindow):
    def choose_dirs(self):
        if 'source' not in cfg:
            cfg['source'] = QFileDialog.getExistingDirectory(self, "Choose a source folder", None, QFileDialog.ShowDirsOnly)
        if 'destination' not in cfg:
            cfg['destination'] = QFileDialog.getExistingDirectory(self, "Choose a destination folder", None, QFileDialog.ShowDirsOnly)

        save_cfg(cfg, cfg_file)
        print(cfg)

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        w = QWidget()
        self.layout=QBoxLayout(QBoxLayout.LeftToRight, w)

        self.choose_dirs()
        self.lasttab = 0

        file = gl(cfg['source']+"\*.jpg")[0]

        self.bitmap = QtGui.QImage(file)
        self.bitmap = self.bitmap.scaled(w_width, w_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label = QLabel('Hello World!', parent=w)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.bitmap))

        # scroll
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.shift)
        #QTimer.singleShot(2000, lambda: self.timer.start(10))
        #QTimer.singleShot(5000, self.timer.stop)

        self.expanded_dir = ''
        self.completions = get_subdirs(cfg['destination'] + self.expanded_dir)
        self.comp = DirCompleter(self.completions)
        #self.comp.setCompletionMode(QCompleter.InlineCompletion)


        self.box = QLineEdit(parent=w)
        self.box.setFixedWidth(500)
        #self.box.setFocusPolicy(Qt.ClickFocus)
        self.box.setCompleter(self.comp)

        self.popup = self.comp.popup()
        #popup.setFocusPolicy(Qt.NoFocus)
        self.popup.installEventFilter(self)
        self.box.installEventFilter(self)
        
        self.model = self.popup.model()

        self.setCentralWidget(w)

        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.box.textChanged.connect(self.updateComp)

    def reloadComp(self):
        self.comp.deleteLater()
        #self.model.deleteLater()
        #self.popup.deleteLater()
        #del self.comp, self.model, self.popup

        self.comp = DirCompleter(self.completions)
        self.box.setCompleter(self.comp)
        self.model = self.comp.model()
        self.popup = self.comp.popup()
        self.movePopup()

    def updateComp(self, text):
        print("text: " + text)
        self.box.setFocus()
        self.popup.show()
        
        if text in self.completions:

            #if text != path.dirname(self.expanded_dir):
            subdirs = get_subdirs(cfg['destination'] + '/' + text)
            if not subdirs:
                print("exit")
                return
            self.expanded_dir = text
            self.completions = subdirs
            #print(subdirs)
            self.reloadComp()

            
        elif len(text) < len(self.expanded_dir):
            parent = path.dirname(self.expanded_dir)
            print("parent: " + parent)
            subdirs = get_subdirs(cfg['destination'] + '/' + parent)
            self.expanded_dir = parent
            self.completions = subdirs
            print("subdirs: ", subdirs)

            self.reloadComp()
        
        elif not text:
            self.reloadComp()


    def showEvent(self, event):
        self.movePopup()

    def movePopup(self):
        bl = self.box.rect().bottomLeft()
        p = self.box.mapToGlobal(bl)
        self.popup.move(p)
        self.popup.show()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyRelease and
            (source is self.box or source is self.popup)):

            #self.box.keyPressEvent(event)
            self.box.setFocus()
            self.popup.show()

            
            if event.key() == Qt.Key_Tab:
                text = self.box.text()
                print("text: ", text)
                items = list(filter(lambda x: x.lower().startswith(text.lower()), self.completions))
                #items = [self.model.data(self.model.index(x, 0)) for x in range(self.model.rowCount())]
                print("items: ", items)

                prefix = path.commonprefix(items)
                print("prefix: " + prefix)
                if len(prefix) > len(text):
                    self.box.setText(prefix)
                # choose the first items when tabbing two times in 1 sec
                elif len(prefix) == len(text):
                    now = time.time()
                    if now - self.lasttab < 1:
                        self.box.setText(items[0])
                    self.lasttab = time.time()
            
        if (event.type() == QEvent.KeyPress and
            event.key() == Qt.Key_Tab):
            pass
            # tab turns the completion popup off, so we must show it again
            #QTimer.singleShot(1, self.popup.show)

            #model = self.comp.popup().model()
            #items = [model.data(model.index(x, 0)) for x in range(model.rowCount())]

            #print(items)
            #prefix = path.commonprefix(items)
            #print(prefix)

            #if prefix:
            #    self.box.setText(prefix)
            

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

window.setWindowTitle('img-sorter')
window.resize(w_width, w_height)
#window.keyPressEvent = keyPressEvent
window.show()
#window.popup.show()
app.exec()