import pickle
from PySide.QtGui import*
import time
from PySide.QtUiTools import*

class Note(QGraphicsPixmapItem):
    def __init__(self,parent = None):
        QGraphicsPixmapItem.__init__(self,parent)

        self.setFlag(QGraphicsItem.ItemIsSelectable,True)

class Save_window(QWidget):
    def __init__(self,view,staves):
        QWidget.__init__(self,None)

        self.staves = staves
        self.view = view
        layout = QVBoxLayout()
        loader = QUiLoader()
        form = loader.load("ui/Name.ui",self)

        self.Name = form.findChild(QLineEdit,"Name")
        self.Select_Name = form.findChild(QLabel,"Select_Name")
        self.comboBox = form.findChild(QComboBox,"comboBox")
        self.Ok = form.findChild(QPushButton,"OK_Button")
        self.Ok.clicked.connect(self.save)
        layout.addWidget(form)

        self.setLayout(layout)
    def save(self):
         if self.comboBox.currentText() == "PNG":
            pixmap = QPixmap.grabWidget(self.view)
            pixmap.save(self.Name.text()+"."+self.comboBox.currentText(),self.comboBox.currentText())
         else:
             infile = open(self.Name.text()+"."+self.comboBox.currentText(),'wb')
             pickle.dump(self.staves.mel,infile)
             infile.close()
         self.close()

class Load_window(QWidget):
    def __init__(self,staves):
        QWidget.__init__(self,None)

        self.staves = staves
        layout = QVBoxLayout()
        loader = QUiLoader()
        form = loader.load("ui/Load.ui",self)

        self.Filename = form.findChild(QLabel,"Filename")
        self.Load_button = form.findChild(QPushButton,"Load_button")
        self.Load_button.clicked.connect(self.load)
        self.Name = form.findChild(QLineEdit,"Name")

        layout.addWidget(form)
        self.setLayout(layout)

    def load(self):
        outfile = open(self.Name.text(),'rb')
        self.staves.mel = pickle.load(outfile)
        outfile.close()
       # print(self.staves.mel)
        s =''
        for i in self.staves.mel:
            try:
                if isinstance(int(i[0]),int):
                    self.staves.putKey(int(i[0]))
                    self.staves.setNote(int(i[-1]))
            except ValueError:
                print(i)
                for j in i:
                    if j == '.':
                        break
                    else:
                        s += j
                self.staves.putKey(s)
                s = ''
                print(s)
        self.close()

