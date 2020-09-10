#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui 
from PyQt4.QtSql import *
from PyQt4 import uic
import time
import datetime
import calendar
from Reproductor import Reproduce
import matplotlib
matplotlib.use('QT4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from pylab import *
(Ui_MainWindow, QMainWindow) = uic.loadUiType('/usr/usr/share/MonitoreoRadio/monitoreo.ui')

class Monitor(QMainWindow):
		"""MainWindow inherits QMainWindow"""
		def __init__ (self, parent=None):
			global mainWindow
			utfcodec = QtCore.QTextCodec.codecForName("UTF-8")
			QtCore.QTextCodec.setCodecForTr(utfcodec)
			QtCore.QTextCodec.setCodecForCStrings(utfcodec)
			QtCore.QTextCodec.setCodecForLocale(utfcodec)
			QMainWindow.__init__(self, parent)
			self.ui = Ui_MainWindow()
			self.ui.setupUi(self)
			self.setWindowTitle("Monitoreo")
			self.centrar()
			self.base_datos()
			self.busca()
			self.setWindowIcon(QtGui.QIcon('/usr/usr/share/MonitoreoRadio/logo2.png'))
			global fecha		
			fecha=QtCore.QDate()
			self.ui.dateEdit.setDate(fecha.currentDate())
			self.ui.dateEdit_2.setDate(fecha.currentDate())
			QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"), self.buscador)
			QtCore.QObject.connect(self.ui.radioButton,QtCore.SIGNAL("clicked()"), self.radioA)
			QtCore.QObject.connect(self.ui.radioButton_2,QtCore.SIGNAL("clicked()"), self.radioB)
			QtCore.QObject.connect(self.ui.pushButton_2,QtCore.SIGNAL("clicked()"), self.consulta)
			QtCore.QObject.connect(self.ui.radioButton_3,QtCore.SIGNAL("clicked()"), self.radioC)
			QtCore.QObject.connect(self.ui.dateEdit,QtCore.SIGNAL("dateChanged(QDate)"), self.cambioFecha)
			QtCore.QObject.connect(self.ui.dateEdit_2,QtCore.SIGNAL("dateChanged(QDate)"), self.cambioFecha2)
			self.ui.label_10.setVisible(False)
			self.ui.lineEdit.setVisible(False)
			self.radioA()
			global queryFecha
			queryFecha = "and fecha >= '" + self.ui.dateEdit.date().toString("yyyy-MM-dd") + \
			"' and fecha <= '" + self.ui.dateEdit_2.date().toString("yyyy-MM-dd") + "'"
			self.ui.label_11.setText(queryFecha)
			self.ui.label_11.setVisible(False)
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
		def buscador(self):
			global botones
			botones = []
			queryFecha=self.ui.label_11.text()
			while self.ui.tableWidget.rowCount() > 0 :			
				self.ui.tableWidget.removeRow(self.ui.tableWidget.rowCount()-1)
			if len(str(self.ui.comboBox_2.currentText())) > 0 and len(str(self.ui.comboBox.currentText())) > 0 and len( str(self.ui.comboBox_3.currentText())) > 0:
				query = QSqlQuery(db)	
				if query.exec_("SELECT g.fecha,g.hora,g.codigo,u.nombre,u.apellido,u.cargo,\
				j.Nombre,g.audio FROM radios_nombre j, radios_grabacion g LEFT OUTER JOIN \
				usuarios u ON g.codigo=u.codigo where j.Nombre='%s' and g.codigo='%s' and \
				j.Nombre=g.radio %s" % (str(self.ui.comboBox.currentText()),\
				str(self.ui.comboBox_2.currentText()),queryFecha)):
					while query.next():
						self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
						valor=self.ui.tableWidget.rowCount()-1
						for ind in range(0,9):		
							item=QtGui.QTableWidgetItem()
							if ind <> 8:
								item.setText(query.value(ind).toString())
								self.ui.tableWidget.setItem(valor,ind,item)
							else:
								botones.append(QtGui.QPushButton(""))
								icon = QtGui.QIcon("/usr/usr/share/MonitoreoRadio/Play-Normal-icon.png")
								botones[valor].setIcon(icon)
								self.ui.tableWidget.setCellWidget(valor,ind,botones[valor])
								QtCore.QObject.connect(botones[valor],QtCore.SIGNAL("clicked()"), self.pulsa)
							self.ui.tableWidget.resizeColumnsToContents()

			elif len(str(self.ui.comboBox_2.currentText())) == 0 and len(str(self.ui.comboBox.currentText())) == 0 and len( str(self.ui.comboBox_3.currentText())) == 0:
				query = QSqlQuery(db)	
				if query.exec_("SELECT g.fecha,g.hora,g.codigo,u.nombre,u.apellido,u.cargo,j.Nombre,g.audio FROM radios_nombre j, radios_grabacion g LEFT OUTER JOIN usuarios u ON g.codigo=u.codigo where j.Nombre=g.radio %s" % queryFecha):

					while query.next():
						#print "Bien"
						self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
						valor=self.ui.tableWidget.rowCount()-1
						for ind in range(0,9):		
							item=QtGui.QTableWidgetItem()
							if ind <> 8:
								item.setText(query.value(ind).toString())
								self.ui.tableWidget.setItem(valor,ind,item)
							else:
								botones.append(QtGui.QPushButton(""))
								icon = QtGui.QIcon("/usr/usr/share/MonitoreoRadio/Play-Normal-icon.png")
								botones[valor].setIcon(icon)
								self.ui.tableWidget.setCellWidget(valor,ind,botones[valor])
								QtCore.QObject.connect(botones[valor],QtCore.SIGNAL("clicked()"), self.pulsa)
							self.ui.tableWidget.resizeColumnsToContents()

			else:
				query = QSqlQuery(db)
				if len(str(self.ui.comboBox_2.currentText())) > 0 or len(str(self.ui.comboBox.currentText())) > 0 or len( str(self.ui.comboBox_3.currentText())) > 0:
					if  len(str(self.ui.comboBox.currentText())) == 0 and len(str(self.ui.comboBox_2.currentText())) > 0 and len(str(self.ui.comboBox_3.currentText())) == 0:
						query.exec_("SELECT g.fecha,g.hora,g.codigo,u.nombre,u.apellido,u.cargo,j.Nombre,g.audio FROM radios_nombre j, radios_grabacion g LEFT OUTER JOIN usuarios u ON g.codigo=u.codigo where j.Nombre=g.radio and g.codigo='%s' %s" % (str(self.ui.comboBox_2.currentText()),queryFecha))
					elif len(str(self.ui.comboBox.currentText())) > 0 and len(str(self.ui.comboBox_2.currentText())) == 0 and len(str(self.ui.comboBox_3.currentText())) == 0:
						query.exec_("SELECT g.fecha,g.hora,g.codigo,u.nombre,u.apellido,u.cargo,j.Nombre,g.audio FROM radios_nombre j, radios_grabacion g LEFT OUTER JOIN usuarios u ON g.codigo=u.codigo where j.Nombre='%s' and j.Nombre=g.radio %s" % (str(self.ui.comboBox.currentText()),queryFecha))
					else:
						if len(str(self.ui.comboBox.currentText())) == 0 and len(str(self.ui.comboBox_2.currentText())) == 0 and len(str(self.ui.comboBox_3.currentText())) > 0:					
							 
							query.exec_("SELECT g.fecha,g.hora,g.codigo,u.nombre,u.apellido,u.cargo,j.Nombre,g.audio FROM radios_nombre j, radios_grabacion g LEFT OUTER JOIN usuarios u ON g.codigo=u.codigo where u.cargo='%s' and j.Nombre=g.radio %s" % (str(self.ui.comboBox_3.currentText()),queryFecha))

#---------------------------------------------------------------------------------------------------------------------------------------------------------

					if  len(str(self.ui.comboBox.currentText())) > 0 and len(str(self.ui.comboBox_2.currentText())) > 0 and len(str(self.ui.comboBox_3.currentText())) == 0:
						query.exec_("SELECT g.fecha,g.hora,g.codigo,u.nombre,u.apellido,u.cargo,j.Nombre,g.audio FROM radios_nombre j, radios_grabacion g LEFT OUTER JOIN usuarios u ON g.codigo=u.codigo where j.Nombre='%s' and g.codigo='%s' and j.Nombre=g.radio %s" % (str(self.ui.comboBox.currentText()),str(self.ui.comboBox_2.currentText()),queryFecha))
					elif len(str(self.ui.comboBox.currentText())) > 0 and len(str(self.ui.comboBox_2.currentText())) == 0 and len(str(self.ui.comboBox_3.currentText())) > 0:
						query.exec_("SELECT g.fecha,g.hora,g.codigo,u.nombre,u.apellido,u.cargo,j.Nombre,g.audio FROM radios_nombre j, radios_grabacion g LEFT OUTER JOIN usuarios u ON g.codigo=u.codigo where j.Nombre='%s' and j.Nombre=g.radio and u.cargo='%s' %s" % (str(self.ui.comboBox.currentText()),str(self.ui.comboBox_3.currentText()),queryFecha))
					else:
						if len(str(self.ui.comboBox.currentText())) == 0 and len(str(self.ui.comboBox_2.currentText())) > 0 and len(str(self.ui.comboBox_3.currentText())) > 0:					
							query.exec_("SELECT g.fecha,g.hora,g.codigo,u.nombre,u.apellido,u.cargo,j.Nombre,g.audio FROM radios_nombre j, radios_grabacion g LEFT OUTER JOIN usuarios u ON g.codigo=u.codigo where u.cargo='%s' and j.Nombre=g.radio and g.codigo='%s' %s" % (str(self.ui.comboBox_3.currentText()),str(self.ui.comboBox_2.currentText()),queryFecha))
					while query.next():
						#print "Entra"
						self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
						valor=self.ui.tableWidget.rowCount()-1
						for ind in range(0,9):		
							item=QtGui.QTableWidgetItem()
							if ind <> 8:
								item.setText(query.value(ind).toString())
								self.ui.tableWidget.setItem(valor,ind,item)
							else:
								botones.append(QtGui.QPushButton(""))
								icon = QtGui.QIcon("//usr/usr/share/MonitoreoRadio/Play-Normal-icon.png")
								botones[valor].setIcon(icon)
								self.ui.tableWidget.setCellWidget(valor,ind,botones[valor])
								QtCore.QObject.connect(botones[valor],QtCore.SIGNAL("clicked()"), self.pulsa)
							self.ui.tableWidget.resizeColumnsToContents()
																
		
		def busca(self):
			global nombre,codigo,cargo	
			nombre = []
			codigo = []
			cargo = []
			query = QSqlQuery(db)
			if query.exec_("SELECT Nombre FROM radios_nombre"):
				nombre.append("")
				self.ui.comboBox.addItem("")
							
				while query.next():
					nombre.append(str(query.value(0).toString()))
					self.ui.comboBox.addItem(str(query.value(0).toString()))
					self.ui.comboBox_4.addItem(str(query.value(0).toString()))
			if query.exec_("SELECT distinct codigo FROM usuarios"):
				codigo.append("")
				self.ui.comboBox_2.addItem("")
				#codigo.append("Desconocido")
				#self.ui.comboBox_2.addItem("Desconocido")
				while query.next():
					codigo.append(str(query.value(0).toString()))
					self.ui.comboBox_2.addItem(str(query.value(0).toString()))
			if query.exec_("SELECT distinct cargo FROM usuarios"):
				cargo.append("")
				self.ui.comboBox_3.addItem("")
				while query.next():
					if len(str(query.value(0).toString())) > 0:
						cargo.append(str(query.value(0).toString()))
						self.ui.comboBox_3.addItem(str(query.value(0).toString()))				
		def salir(self):
			db.close()
			self.close()
		def pulsa(self):
			try:
				i = botones.index(self.sender())
    			except ValueError:
				i = -1
			itemEnv=self.ui.tableWidget.item(i,7)					
			Ventana = Reproduce(itemEnv.text())
		def radioA(self):
			self.ui.comboBox_5.clear()
			self.ui.comboBox_6.clear()
			self.ui.comboBox_5.addItem(time.strftime("%Y", time.localtime()))
			self.ui.comboBox_6.addItem(time.strftime("%Y", time.localtime()))
			self.ui.label_10.setVisible(False)
			self.ui.lineEdit.setVisible(False)
		def radioB(self):
			self.ui.comboBox_5.clear()
			self.ui.comboBox_6.clear()
			self.ui.label_10.setVisible(True)
			self.ui.lineEdit.setVisible(True)
			self.ui.lineEdit.setText(time.strftime("%Y", time.localtime()))
			for mes in range(1,13):
				self.ui.comboBox_5.addItem(calendar.month_name[mes].upper())
				self.ui.comboBox_6.addItem(calendar.month_name[mes].upper())
    

		def bar_graph(self,name_value_dict,meses2, graph_title='', output_name='grafica.png'):
			figure(figsize=(10, 5)) # image dimensions  
			title(graph_title, size='x-small')
			#print name_value_dict.keys()
			# add bars
			valores = []
			for i, key in enumerate(meses2):
				bar(i + 0.15 , name_value_dict[key], color='red')
				valores.append(name_value_dict[key])	
			valores2 = []			
			for i in range(0,len(valores)):
				valores2.append(meses2[i] + ":" + str(valores[i]))	 
			#print valores2
			# axis setup
			xticks(arange(0.55, len(name_value_dict)),
			['%s' % (kv) for kv in valores2],
			size='xx-small')
			max_value = max(name_value_dict.values()) + 7
			tick_range = arange(0, max_value, (max_value / 7))
			yticks(tick_range, size='xx-small')
			formatter = FixedFormatter([str(x) for x in tick_range])
			gca().yaxis.set_major_formatter(formatter)
			gca().yaxis.grid(which='major')
			savefig(output_name)
			img=QtGui.QPixmap('grafica.png')
			self.ui.label_7.setPixmap(img)

		def consulta(self):
			if self.ui.radioButton.isChecked()==False:
				my_dict = {'Enero': 0}
				meses2 = []
				inicio = self.ui.comboBox_5.currentIndex() + 1
				final = self.ui.comboBox_6.currentIndex() + 1
				if final >= inicio:
					query = QSqlQuery(db)
					del my_dict['Enero']
					for meses in range(inicio,final+1):
						print meses
						quer="SELECT count(fecha) FROM radios_grabacion where radio='" + str(self.ui.comboBox_4.currentText()) +  "' and month(fecha)=" + str(meses ) + " and year(fecha)=" + self.ui.lineEdit.text()	
						#print quer
						if query.exec_(quer):				
							while query.next():
								mesNomb=calendar.month_name[meses].upper()
								#print mesNomb
								if mesNomb <> '':
									meses2.append(mesNomb)
									llamada=int(query.value(0).toString())
									#print llamada	
									my_dict[mesNomb] = llamada
						 			
					if '' in my_dict:					
						del my_dict['']
					#print my_dict			
					self.bar_graph(my_dict,meses2, graph_title='Numero de LLamadas') 
			else:
				self.consulta2()
	
		def consulta2(self):
			my_dict = {'Enero': 0}
			a_nos2 = []
			inicio = int(self.ui.comboBox_5.currentText())
			final  = int(self.ui.comboBox_6.currentText())
			if final >= inicio:
				query = QSqlQuery(db)
				del my_dict['Enero']
				for meses in range(inicio,final+1):
					quer="SELECT count(fecha) FROM radios_grabacion where radio='" + str(self.ui.comboBox_4.currentText()) +  "' and year(fecha)=" + str(meses)
					if query.exec_(quer):				
						while query.next():
							mesNomb=str(meses)
							llamada=int(query.value(0).toString())	
							my_dict[mesNomb] = llamada
							if mesNomb <> '':
								a_nos2.append(str(mesNomb)) 
					 			
				if '' in my_dict:					
					del my_dict['']
				#print my_dict			
				self.bar_graph(my_dict,a_nos2, graph_title='Numero de LLamadas') 	
		def radioC(self):
			if self.ui.radioButton_3.isChecked() == True:
				self.ui.dateEdit.setVisible(True)
				self.ui.dateEdit_2.setVisible(True)
				self.ui.label_3.setVisible(True)
				self.ui.label_5.setVisible(True)
				queryFecha = " and fecha >= '" + self.ui.dateEdit.date().toString("yyyy-MM-dd") + \
				"' and fecha <= '" + self.ui.dateEdit_2.date().toString("yyyy-MM-dd") + "'"
				self.ui.label_11.setText(queryFecha)
			else:
				self.ui.dateEdit.setVisible(False)
				self.ui.dateEdit_2.setVisible(False)
				self.ui.label_3.setVisible(False)
				self.ui.label_5.setVisible(False)
				queryFecha = ""
				self.ui.label_11.setText(queryFecha)
		
		def cambioFecha(self, fecha):
			queryFecha = " and fecha >= '" + self.ui.dateEdit.date().toString("yyyy-MM-dd") + \
			"' and fecha <= '" + self.ui.dateEdit_2.date().toString("yyyy-MM-dd") + "'"
			self.ui.label_11.setText(queryFecha)
			
		def cambioFecha2(self, fecha2):
			queryFecha = " and fecha >= '" + self.ui.dateEdit.date().toString("yyyy-MM-dd") + \
			"' and fecha <= '" + self.ui.dateEdit_2.date().toString("yyyy-MM-dd") + "'"
			self.ui.label_11.setText(queryFecha)			

		def centrar(self):
			screen = QtGui.QDesktopWidget().screenGeometry()
			size =  self.geometry()
			self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

