from Staves import *

class WhiteKey(QGraphicsRectItem):
    def __init__(self, i, staves):
        QGraphicsRectItem.__init__(self, 48*i, 0, 48, 369)
        self.setBrush(QBrush(QColor(255,255,255)))
        self.i = i
        self.j = str(self.i)
        self.staves = staves

    def mousePressEvent(self,event):
        if self.scene().itemAt(event.pos()) == self:
            QSound.play("Sounds/piano_" + self.j + ".wav")
            self.setBrush(QBrush(QColor(200,200,200)))
        self.staves.putinMel(self.i)
        self.staves.putKey(self.i)

    # def keyPressEvent(self,event):
    #     if event.key() == Qt.Key_q:
    #          QSound.play("piano_0.wav")

    def mouseReleaseEvent(self,event):
        self.setBrush(QBrush(QColor(255,255,255)))

class BlackKey(QGraphicsRectItem):
    def __init__(self, i, staves):
        QGraphicsRectItem.__init__(self, 48*i + 38 , 0, 18 , 180)
        self.setBrush(QBrush(QColor(0,0,0)))
        self.i = i
        self.j = str(self.i)
        self.staves = staves

    def mousePressEvent(self,event):
        if self.scene().itemAt(event.pos()) == self:
            QSound.play("Sounds/#piano_" + self.j + ".wav")
            self.setBrush(QBrush(QColor(200,200,200)))
        self.staves.putKey(self.i+14)

    def mouseReleaseEvent(self,event):
        self.setBrush(QBrush(QColor(0,0,0)))