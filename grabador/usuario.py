#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui 
from PyQt4.QtSql import *
from PyQt4 import uic

(Ui_MainWindow, QMainWindow) = uic.loadUiType('/usr/usr/share/GrabadorRadio/usuarios.ui')

class Usuario(QMainWindow):
		"""MainWindow inherits QMainWindow"""
		def __init__ (self, parent=None):
			utfcodec = QtCore.QTextCodec.codecForName("UTF-8")
        		QtCore.QTextCodec.setCodecForTr(utfcodec)
        		QtCore.QTextCodec.setCodecForCStrings(utfcodec)
        		QtCore.QTextCodec.setCodecForLocale(utfcodec)			
			QMainWindow.__init__(self, parent)
			self.ui = Ui_MainWindow()
			self.ui.setupUi(self)
			self.setWindowTitle("Agregar Usuario")
			self.setWindowIcon(QtGui.QIcon('/usr/usr/share/GrabadorRadio/logo2.png'))
			self.centrar()
			self.base_datos()
			self.busca()	
			QtCore.QObject.connect(self.ui.pushButton_2,QtCore.SIGNAL("clicked()"), self.salir)
			QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"), self.agrega)
			QtCore.QObject.connect(self.ui.pushButton_3,QtCore.SIGNAL("clicked()"), self.eliminar)	
			query = QSqlQuery(db)			
			if query.exec_("SELECT * FROM cargos"):
				while query.next():
					self.ui.comboBox.addItem(str(query.value(1).toString()))
					
		def base_datos(self):
			global db
			base_datos="Db"
			db = QSqlDatabase.addDatabase("QMYSQL",base_datos);
			if db.isOpen() == False:
				db.setHostName("localhost")
				db.setDatabaseName("radiomonitor")
				db.setUserName("root")
				db.setPassword("cadafe")
				ok = db.open()
				# True if connected
				if ok:
					print "Conecto"
				else:
					print "Fallo"
		def agrega(self):
			if len(str(self.ui.lineEdit.text()))>0 and len(str(self.ui.lineEdit_2.text()))>0:
				query = QSqlQuery(db)			
				cod=str(self.ui.lineEdit.text())
				nomb=str(self.ui.lineEdit_2.text())
				app=str(self.ui.lineEdit_3.text())
				carg=str(self.ui.comboBox.currentText())
				model=str(self.ui.lineEdit_5.text())
				seri=str(self.ui.lineEdit_6.text())
				query.exec_("INSERT INTO usuarios (codigo,nombre,apellido,cargo,modelo,serial) values('%s', '%s','%s','%s','%s','%s')" % (cod,nomb,app,carg,model,seri))
				self.ui.listWidget.clear()
				self.ui.lineEdit.clear()
				self.ui.lineEdit_2.clear()
				self.ui.lineEdit_3.clear()
				#self.ui.lineEdit_4.clear()
				self.ui.lineEdit_5.clear()
				self.ui.lineEdit_6.clear()				
				self.busca()
			else:
				self.ui.label_5.setText("No debe dejar campos vacios")
		
		def busca(self):
			global codigos	
			codigos = []
			query = QSqlQuery(db)
			if query.exec_("SELECT * FROM usuarios where codigo!='Desconocido'"):
				while query.next():
					codigos.append(str(query.value(1).toString()))
					self.ui.listWidget.addItem(str(query.value(1).toString()) + "   " + str(query.value(2).toString()) + " " + str(query.value(4).toString()) + " " + str(query.value(3).toString()))		
		def eliminar(self):
			if self.ui.listWidget.currentRow() >= 0:
				codigo = (codigos[self.ui.listWidget.currentRow()])
				query = QSqlQuery(db)			
				query.exec_("DELETE FROM usuarios WHERE codigo='%s'" % (codigo))
				query.exec_("ALTER TABLE usuarios AUTO_INCREMENT=0")
				self.ui.listWidget.clear()
				self.busca()
				
		def salir(self):
			db.close()
			self.close()

		def centrar(self):
			screen = QtGui.QDesktopWidget().screenGeometry()
			size =  self.geometry()
			self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
