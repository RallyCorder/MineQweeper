import os
from PySide6 import QtCore
from PySide6.QtCore import QSettings

conf=QSettings('MineQweeper','mineqweeper')
conf.setValue('difficulty','easy')
conf.setValue('theme','system')
conf.beginGroup('Custom')
conf.setValue('customx',15)
conf.setValue('customy',16)
conf.setValue('custombombs',23)
conf.endGroup()