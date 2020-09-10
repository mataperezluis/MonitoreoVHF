#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
from monitoreo import Monitor 
from PyQt4 import QtGui 
from PyQt4 import QtCore
import sys

def main():
	app = QtGui.QApplication(sys.argv)
	app.Encoding(QtGui.QApplication.UnicodeUTF8)
	utfcodec = QtCore.QTextCodec.codecForName("UTF-8")
	QtCore.QTextCodec.setCodecForTr(utfcodec)
	QtCore.QTextCodec.setCodecForCStrings(utfcodec)
	QtCore.QTextCodec.setCodecForLocale(utfcodec)
	mainWindow = Monitor()   
	#mainWindow.setGeometry(100, 100, 200, 200)
	mainWindow.show()	
	sys.exit(app.exec_())

if __name__ == "__main__":	
	main()
