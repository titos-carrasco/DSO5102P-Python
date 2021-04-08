#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import cv2

import http.server
import socketserver

from rcr.dso5102p.DSO5102P import DSO5102P

class Streamer( http.server.SimpleHTTPRequestHandler ):
    def do_GET(self):
        self.send_response( 200 )
        self.send_header( "Content-type", "multipart/x-mixed-replace; boundary=--boundary" )
        self.end_headers()
        while(True):
            try:
                img = self.dso.Screenshot()
                #img = cv2.applyColorMap( img, cv2.COLORMAP_HOT )
                _, data = cv2.imencode( '.JPEG', img, ( cv2.IMWRITE_JPEG_QUALITY, 80 ) )
                self.wfile.write( b"--boundary\r\n" )
                self.wfile.write( b"Content-Type: image/jpeg\r\n" )
                self.wfile.write( b"Content-length: " + bytes( str( len( data) ).encode() ) )
                self.wfile.write( b"\r\n" )
                self.end_headers()
                self.wfile.write( data )
                self.wfile.write( b"\r\n\r\n\r\n" )
                #time.sleep( 0.100 )
            except Exception as e:
                print( e )
                break


# show time
if __name__ == '__main__':
    try:
        print( "Inicializando DSO5102P" )
        Streamer.dso = DSO5102P( 0x049f, 0x505a, False )

        print( "Levantando HTTP Server" )
        server = socketserver.TCPServer( ('', 8080), Streamer )
        server.serve_forever()
    except Exception as e:
        print( e )