class Staves(QWidget):
    def __init__(self):
        QWidget.__init__(self,None)

        self.type = QPixmap()
        self.typ = 0
        self.mel = []
        self.Clefx = 0
        self.Clefy = 0
        self.liney = 20
        self.di = {0:"Whole",1:"Half",2:"Quarter",3:'Eighth',4:'Sixteenth',5:"DottedQuarter",6:"DottedHalf"}
        self.name = ''
        self.x = 100
        self.y = 0
        self.rhythm = 0
        self.rhythms = 0

        self.initUi()

    def initUi(self):

        layout = QVBoxLayout()

        self.resize(800,650)
        self.setWindowTitle("Meloditizer")

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 750, 550)

        clef = QPixmap("Images/Clef.png")
        clefGr = QGraphicsPixmapItem(clef)
        clefGr.setPos(self.Clefx,self.Clefy)

        self.scene.addItem(clefGr)

        self.view = QGraphicsView(self.scene, self)
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.show()

        loader = QUiLoader()
        form = loader.load("ui/Saved.ui",self)

        self.Save_Button = form.findChild(QPushButton,"Save_Button")
        self.Save_Button.clicked.connect(self.Saving)

        self.Play_Button = form.findChild(QPushButton,"Play_Button")
        self.Play_Button.clicked.connect(self.Playing)

        self.Delete_Button = form.findChild(QPushButton,"Delete_Button")
        self.Delete_Button.clicked.connect(self.Deleting)

        # timer = QTimer(self)
        # self.connect(timer,SIGNAL("timeout()"),self.Playing)
        # timer.start(1000)

        self.Load_Button = form.findChild(QPushButton,"Load_Button")
        self.Load_Button.clicked.connect(self.Loading)

        layout.addWidget(form)
        self.setLayout(layout)

    def Deleting(self):
        print(self.mel)
        self.mel.pop()
        infile = open("temp.MEL",'wb')
        pickle.dump(self.mel,infile)
        infile.close()
        self.close()

        self.v = Staves()
        self.v.show()
        outfile = open('temp.MEL','rb')
        self.v.mel = pickle.load(outfile)
        outfile.close()
        print(self.v.mel)
        for i in self.v.mel:
            self.v.putKey(int(i[0]))
            self.v.setNote(int(i[-1]))

    def Saving(self):
        self.s = Save_window(self.view,self)
        self.s.show()

    def Loading(self):
        self.l = Load_window(self)
        self.l.show()

    def Playing(self):
        for j in self.mel:
            time.sleep(0.5)
            QSound.play("Sounds/piano_" + j[0] + ".wav")

    def newLine(self):
        self.x = 100
        self.x2 = 100
        self.Clefy += 150
        clef = QPixmap("Images/Clef.png")
        clefGr = QGraphicsPixmapItem(clef)
        clefGr.setPos(self.Clefx,self.Clefy)
        self.scene.addItem(clefGr)

    def setNote(self,type):
        if isinstance(type,str):
            self.type = QPixmap("Images/"+type+".png")
            self.name = type
            self.typ = type
        else:
            self.type = QPixmap("Images/"+self.di[type]+".png")
            self.name = self.di[type]
            self.typ = type
        self.rhythmCheck()

    def rhythmCheck(self):
        counts = {"Quarter":1,"Half":2,"Whole":4,"Eighth":0.5,"Sixteenth":0.25,"DottedQuarter":1.5,"DottedHalf":3,"Rest":1\
            ,"Half_Rest":2,"Full_Rest":4}
        self.rhythm = counts[self.name]

    def clefCheck(self,i):
        if isinstance(i,str):
            self.y = self.Clefy + 8
        else:
            if self.Clefy == 0:
                self.y = 30-(4.25*i)
            elif self.Clefy == 150:
                self.y = 180-(4.25*i)
            elif self.Clefy == 300:
                self.y = 330-(4.25*i)
            elif self.Clefy == 450:
                self.y = 480-(4.25*i)
    def putinMel(self,i):
        self.mel.append(str(i)+ "."+ str(self.typ))
    def putKey(self,i):
        # self.mel.append(str(i))
        self.clefCheck(i)
        lineVer = QPixmap("Images/LineVer.png")
        lineVerGr = QGraphicsPixmapItem(lineVer)

        if self.rhythms >= 4:
            lineVerGr.setPos(self.x,self.liney)
            self.scene.addItem(lineVerGr)
            self.rhythms = 0
            self.x += 20

        self.rhythms += self.rhythm
        lineHori = QPixmap("Images/LineHori.png")
        lineHoriGr = QGraphicsPixmapItem(lineHori)

        if i == 0 or i == 12:
            lineHoriGr.setPos(self.x-3,self.y+32)
            self.scene.addItem(lineHoriGr)
        elif i == 13:
            lineHoriGr.setPos(self.x-3,self.y+34)
            self.scene.addItem(lineHoriGr)
        if isinstance(i,str):
            self.type = QPixmap("Images/" + i + ".png")
        elif i >= 6:
            self.type = QPixmap("Images/" + self.name + "2.png")
            self.y += 25
        elif i < 6:
            self.type = QPixmap("Images/" + self.name + ".png")

        note = Note(self.type)
        note.setPos(self.x,self.y)
        self.x += 30

        if self.x >= 700:
            self.liney +=150
            self.newLine()
        self.scene.addItem(note)


