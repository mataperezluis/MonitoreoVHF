#!/usr/bin/env python2.6
import sys, os, random, threading
import gst, gobject, sys, gtk


class gnonlin(object):

	def on_pad(self,gnlcomp, pad):
	   # print "on_pad"
	    PAD_MUTEX.acquire()
	    convpad = adder.get_compatible_pad(pad, pad.get_caps())        
	    pad.link(convpad)
	    PAD_MUTEX.release()
	  #  print "padded", convpad

	def handle_message(self,bus, message):
	    if message.type == gst.MESSAGE_EOS:
	       	# print "trying to quit"
		pipeline.set_state(gst.STATE_PLAYING)
		#print "final"		
		gtk.main_quit()	
				

	def get_comp(self,path, start):
	    """returns a gnlcomposition with the file at some position in a sparse timeline"""

	    comp = gst.element_factory_make("gnlcomposition")

	    # setup silent backing track as default
	    silence = gst.element_factory_make("audiotestsrc")
	    silence.set_property("volume", 0.0)
	    silencesrc = gst.element_factory_make("gnlsource")
	    silencesrc.set_property("priority", 2**32-1) # -1 is not of type guint!
	    silencesrc.add(silence)
	    comp.add(silencesrc)

	    #add file
	    filesrc = gst.element_factory_make("gnlfilesource")
	    filesrc.set_property("location", "file://%s" % (path))
	    filesrc.set_property("start", 0)
	    filesrc.set_property("duration", 2*gst.SECOND)
	    # strange errors without media-start & duration
	    filesrc.set_property("media-start", int(start*gst.SECOND))
	    filesrc.set_property("media-duration", 2*gst.SECOND)

	    comp.add(filesrc)

	    #set on-pad behavior
	    comp.connect("pad-added", self.on_pad)

	    return comp

	def convertir(self,ruta,comienzo,pos):
		gobject.threads_init()
		global pipeline,adder,PAD_MUTEX,bus
		pipeline = gst.Pipeline("mypipeline")
		adder = gst.element_factory_make("adder")

		PAD_MUTEX = threading.Lock()

		bus = pipeline.get_bus()
		bus.enable_sync_message_emission()
		bus.connect("sync-message", self.handle_message)

		many = []
		comp = self.get_comp(ruta, comienzo)
		many.append(comp)

		convert = gst.element_factory_make("audioconvert")
		resample = gst.element_factory_make("audioresample")

		caps = gst.Caps("audio/x-raw-int, channels=1, width=16, rate=8000")
		filt = gst.element_factory_make("capsfilter")
		filt.set_property("caps", caps)

		enc = gst.element_factory_make("wavenc")

		#sink = gst.element_factory_make("alsasink")

		sink = gst.element_factory_make("filesink")
		outloc = "salida_" + str(pos) + ".wav" #os.path.join(bundle.dir, "punch.wav")
		#print pos
		sink.set_property("location", outloc)

		pipeline.add(*many)
		pipeline.add(adder, resample, convert, filt, enc, sink)
		gst.element_link_many(adder, resample, convert, filt, enc, sink)

		pipeline.set_state(gst.STATE_PLAYING)
		gtk.main()

