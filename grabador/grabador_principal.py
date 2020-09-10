#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui 
from PyQt4 import uic

(Ui_MainWindow, QMainWindow1) = uic.loadUiType('/usr/usr/share/GrabadorRadio/mainwindow.ui')
#(Ui_MainWindow2, QMainWindow) = uic.loadUiType('principal.ui')
(Ui_MainWindow3, QMainWindow3) = uic.loadUiType('/usr/usr/share/GrabadorRadio/acerca.ui')
from mainwindow import MainWindow
from radios import Radios
from usuario import Usuario
#from monitoreo import Monitor

class acerca(QMainWindow3):

	def __init__(self):
		QMainWindow3.__init__(self)
		self.ui = Ui_MainWindow3()
		self.ui.setupUi(self) 				
		self.centrar()
		self.setWindowTitle("Acerca de...")
		self.setWindowIcon(QtGui.QIcon('/usr/usr/share/GrabadorRadio/logo2.png'))
		
	def centrar(self):	
		screen = QtGui.QDesktopWidget().screenGeometry()
		size =  self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

class propiedades(QMainWindow1):
	def __init__(self,parent):
		QMainWindow1.__init__(self,parent)
		self.prueba = parent
		#layout = QHBoxLayout()
		#lineEdit = QLineEdit()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self) 
		self.centrar()
		#lineEdit.setText("Just to fill up the dialog")
		#layout.addWidget(lineEdit)
		self.widget2 = (MainWindow())
		#self.widget.setLayout(layout)
		self.setCentralWidget(self.widget2)
		self.setWindowIcon(QtGui.QIcon('/usr/usr/share/GrabadorRadio/logo2.png'))
		self.setWindowTitle("Propiedades Conexion")
		QtCore.QObject.connect(self.widget2.ui.pushButton,QtCore.SIGNAL("clicked()"), self.salir)
		QtCore.QObject.connect(self.widget2.ui.pushButton_4,QtCore.SIGNAL("clicked()"), self.ocultar)
		QtCore.QObject.connect( self.widget2, QtCore.SIGNAL( "send( PyQt_PyObject)"), self.barraVol)
		QtCore.QObject.connect( self.widget2, QtCore.SIGNAL( "send2( PyQt_PyObject)"), self.dtmf)
	def salir(self):
		QtCore.QObject.disconnect(self.widget2.ui.pushButton,QtCore.SIGNAL("clicked()"), self.salir)
		QtCore.QObject.disconnect(self.widget2.ui.pushButton_4,QtCore.SIGNAL("clicked()"), self.ocultar)
		QtCore.QObject.disconnect( self.widget2, QtCore.SIGNAL( "send( PyQt_PyObject)"), self.barraVol)
		QtCore.QObject.disconnect( self.widget2, QtCore.SIGNAL( "send2( PyQt_PyObject)"), self.dtmf)		
		self.widget2.ctimer.stop()
		try:
			conteo = self.prueba.layout.indexOf(self.boton)
			h=0
		except:
			h=1
		if h == 0 :				
			conteo2=conteo 
			while conteo >= (conteo2 - 3):
				item = self.prueba.layout.takeAt(conteo)
				conteo = conteo - 1
				if not item:
				   continue
				w = item.widget()
				if w:	
				   w.deleteLater()
		self.widget2.salir()
		self.close()

	def barraVol(self, message):
		self.barra.setValue(int(message))

	def dtmf(self,message):
		self.lista.addItem(str(message))

	def ocultar(self):
		oculta,indice,texto = self.widget2.ocultar()				
		if  oculta== 1:		
			self.label1 = (QtGui.QLabel("Conexion " + str(texto)))		
			self.prueba.layout.addWidget(self.label1,indice,0)
			self.barra = (QtGui.QProgressBar())			
			self.prueba.layout.addWidget(self.barra,indice,1)
			self.barra.setRange(-50,0)	
			self.barra.setValue(-50)							
			self.barra.setFormat("%v")	
			self.lista = QtGui.QListWidget()	
			self.prueba.layout.addWidget(self.lista,indice,2)
			self.boton = QtGui.QPushButton("X")
			QtCore.QObject.connect(self.boton,QtCore.SIGNAL("clicked()"), self.salir)
			self.prueba.layout.addWidget(self.boton,indice,3)
			self.prueba.widget.setLayout(self.prueba.layout)
			self.hide()	
	def centrar(self):
		screen = QtGui.QDesktopWidget().screenGeometry()
		size =  self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

class MainWindow2(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		#self.ui = Ui_MainWindow2()      	
		self.widget = QtGui.QWidget()
		self.setCentralWidget(self.widget)
		#self.ui.setupUi(self)  
		self.menuBar = QtGui.QMenuBar(self)	
		self.setMenuBar(self.menuBar)
		self.menu = self.menuBar.addMenu('&Acciones')
		self.menu2 = self.menuBar.addMenu('&Herramientas')
		self.menu3 = self.menuBar.addMenu('&Ayuda')
		global mainWindow		
		
		accionNuv = self.menu.addAction('Nueva Conexion')		
		accionSal = self.menu.addAction('Salir')				
		accionacr=self.menu3.addAction('Acerca de...')	
		accionUser=self.menu2.addAction('Agregar Usuario')	
		accionRadio=self.menu2.addAction('Agregar Radio')
		#accionMonitor=self.menu2.addAction('Monitoreo')						
		self.layout = QtGui.QGridLayout()
		self.widget.setLayout(self.layout)		
		self.setGeometry(0, 0, 500, 250)
		self.setWindowIcon(QtGui.QIcon('/usr/usr/share/GrabadorRadio/logo2.png'))
		self.setWindowTitle("Grabador Radio")
		self.centrar()
		self.connect(accionNuv, QtCore.SIGNAL('triggered()'), self.newWindow)
		self.connect(accionacr, QtCore.SIGNAL('triggered()'), self.acercade)
		self.connect(accionSal, QtCore.SIGNAL('triggered()'), self.salir)
		self.connect(accionUser, QtCore.SIGNAL('triggered()'), self.usuario)	
		self.connect(accionRadio, QtCore.SIGNAL('triggered()'), self.radio)
		#self.connect(accionMonitor, QtCore.SIGNAL('triggered()'), self.monitoreo)

	def newWindow(self):	
		self.prop=propiedades(self)
		self.prop.show()
	def acercade(self):		
		self.acer = acerca()
		self.acer.show()
	def salir(self):
		sys.exit(0)
	def usuario(self):
		self.usr = Usuario()
		self.usr.show()
	def radio(self):
		self.radio = Radios()
		self.radio.show()
	#def monitoreo(self):
	#	self.mon=Monitor()
	#	self.mon.show()
	def centrar(self):
		screen = QtGui.QDesktopWidget().screenGeometry()
		size =  self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
