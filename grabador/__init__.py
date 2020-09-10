#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui 
from grabador_principal import MainWindow2

def main():	
	app = QtGui.QApplication(sys.argv)
	app.Encoding(QtGui.QApplication.UnicodeUTF8)
        utfcodec = QtCore.QTextCodec.codecForName("UTF-8")
	QtCore.QTextCodec.setCodecForTr(utfcodec)
	QtCore.QTextCodec.setCodecForCStrings(utfcodec)
	QtCore.QTextCodec.setCodecForLocale(utfcodec)
	mainWindow = MainWindow2()   
	#mainWindow.setGeometry(100, 100, 200, 200)
	mainWindow.show()	
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
