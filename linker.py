#!/usr/bin/env python

import pygtk
pygtk.require( '2.0' )
import gtk
import re
import os
import sys
import urllib
import platform

class Linker:
	def delete_event( self, widget, data = None ):
		return False

	def show_link( self, widget, data = None ):
		# get all text in the textview widget
		buffer = self.textView.get_buffer()
		start = buffer.get_iter_at_offset( 0 )
		end = buffer.get_iter_at_offset( buffer.get_char_count() )
		#print buffer.get_text( start, end )

		# processing the text to obtain all link
		text = buffer.get_text( start, end )

		links = []
		links_text = ''
		# print text
		for link in text.split( "\n" ):
			link = link.strip()
			if( re.match( "^[http|www]", link ) ):
				special_chars = [ '(', ')', '&', ';' ]
				for char in special_chars:
					link = link.replace( char, '\\' + char )
				print link
				links.append( link )
				links_text += ' ' + link

		# open url 
		if platform.system() == 'Windows':
			for link in links:
				os.system( 'rundll32 url.dll,FileProtocolHandler ' + link )
		elif platform.system() == 'Linux' and os.path.exists( '/etc/redhat-release' ):
			for link in links:
				os.system( "xdg-open " + link )
		elif platform.system() == 'Linux' and os.path.exists( '/etc/debian_version' ):
			for link in links:
				os.system( "sensible-browser " + link )


	def destroy( self, widget, data = None ):
		gtk.main_quit()

	def __init__( self ):
		self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )

		self.window.connect( "delete_event", self.delete_event )
		self.window.connect( "destroy", self.destroy )

		# setup window settings
		self.window.set_border_width( 10 )
		self.window.set_resizable( True )
		self.window.set_title( "linker" )
		self.window.set_size_request( 200, 500 )

		# setup text view settings
		self.textView = gtk.TextView()
		self.textView.set_editable( True )
		self.textView.set_cursor_visible( True )
		self.textView.set_size_request( 200, 450 )

		# setup scroll window settings
		self.sw = gtk.ScrolledWindow()
		self.sw.set_policy( gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC )
		self.sw.add( self.textView )

		# setup button settings
		self.button = gtk.Button( "Show" )
		self.button.connect( "clicked", self.show_link, None )

		# setup vbox settings
		self.vbox = gtk.VBox( False, 0 )
		self.vbox.pack_start( self.sw )
		self.vbox.pack_end( self.button )

		self.window.add( self.vbox )
		tb = self.textView.get_buffer()

		self.button.show()
		self.textView.show()
		self.sw.show()
		self.vbox.show()
		self.window.show()
	
	def main( self ):
		gtk.main()

if __name__ == "__main__":
	lk = Linker()
	lk.main()
