from Piano import *
from PySide.QtUiTools import *

class menu(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self,None)
        loader = QUiLoader()
        form = loader.load("./ui/Meloditizer.ui",self)
        self.setCentralWidget(form)

    def mousePressEvent(self,event):
        w = Piano()
        w.show()
        self.close()