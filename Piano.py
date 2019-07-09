from Key import *
from PySide.QtUiTools import *

class Piano(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Meloditizer")

        self.staves = Staves()

        self.note_type = 2
        self.staves.setNote(self.note_type)
        self.initUi()

    def initUi(self):
        layout = QVBoxLayout()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0,0,673,293)

        for i in range(14):
            self.scene.addItem(WhiteKey(i, self.staves))
        for i in [0, 1, 3, 4, 5, 7, 8, 10, 11, 12]:
            self.scene.addItem(BlackKey(i,self.staves))

        view = QGraphicsView(self.scene)
        layout.addWidget(view)
        self.setLayout(layout)

        loader = QUiLoader()
        form = loader.load("./ui/Select the Note.ui",self)

        self.Whole_Note = form.findChild(QPushButton,"Whole_Note")
        self.Whole_Note.clicked.connect(lambda: self.selected(0))

        self.Half_Note = form.findChild(QPushButton,"Half_Note")
        self.Half_Note.clicked.connect(lambda: self.selected(1))

        self.Quarter_Note = form.findChild(QPushButton,"Quarter_Note")
        self.Quarter_Note.clicked.connect(lambda: self.selected(2))

        self.Eighth_Note = form.findChild(QPushButton,"Eighth_Note")
        self.Eighth_Note.clicked.connect(lambda: self.selected(3))

        self.Sixteenth_Note = form.findChild(QPushButton,"Sixteenth_Note")
        self.Sixteenth_Note.clicked.connect(lambda: self.selected(4))

        self.Dotted_QNote = form.findChild(QPushButton,"Dotted_QuarterNote")
        self.Dotted_QNote.clicked.connect(lambda: self.selected(5))

        self.Dotted_HNote = form.findChild(QPushButton,"Dotted_HalfNote")
        self.Dotted_HNote.clicked.connect(lambda: self.selected(6))

        self.Rest = form.findChild(QPushButton,"Rest")
        self.Rest.clicked.connect(lambda: self.restPut("Rest"))

        self.Half_Rest = form.findChild(QPushButton,"Half_Rest")
        self.Half_Rest.clicked.connect(lambda: self.restPut("Half_Rest"))

        self.Full_Rest = form.findChild(QPushButton,"Full_Rest")
        self.Full_Rest.clicked.connect(lambda: self.restPut("Full_Rest"))

        self.wholeCh = form.findChild(QLabel,"WholeCh")
        self.eighthCh = form.findChild(QLabel,"EighthCh")
        self.halfCh = form.findChild(QLabel,"HalfCh")
        self.quarterCh = form.findChild(QLabel,"QuarterCh")
        self.DhalfCh = form.findChild(QLabel,"DottedHalfCh")
        self.DquarterCh = form.findChild(QLabel,"DottedQuarterCh")
        self.sixteenCh = form.findChild(QLabel,"SixteenthCh")

        self.types = [self.wholeCh,self.halfCh,self.quarterCh,self.eighthCh,self.sixteenCh,self.DquarterCh,self.DhalfCh]

        for i in self.types:
            i.setPixmap("Images/Check.png")
            i.setVisible(False)

        self.quarterCh.setVisible(True)

        layout.addWidget(form)

        self.setLayout(layout)

    def restPut(self,rest_type):
        self.staves.setNote(rest_type)
        self.staves.putKey(rest_type)
    def selected(self,note_type):
        self.note_type = note_type
        for i in self.types:
            i.setVisible(False)
            self.types[note_type].setVisible(True)
        self.staves.setNote(self.note_type)