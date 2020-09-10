#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import sys, os, thread, time
import pygtk, gtk, gobject
import pygst
import gst

class Reproduce(gtk.Window):

	def __init__(self,archivo):
		self.PLAY_IMAGE = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_BUTTON)
    		self.PAUSE_IMAGE = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_BUTTON)	
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Reproductor")
		window.set_position(gtk.WIN_POS_CENTER)
		window.set_default_size(500, -1)
		#window.connect("destroy", self.on_destroy,"WM destroy")
		window.set_icon_from_file("/usr/usr/share/MonitoreoRadio/logo2.png")
		vbox = gtk.VBox()
		window.add(vbox)
		self.entry = gtk.Entry()
		self.entry.set_text(str(archivo))
		vbox.pack_start(self.entry, False)

		adj1 = gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0)		
		self.scale=gtk.HScale(adj1)
		vbox.pack_start(self.scale, True, True, 0)
		self.scale.set_draw_value(False)
		self.scale.connect('value-changed', self.on_scale_change)
		window.connect('destroy', self.on_destroy)
		hbox = gtk.HBox()
		vbox.add(hbox)
		buttonbox = gtk.HButtonBox()
		hbox.pack_start(buttonbox, False)
		self.play_button = gtk.Button()
		self.play_button.set_image(self.PLAY_IMAGE)
		self.play_button.connect('clicked', self.on_play)
		buttonbox.add(self.play_button)
		self.time_label = gtk.Label()
		self.time_label.set_text("00:00 / 00:00")
		hbox.add(self.time_label)
		window.show_all()
		self.playbin = gst.element_factory_make('playbin2')
        	self.playbin.set_property('uri', 'file:' + str(archivo))
        	self.bus = self.playbin.get_bus()
        	self.bus.add_signal_watch()
        	self.bus.connect("message::eos", self.on_finish)
        	self.is_playing = False
		gobject.threads_init()		

    	def on_finish(self, bus, message):

		t = message.type
		if t == gst.MESSAGE_EOS:
			self.play_thread_id = None
			self.playbin.set_state(gst.STATE_NULL)
			self.play_button.set_image(self.PLAY_IMAGE)
			self.time_label.set_text("00:00 / 00:00")
        		self.is_playing = False
        		self.playbin.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 0)
        		self.scale.set_value(0)
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.play_thread_id = None
			self.playbin.set_state(gst.STATE_NULL)
			self.play_button.set_image(self.PLAY_IMAGE)
			self.time_label.set_text("00:00 / 00:00")

    	def on_destroy(self, window):
        	# NULL state allows the pipeline to release resources
		self.play_button.set_image(self.PLAY_IMAGE)
        	self.playbin.set_state(gst.STATE_NULL)
        	self.is_playing = False
        	#gtk.main_quit()

    	def on_play(self, button):
        	if not self.is_playing:
            		self.play_button.set_image(self.PAUSE_IMAGE)
            		self.is_playing = True
            		self.playbin.set_state(gst.STATE_PLAYING)
            		gobject.timeout_add(100, self.update_scale)
			self.play_thread_id = thread.start_new_thread(self.play_thread, ())

        	else:
			self.play_thread_id = None            		
			self.play_button.set_image(self.PLAY_IMAGE)
            		self.is_playing = False
            		self.playbin.set_state(gst.STATE_PAUSED)

    	def on_scale_change(self, scale):
        	seek_time_secs = scale.get_value()
        	self.playbin.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_KEY_UNIT, seek_time_secs * gst.SECOND)

    	def update_scale(self):
        	if not self.is_playing:
            		return False # cancel timeout

        	try:
            		nanosecs, format = self.playbin.query_position(gst.FORMAT_TIME)
            		duration_nanosecs, format = self.playbin.query_duration(gst.FORMAT_TIME)

            		# block seek handler so we don't seek when we set_value()
            		self.scale.handler_block_by_func(self.on_scale_change)

            		self.scale.set_range(0, float(duration_nanosecs) / gst.SECOND)
            		self.scale.set_value(float(nanosecs) / gst.SECOND)

            		self.scale.handler_unblock_by_func(self.on_scale_change)

        	except gst.QueryError:
            	# pipeline must not be ready and does not know position
         		pass

        	return True # continue calling every 30 milliseconds

	def play_thread(self):
		play_thread_id = self.play_thread_id
		gtk.gdk.threads_enter()
		#self.time_label.set_text("00:00 / 00:00")
		gtk.gdk.threads_leave()
		while play_thread_id == self.play_thread_id:
			try:				
				time.sleep(0.2)
				dur_int = self.playbin.query_duration(gst.FORMAT_TIME, None)[0]
				try:
					pos_int = self.playbin.query_position(gst.FORMAT_TIME, None)[0]
					pos_str = self.convert_ns(pos_int)

				except:
					pass
				if dur_int == -1:
					continue
				dur_str = self.convert_ns(dur_int)
				gtk.gdk.threads_enter()
				self.time_label.set_text(pos_str + " / " + dur_str)
				gtk.gdk.threads_leave()
				break
			except:
				pass
				
		time.sleep(0.2)
		while play_thread_id == self.play_thread_id:
			try:
				pos_int = self.playbin.query_position(gst.FORMAT_TIME, None)[0]
				pos_str = self.convert_ns(pos_int)
			except:
				pass
			if play_thread_id == self.play_thread_id:
				gtk.gdk.threads_enter()
				self.time_label.set_text(pos_str + " / " + dur_str)
				gtk.gdk.threads_leave()
			time.sleep(1)
		
	def convert_ns(self, t):
		# This method was submitted by Sam Mason.
		# It's much shorter than the original one.
		s,ns = divmod(t, 1000000000)
		m,s = divmod(s, 60)
		if m < 60:
			return "%02i:%02i" %(m,s)
		else:
			h,m = divmod(m, 60)
			return "%i:%02i:%02i" %(h,m,s)	
	gtk.gdk.threads_init()	
	
