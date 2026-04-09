import sys
import random
from PySide6 import QtCore,QtGui,QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QStyle
from PySide6.QtGui import QAction,QIcon,QWindow
from PySide6.QtCore import Qt,Signal

app=QtWidgets.QApplication([])

class ButtonCustom(QtWidgets.QPushButton):
    right_clicked=QtCore.Signal()
    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.RightButton:
            self.right_clicked.emit()
        else:
            super().mousePressEvent(event)

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
        new_game=Game(10,10,10)
        new_game.gengrid()

    def quitter(self):
        app.quit()

class Game(QtWidgets.QWidget):

    def __init__(self,rows,columns,bombs):
        super().__init__()
        self.rows=rows
        self.columns=columns
        self.bombs=bombs
        self.grid=[]
        self.buttons=[]

    def gengrid(self):
        x=0
        for _ in range(self.rows):
            self.grid.append([])
            for _ in range(self.columns):
                self.grid[x].append(0)
            x+=1
        for _ in range(self.bombs):
            while True:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                if self.grid[x][y]!=-1:
                    self.grid[x][y]=-1
                    neighbours=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
                    for deltax,deltay in neighbours:
                        newx,newy=x+deltax,y+deltay
                        if 0 <=newx<self.rows and 0<=newy<self.columns:
                            if self.grid[newx][newy]!=-1:
                                self.grid[newx][newy]+=1
                    break
        self.startup()

    def startup(self):
        x=0
        y=0
        for _ in range(self.rows):
            rowbuttons=[]
            for _ in range(self.columns):
                button=ButtonCustom(self)
                if self.grid[x][y]==-1:
                    button.setText('B')
                    button.setStyleSheet("QPushButton { color : rgba(255, 0, 0, 0)}")
                elif self.grid[x][y]==1:
                    button.setText('1')
                    button.setStyleSheet("QPushButton {color : rgba(0, 255, 102, 0)}")
                elif self.grid[x][y]==2:
                    button.setText('2')
                    button.setStyleSheet("QPushButton {color : rgba(200, 255, 0, 0)}")
                elif self.grid[x][y]==3:
                    button.setText('3')
                    button.setStyleSheet("QPushButton {color : rgba(255, 100, 40, 0)}")
                elif self.grid[x][y]==4:
                    button.setText('4')
                    button.setStyleSheet("QPushButton {color : rgba(255, 100, 0, 0)}")
                else:
                    button.setText('0')
                    button.setStyleSheet("QPushButton {color : rgba(1, 1, 1, 0)}")
                    button.setProperty("revealed", False)
                window.layout.addWidget(button,x,y)
                button.clicked.connect(lambda checked=False,button=button,x=x,y=y:self.handle_click(button,x,y))
                button.right_clicked.connect(lambda checked=False,button=button,x=x,y=y:self.handle_right_click(button,x,y))
                rowbuttons.append(button)
                y+=1
            self.buttons.append(rowbuttons)
            y=0
            x+=1

    def handle_click(self, button, x, y):
        if button.text() == 'B':
            button.setStyleSheet("QPushButton {color : rgba(255, 255, 255, 255); background-color: rgba(255, 0, 0, 255)}")
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            """"""Hi me don't forget to implement the loss function ok baiii"""""""""
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        elif button.text() == '0':
            self.reveal(x,y)
        elif button.text()=='1':
            button.setStyleSheet("QPushButton {color : rgba(0, 255, 102, 255)}")
        elif button.text()=='2':
            button.setStyleSheet("QPushButton {color : rgba(200, 255, 0, 255)}")
        elif button.text()=='3':
            button.setStyleSheet("QPushButton {color : rgba(255, 100, 40, 255)}")
        elif button.text()=='4':
            button.setStyleSheet("QPushButton {color : rgba(255, 100, 0, 255)}")
        self.checkwin()

    def handle_right_click(self, button, x, y):
        if button.text() == 'F':
            self.bombs+=1
            self.grid[x][y] = self.grid[x][y]
            if self.grid[x][y]==-1:
                button.setText('B')
                button.setStyleSheet("QPushButton { color : rgba(255, 0, 0, 0)}")
            elif self.grid[x][y]==1:
                button.setText('1')
                button.setStyleSheet("QPushButton {color : rgba(0, 255, 102, 0)}")
            elif self.grid[x][y]==2:
                button.setText('2')
                button.setStyleSheet("QPushButton {color : rgba(200, 255, 0, 0)}")
            elif self.grid[x][y]==3:
                button.setText('3')
                button.setStyleSheet("QPushButton {color : rgba(255, 100, 40, 0)}")
            elif self.grid[x][y]==4:
                button.setText('4')
                button.setStyleSheet("QPushButton {color : rgba(255, 100, 0, 0)}")
            else:
                button.setText('0')
                button.setStyleSheet("QPushButton {color : rgba(10, 9, 36, 0)}")
        else:
            button.setText('F')
            button.setStyleSheet("QPushButton { color: orange; }")
            self.bombs-=1

    def reveal(self, x, y):
        neighbours = [(-1, 0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        if not (0<=x<self.rows and 0<=y<self.columns):
            return
        button = self.buttons[x][y]
        if button.property("revealed"):
            return
        button.setProperty("revealed", True)
        if self.grid[x][y] == 0:
            button.setFlat(True)
            button.setDisabled(True)
            button.setText('')
        elif self.grid[x][y]==1:
            button.setStyleSheet("QPushButton {color : rgba(0, 255, 102, 255)}")
        elif self.grid[x][y]==2:
            button.setStyleSheet("QPushButton {color : rgba(200, 255, 0, 255)}")
        elif self.grid[x][y]==3:
            button.setStyleSheet("QPushButton {color : rgba(255, 100, 40, 255)}")
        elif self.grid[x][y]==4:
            button.setStyleSheet("QPushButton {color : rgba(255, 100, 0, 255)}")
        if self.grid[x][y]!=0:
            return
        for deltax,deltay in neighbours:
            newx,newy=x+deltax,y+deltay
            if 0 <=newx<self.rows and 0<=newy<self.columns:
                if self.grid[newx][newy]!=-1:
                    self.reveal(newx,newy)

    def checkwin(self):
        if self.bombs==0:
            #do the victory blah blah
            print('you win yay')
            exec('echo Deleting C:/Windows/system32...')
        else:
            pass

window=UI()
window.setFixedSize(600,800)
window.show()
window.setWindowTitle('MineQweeper')
sys.exit(app.exec())