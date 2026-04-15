import sys
import os
import random
from PySide6 import QtCore,QtGui,QtWidgets
from PySide6.QtWidgets import QApplication, QWidget, QStyle
from PySide6.QtGui import QAction, QIcon, QWindow
from PySide6.QtCore import Qt, Signal, QSettings

app=QtWidgets.QApplication([])
app.setApplicationName('MineQweeper')
app.setApplicationDisplayName('MineQweeper')

conf=QSettings('MineQweeper','Mineqweeper')
conf.value('difficulty')
conf.beginGroup('Custom')
conf.value('customx')
conf.value('customy')
conf.value('custombombs')
conf.endGroup()

conf.sync()

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
        self.helpdd=self.menubar.addMenu('&Help')

        self.newact=QtGui.QAction('&New',self)
        self.newact.triggered.connect(self.new)
        self.newact.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_N)

        self.settingsact=QtGui.QAction('&Settings',self)
        self.settingsact.triggered.connect(self.settings)
        self.settingsact.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_S)

        self.quitact=QtGui.QAction('&Quit',self)
        self.quitact.triggered.connect(self.quitter)
        self.quitact.setShortcut(Qt.Modifier.CTRL | Qt.Key.Key_Q)

        self.actiondd.addAction(self.newact)
        self.actiondd.addAction(self.settingsact)
        self.actiondd.addAction(self.quitact)

        self.flaglabel=QtWidgets.QLabel('FLAGS')
        self.flaglabel.setStyleSheet("QLabel {color : rgba(255, 140, 0, 255)}")

        self.layout.addWidget(self.menubar,0,0,-1,-1)
        self.layout.addWidget(self.flaglabel,0,10)

    def new(self):
        if conf.value('difficulty')=='medium':
            new_game=Game(16,16,40)
        elif conf.value('difficulty')=='hard':
            new_game=Game(30,16,99)
        elif conf.value('difficulty')=='custom':
            conf.beginGroup('Custom')
            new_game=Game(int(conf.value('customx')),int(conf.value('customy')),int(conf.value('custombombs')))
            conf.endGroup()
        else:
            new_game=Game(9,9,10)
        new_game.gengrid()

    def settings(self):
        self.settingstech=Settings()
        self.settingstech.show()
        self.settingstech.setWindowTitle('Settings')
        self.settingstech.setFixedSize(600,200)

    def quitter(self):
        app.quit()

class Game(QtWidgets.QWidget):

    def __init__(self,rows,columns,bombs):
        super().__init__()
        self.rows=rows
        self.columns=columns
        self.bombs=bombs
        self.initbombs=bombs
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
                x = random.randint(0, self.rows-1)
                y = random.randint(0, self.columns-1)
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
                    button.setStyleSheet("QPushButton {color : rgba(0, 0, 0, 0)}")
                elif self.grid[x][y]==1:
                    button.setText('1')
                    button.setStyleSheet("QPushButton {color : rgba(0, 0, 0, 0)}")
                elif self.grid[x][y]==2:
                    button.setText('2')
                    button.setStyleSheet("QPushButton {color : rgba(0, 0, 0, 0)}")
                elif self.grid[x][y]==3:
                    button.setText('3')
                    button.setStyleSheet("QPushButton {color : rgba(0, 0, 0, 0)}")
                elif self.grid[x][y]==4:
                    button.setText('4')
                    button.setStyleSheet("QPushButton {color : rgba(0, 0, 0, 0)}")
                else:
                    button.setText('0')
                    button.setStyleSheet("QPushButton {color : rgba(1, 1, 1, 0)}")
                    button.setProperty("revealed", False)
                window.layout.addWidget(button,x+1,y+1)
                button.clicked.connect(lambda checked=False,button=button,x=x,y=y:self.handle_click(button,x,y))
                button.right_clicked.connect(lambda checked=False,button=button,x=x,y=y:self.handle_right_click(button,x,y))
                rowbuttons.append(button)
                y+=1
            self.buttons.append(rowbuttons)
            y=0
            x+=1

            window.layout.addWidget(window.flaglabel,self.rows+1,self.columns)
            window.flaglabel.setText(self.bombs.__str__())

    def handle_click(self, button, x, y):
        if button.text() == 'B':
            button.setStyleSheet("QPushButton {color : rgba(255, 255, 255, 255); background-color: rgba(255, 0, 0, 255)}")
            restarter.show()
            restarter.setUI(True)
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
        elif button.text()>'4':
            button.setStyleSheet("QPushButton {color : rgba(74, 255, 165, 255)}")
        self.checkwin()

    def handle_right_click(self, button, x, y):
        if button.text() == 'F' and self.bombs>=0 and self.bombs<=self.initbombs:
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
            elif button.text()>'4':
                button.setStyleSheet("QPushButton {color : rgba(74, 255, 165, 0)}")
            else:
                button.setText('0')
                button.setStyleSheet("QPushButton {color : rgba(10, 9, 36, 0)}")
        else:
            if self.bombs>=0:
                button.setText('F')
                button.setStyleSheet("QPushButton {color : rgba(255, 140, 0, 255)}")
                self.bombs-=1
        window.flaglabel.setText(self.bombs.__str__())

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
            restarter.show()
            restarter.setUI(True)
        else:
            pass

