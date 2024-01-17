import sys
import time
import pygame

from pygame import mixer
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('zmeila_dezin.ui', self)  # Загружаем дизайн
        self.pushButton_2.clicked.connect(self.prod1)
        self.pushButton_3.clicked.connect(self.zak)
        mixer.init()
        mixer.music.load("zmeika_nachalo.mp3")
        mixer.music.play()



    def prod1(self):
        self.pushButton_2.setText('Точно?')
        self.pushButton_2.clicked.connect(self.prod2)


    def prod2(self):
        self.pushButton_2.setText('Уверены?')
        self.pushButton_2.clicked.connect(self.prod3)


    def prod3(self):
        self.pushButton_2.setText('100%?')
        self.pushButton_2.clicked.connect(self.prod4)
        self.label.setText('😈🐍😈🐍😈🐍😈🐍😈')
        self.label_2.setText('🐍😈🐍😈🐍😈🐍😈🐍')
        self.label_3.setText('😈🐍😈🐍😈🐍😈🐍😈')



    def prod4(self):
        mixer.music.pause()
        mixer.music.load("zmeika.mp3")
        mixer.music.play()
        time.sleep(1)
        pp = 931
        while pp > 0:
            time.sleep(0.01)
            ex.resize(pp, pp)
            pp -= 1
        ex.hide()
        mixer.music.pause()






    def zak(self):
        ex.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
