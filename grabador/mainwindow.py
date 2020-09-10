#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
from PyQt4 import uic
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtSql import *
import PyQt4
import PyQt4.Qt as qt
from optparse import OptionParser
import os
import dbus
import gst
import sys
import time
import datetime
import pyaudio
import gobject
import wave
import threading
import alsaaudio, time, audioop
from DTMFdetector import DTMFdetector
from gnonlin import gnonlin
import ogg.vorbis
import math
from kiwi.ui.dialogs import selectfolder as select_folder


NUM_SAMPLES = 1024
SAMPLING_RATE = 8000

(Ui_MainWindow, QMainWindow) = uic.loadUiType('/usr/usr/share/GrabadorRadio/mainwindow.ui')

class MainWindow (QMainWindow):
		"""MainWindow inherits QMainWindow"""
		def __init__ (self, parent=None):
			global homeDir
			QMainWindow.__init__(self, parent)
			homeDir = os.environ['HOME'] + '/Documentos/audio/'
			self.ui = Ui_MainWindow()
			self.ui.setupUi(self)
			self.centrar()
			self.lista_dispositivos()
			oparser = OptionParser()
			oparser.add_option("-f", "--file", dest="path",help="save to FILE", metavar="FILE")
			oparser.add_option("-d", "--device", dest="device",help="Use device DEVICE", metavar="DEVICE")
			(options, args) = oparser.parse_args()
			self.ctimer = QtCore.QTimer()
			self.ctimer2 = QtCore.QTimer()
			self.ui.lineEdit.setText(homeDir)
			self.basedatos(0)
			self.setWindowIcon(QtGui.QIcon('/usr/usr/share/GrabadorRadio/logo2.png'))
			query = QSqlQuery(db)
			if query.exec_("SELECT * FROM radios_nombre"):
				while query.next():
					self.ui.comboBox_2.addItem(query.value(1).toString())
			db.close()
			db.removeDatabase("rad0") 			
			QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"), self.salir)
			QtCore.QObject.connect(self.ui.pushButton_4,QtCore.SIGNAL("clicked()"), self.constant)
			QtCore.QObject.connect(self.ui.pushButton_2,QtCore.SIGNAL("clicked()"), self.ruta)
			QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.constantUpdate)
			QtCore.QMetaObject.connectSlotsByName(self)

			#self.basedatos()
			self.player = gst.element_factory_make('playbin', 'player')
			try:
             # alsasink pulsesink osssink autoaudiosink
				device = gst.parse_launch('alsasink')
			except gobject.GError:
				print 'Error: could not launch audio sink'
			else:
				self.player.set_property('audio-sink', device)
			gobject.threads_init()

		def centrar(self):
			screen = QtGui.QDesktopWidget().screenGeometry()
			size =  self.geometry()
			self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
			
		def lista_dispositivos(self):
			global identifiers
			bus = dbus.SystemBus()
			hal_manager = bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/Manager")
			hal_manager = dbus.Interface(hal_manager, "org.freedesktop.Hal.Manager")

			devices = hal_manager.FindDeviceStringMatch("alsa.type", "capture")
			devices.sort()
			identifiers = []

			for dev in devices:
				device = bus.get_object("org.freedesktop.Hal", dev)

				card = device.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
				if card["alsa.card"] not in identifiers:
					self.ui.comboBox.addItem("%d. %s" % (card["alsa.card"], card["alsa.card_id"]))
					identifiers.append(card["alsa.card"])
			return identifiers
			
		def recslot(self):
			global f,hora,fecha,base,radio
			hora = time.strftime("%H%M%S", time.localtime())
			fecha = time.strftime("%Y%m%d", time.localtime())
			base = str(self.ui.lineEdit.text())
			radio= str(self.ui.comboBox_2.currentText())
			f = base  + fecha + '_' + hora +'.ogg'
			indice=identifiers[self.ui.comboBox.currentIndex()]
			self.record(indice,f)
			
		def record(self,device_id, capture_path):
			
			self.player = gst.parse_launch("""alsasrc device=hw:%d ! audioconvert ! level message=true name=recordlevel interval=10000000 ! audioconvert ! volume volume=1.6 ! vorbisenc ! oggmux ! filesink location=%s""" % (device_id, capture_path))
			#self.ui.label_5.setText("grabando")
			self.player.get_bus().add_signal_watch()
			i = self.player.get_bus().connect('message', self.bus_event)
			self.player.set_state(gst.STATE_PLAYING)
			
		
		def __del__ (self):
			self.ui = None
			
		def constant(self):
			global bien
			bien=0
			#print str(self.ui.comboBox_2.currentIndex())
			if os.path.exists(str(self.ui.lineEdit.text())) == True:
				if len(str(self.ui.comboBox_2.currentText())) > 0:
					self.abrir_inp()
					global db
					db = 0	
					self.basedatos(0)
					self.ctimer.start(0.001)
					bien=1
				else:
					self.ui.label_6.setText("Debe Indicar el Nombre del Radio")
			else:
				self.ui.label_5.setText("Debe Indicar una Ruta Valida")
			
		def basedatos(self,inicio):
			global db
			if inicio == 0:
				base_datos="rad" + str(identifiers[self.ui.comboBox.currentIndex()]) 			
			else:				
				base_datos="Db" + str(identifiers[self.ui.comboBox.currentIndex()]) 
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
		
		def bus_event(self,bus, message):
			peak = message.structure["peak"][0]
			print peak
			if peak>-51 and peak < 1:			
				self.emit( QtCore.SIGNAL( "send( PyQt_PyObject)"), peak)
				
			if peak < self.ui.horizontalSlider_2.value():
				#print peak
				self.player.set_state(gst.STATE_NULL)
				#self.ui.label_5.setText("Terminado")
				#self.ui.label_5.setText("Conectado")
				#self.ui.label_4.setText("")
				query = QSqlQuery(db)
				conv=gnonlin()
				try:
					a = ogg.vorbis.VorbisFile(f)
					t=0
				except:
					t=1
					os.remove(f)
				
				if t == 0:
					a.__methods__
					['bitrate', 'bitrate_instant', 'comment', 'info', 'pcm_seek', 'pcm_seek_page', 'pcm_tell', 'pcm_total', 'raw_seek', 'raw_tell','raw_total', 'read', 'seekable', 'serialnumber', 'streams','time_seek', 'time_seek_page', 'time_tell', 'time_total']				
					if a.time_total(0) >= 1:				
						conv.convertir(f,0,0)
						if a.time_total(0) >= 2:
							tiempo=int(math.floor(a.time_total(0))-2)
						else:
							tiempo=int(math.floor(a.time_total(0))-1)	
						conv.convertir(f,tiempo,1)
						dtmf = DTMFdetector()
						dtmf0= dtmf.getDTMFfromWAV("salida_0.wav")
						if len(dtmf0) == 0:
							dtmf0= dtmf.getDTMFfromWAV("salida_1.wav")
						if len(dtmf0) > 0:
							pass
						else:
							dtmf0="Desconocido"
						p = base + dtmf0 + '_' + fecha + '_' + hora +'.ogg'
						os.rename(f,p)
						query.exec_("INSERT INTO radios_grabacion (codigo, hora, fecha, audio,radio) values('%s', '%s', '%s', '%s', '%s')" % (dtmf0,hora,fecha,p,radio))
						self.emit( QtCore.SIGNAL( "send2( PyQt_PyObject)"), dtmf0)
							#self.ui.label_4.setText(dtmf0)
					else:
						os.remove(f)
						print("Borrado" + f)
				
				self.abrir_inp()
				self.ctimer.start() 
			return True

		def salir(self):
			try:
				inp.close()
			except:
				pass
			try:
				self.player.set_state(gst.STATE_NULL)
			except:
				pass
			try:		
				db.close
			except:
				pass
			self.close()
			QtCore.QObject.disconnect(self.ctimer, QtCore.SIGNAL("timeout()"), self.constantUpdate)
				
			
		def abrir_inp(self):
			global inp
			inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK,str(identifiers[self.ui.comboBox.currentIndex()]))
			#print inp.cardname()
			inp.setchannels(0)
			inp.setrate(8000)
			inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
			inp.setperiodsize(160)
		
		def ruta(self):
			chosen_path = select_folder('Seleccione una Ruta', folder='/start/folder/' )
			self.ui.lineEdit.setText((chosen_path) + '/')	
			self.ui.label_5.setText(" ")	
		
		def ocultar(self):
			
			return bien,self.ui.comboBox.currentIndex(),self.ui.comboBox.currentText()
				
		def constantUpdate(self):
			try:
				l,data = inp.read()
			except:
				inp.close()
				self.abrir_inp()
				l,data = inp.read()
			if l:
				try:
					texto=audioop.max(data, 2)
				except:
					texto=0
					#print "Error"
				print texto
				if int(texto) > (self.ui.horizontalSlider.value()*1.2):				
					inp.close()
					self.recslot()
					self.ctimer.stop()
					
					
			