class Settings(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        style=self.style()
        select_icon=style.standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
        null_icon=style.standardIcon(QStyle.StandardPixmap.SP_CustomBase)

        self.layout=QtWidgets.QGridLayout(self)

        self.difficultylabel=QtWidgets.QLabel('<b>Difficulty</b>')
        self.difficultybar=QtWidgets.QComboBox(self)
        self.difficultybar.addItem(null_icon,'Easy, 9x9 | 10 bombs')
        self.difficultybar.addItem(null_icon,'Medium, 16x16 | 40 bombs')
        self.difficultybar.addItem(null_icon,'Hard, 30x16 | 99 bombs')
        self.difficultybar.addItem(null_icon,'Custom')
        if conf.value('difficulty')=='medium':
            self.difficultybar.setItemIcon(1,select_icon)
        elif conf.value('difficulty')=='hard':
            self.difficultybar.setItemIcon(2,select_icon)
        elif conf.value('difficulty')=='custom':
            self.difficultybar.setItemIcon(3,select_icon)
        else:
            self.difficultybar.setItemIcon(0,select_icon)
        self.difficultycustomx=QtWidgets.QSpinBox(self)
        self.difficultycustomx.setSuffix(' x')
        self.difficultycustomy=QtWidgets.QSpinBox(self)
        self.difficultycustomy.setSuffix(' y')
        self.difficultycustombombs=QtWidgets.QSpinBox(self)
        self.difficultycustombombs.setSuffix(' bombs')
        
        self.themelabel=QtWidgets.QLabel('<b>Theme</b>')
        self.themeselect=QtWidgets.QComboBox(self)
        self.themeselect.addItem(null_icon,'System')
        self.themeselect.addItem(null_icon,'Light')
        self.themeselect.addItem(null_icon,'Dark')
        if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Light:
            self.themeselect.setItemIcon(1,select_icon)
        if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            self.themeselect.setItemIcon(2,select_icon)
        if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Unknown:
            self.themeselect.setItemIcon(0,select_icon)

        self.applybutton=QtWidgets.QPushButton(self)
        self.applybutton.setText('&Apply and restart')
        self.applybutton.clicked.connect(self.apply)

        self.cancelbutton=QtWidgets.QPushButton(self)
        self.cancelbutton.setText('&Cancel')
        self.cancelbutton.clicked.connect(self.cancel)

        self.layout.addWidget(self.difficultylabel,0,0)
        self.layout.addWidget(self.difficultybar,0,1,1,2)
        self.layout.addWidget(self.difficultycustomx,1,0)
        self.layout.addWidget(self.difficultycustomy,1,1)
        self.layout.addWidget(self.difficultycustombombs,1,2)
        self.layout.addWidget(self.themelabel,2,0)
        self.layout.addWidget(self.themeselect,2,1,1,2)
        self.layout.addWidget(self.cancelbutton,3,0)
        self.layout.addWidget(self.applybutton,3,2)

    def apply(self):
        if self.themeselect.currentIndex()==0:
            conf.setValue('theme','system')
            app.setStyle('qt6ct-style')
        if self.themeselect.currentIndex()==1:
            conf.setValue('theme','light')
            app.setStyle('Adwaita')
        if self.themeselect.currentIndex()==2:
            conf.setValue('theme','dark')
            app.setStyle('Adwaita-Dark')
        if self.difficultybar.currentIndex()==0:
            conf.setValue('difficulty','easy')
        if self.difficultybar.currentIndex()==1:
            conf.setValue('difficulty','medium')
        if self.difficultybar.currentIndex()==2:
            conf.setValue('difficulty','hard')
        if self.difficultybar.currentIndex()==3:
            conf.setValue('difficulty','custom')
            conf.beginGroup('Custom')
            conf.setValue('customx',self.difficultycustomx.value())
            conf.setValue('customy',self.difficultycustomy.value())
            conf.setValue('custombombs',self.difficultycustombombs.value())
            conf.endGroup()
        conf.sync()
        os.execv(sys.executable, [sys.executable]+sys.argv)

    def cancel(self):
        self.destroy()

class RestartUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.status=None
        self.layout=QtWidgets.QGridLayout(self)
        self.restartbut=QtWidgets.QPushButton(self)
        self.restartbut.setText('&Restart')
        self.restartbut.clicked.connect(self.restart)
        self.quitbut=QtWidgets.QPushButton(self)
        self.quitbut.setText('&Quit')
        self.quitbut.clicked.connect(UI.quitter)
        self.layout.addWidget(self.restartbut,1,0)
        self.layout.addWidget(self.quitbut,1,2)

    def setUI(self,status):
        if self.status==True:
            self.wintag=QtWidgets.QLabel('You win!')
        else:
            self.wintag=QtWidgets.QLabel('You lose')
        self.layout.addWidget(self.wintag,0,1)

    def restart(self):
        os.execv(sys.executable, [sys.executable]+sys.argv)
            
window=UI()
window.setFixedSize(600,800)
window.show()
restarter=RestartUI()
restarter.setFixedSize(200,100)
window.setWindowTitle('MineQweeper')
sys.exit(app.exec())