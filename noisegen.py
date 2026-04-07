import sys
import random
from PySide6 import QtCore,QtGui,QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QStyle
from PySide6.QtGui import QAction,QIcon,QWindow
from PySide6.QtCore import Qt

app=QtWidgets.QApplication([])

class UI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout=QtWidgets.QGridLayout(self)

        self.menubar=QtWidgets.QMenuBar(self)
        self.actiondd=self.menubar.addMenu('&Game')
        self.settingsdd=self.menubar.addMenu('&Settings')
        self.helpdd=self.menubar.addMenu('&Help')

        self.newact=QtGui.QAction('&New',self)
        self.newact.triggered.connect(self.new)
        self.newact.setShortcut(Qt.Key.Key_N)

        self.quitact=QtGui.QAction('&Quit',self)
        self.quitact.triggered.connect(self.quitter)
        self.quitact.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_Q)

        self.actiondd.addAction(self.newact)
        self.actiondd.addAction(self.quitact)

        self.layout.addWidget(self.menubar)

    def new(self):
        new_game=Game()
        new_game.startup()

    def quitter(self):
        app.quit()


class Game(QtWidgets.QWidget):

    x=0
    y=0
    def startup(self):
        import perlin_carson as perlin
        Game.x=0
        Game.y=0
        perlin.gen_noise()
        d=0
        avgg=[]
        for element in range(10):
            avg=sum(perlin.combined_noise_array[d])/len(perlin.combined_noise_array[d])
            d+=1
            avgg.append(avg)
        #add more precision for higher difficulties and grids
        if sum(avgg)>100:
            print('pattern 1 - sum(avgg)<100')
            for element in range(10):
                for element in range(10):
                    button=QtWidgets.QPushButton(self)
                    num=perlin.combined_noise_array[Game.x][Game.y]
                    if num>400:
                        button.setText('B')
                        button.setStyleSheet("QPushButton { color : rgb(255, 0, 0)}")
                    elif num>130:
                        button.setText('3')
                        button.setStyleSheet("QPushButton {color : rgb(255, 100, 40)}")
                    elif num>80:
                        button.setText('2')
                        button.setStyleSheet("QPushButton {color : rgb(200, 255, 0)}")
                    elif num>0:
                        button.setText('1')
                        button.setStyleSheet("QPushButton {color : rgb(0, 255, 102)}")
                    elif num>-80:
                        button.setText('0')
                        button.setStyleSheet("QPushButton {color : rgb(0, 81, 255)}")
                    elif num>-140:
                        button.setText('-1')
                        button.setStyleSheet("QPushButton {color : rgb(16, 0, 190)}")
                    elif num>-190:
                        button.setText('-2')
                        button.setStyleSheet("QPushButton {color : rgb(5, 0, 105)}")
                    else:
                        button.setText('-3')
                        button.setStyleSheet("QPushButton {color : rgb(10, 9, 36)}")
                    window.layout.addWidget(button,Game.x,Game.y)
                    Game.y+=1
                Game.y=0
                Game.x+=1
        else:
            print('pattern 2 - sum(avgg)>100')
            for element in range(10):
                for element in range(10):
                    button=QtWidgets.QPushButton(self)
                    num=perlin.combined_noise_array[Game.x][Game.y]
                    if num>-80:
                        button.setText('B')
                        button.setStyleSheet("QPushButton { color : rgb(255, 0, 0)}")
                    elif num>-79:
                        button.setText('2')
                        button.setStyleSheet("QPushButton {color : rgb(200, 255, 0)}")
                    elif num>-50:
                        button.setText('1')
                        button.setStyleSheet("QPushButton {color : rgb(0, 255, 102)}")
                    elif num>-30:
                        button.setText('0')
                        button.setStyleSheet("QPushButton {color : rgb(0, 81, 255)}")
                    elif num>-20:
                        button.setText('-1')
                        button.setStyleSheet("QPushButton {color : rgb(16, 0, 190)}")
                    elif num>0:
                        button.setText('-2')
                        button.setStyleSheet("QPushButton {color : rgb(5, 0, 105)}")
                    else:
                        button.setText('Null')
                        button.setStyleSheet("QPushButton {color : rgb(10, 9, 36)}")
                    window.layout.addWidget(button,Game.x,Game.y)
                    Game.y+=1
                Game.y=0
                Game.x+=1


window=UI()
window.setFixedSize(600,800)
window.show()
window.setWindowTitle('MineQweeper')
sys.exit(app.exec())