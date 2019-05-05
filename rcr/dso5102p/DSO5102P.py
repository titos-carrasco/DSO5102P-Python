# -*- coding: utf-8 -*-
#
# Thanks to:
#   https://elinux.org/Das_Oszi_Protocol (protocolo)
#   https://randomprojects.org/wiki/Voltcraft_DSO-3062C (uso de usb)
#
# My DSO5102P has idVendor=0x049f and idProduct=0x505a
#
#--

import usb
import serial
import time
import array

import cv2
import numpy as np


class DSO5102P():
    def __init__( self, idVendor, idProduct, debug=False ):
        self.debug = debug
        self.dev = usb.core.find( idVendor=idVendor, idProduct=idProduct )
        if( self.dev is None ):
            print( 'DSO5102P Ne Encontrado' )
            exit()

        # unooad de 'cdc_subset'
        if( self.dev.is_kernel_driver_active( 0 ) ):
            self.dev.detach_kernel_driver( 0 )

        # limpia buffers
        time.sleep( 0.1 )
        try:
            while( True ):
                r = self.dev.read( 0x81, 1024*1024, 2000 )
                self._dump( 'FLUSH', r[:5] )
        except usb.core.USBError:
            pass

    def _dump( self, origin, data ):
        if( self.debug ):
            print( origin, ':',  [ '0x%02X' % h for h in data ] )

    def _SendCommand( self, origin, cmd, data, debug=False ):
        assert isinstance( data, array.array ), '\'data\' must be array.array(\'B\')'

        time.sleep( 0.5 )
        action = 0x43 if debug else 0x53
        packetLen = 1 + len( data ) + 1
        packet = array.array( 'B', [ action, packetLen & 0xFF, ( packetLen >> 8 ) & 0xFF, cmd ] ) + data
        packet = packet + array.array( 'B', [ sum( packet ) & 0xFF ] )
        self._dump( origin.upper(), packet[:5] )
        self.dev.write( 0x02, packet )
        return packet

    def _ReadAnswer( self, origin, rcode ):
        r = None
        while( True ):
            r = self.dev.read( 0x81, 1024*1024, 4000 )
            chksum = sum( r[:-1] ) & 0xFF
            if( chksum != r[-1] ):
                self._dump( 'BADCHKSUM', r[:5] )
            if( r[3] == rcode ):
                break
            else:
                self._dump( 'BADANSWER', r[:-5] )
        self._dump( origin, r[:5] )
        return r

    #----

    # OK
    def Echo( self, data ):
        data = array.array( 'B', data )
        self._SendCommand( 'Echo', 0x00, data )
        r = self._ReadAnswer( 'Echo', 0x80 )
        return list( r[4:-1] )

    def ReadSettings( self ):
        self._SendCommand( 'ReadSettings', 0x01, array.array( 'B' ) )
        r = self._ReadAnswer( 'ReadSettings', 0x81 )
        return r[4:-1]

    def ReadSampleData( self, channel ):
        self._SendCommand( 'ReadSampleData', 0x02, array.array( 'B', [ 0x01, channel & 0x01 ] ) )
        r = array.array( 'B' )
        sdlen = 0
        while( True ):
            d = self._ReadAnswer( 'ReadSampleData', 0x82 )
            if( d[4] == 0x00 ):
                sdlen = d[5] + (d[6]<<8) + (d[7]<<16)
            elif( d[4] == 0x01 ):
                r = r + d[6:-1]
            elif( d[4] == 0x02 ):
                # d[6] == channel
                break;
            else:
                # some error
                # d[6] == channel
                break;
        #print( sdlen, len( r ) )
        return r

    # OK
    def ReadFile( self, fname ):
        p = self._SendCommand( 'ReadFile', 0x10, array.array( 'B', bytearray( '\x00' + fname, 'utf8' ) ) )
        r = array.array( 'B' )
        while( True ):
            d = self._ReadAnswer( 'ReadFile', 0x90 )
            if( d[4] == 0x01 ):
                r = r + d[5:-1]
            else:
                # checksum???
                break;
        r = ''.join( [ chr( c ) for c in r ] )
        return r

    # OK
    def LockControlPanel( self, lock ):
        lock = 1 if lock else 0
        self._SendCommand( 'LockControlPanel', 0x012, array.array( 'B', [ 0x01, lock ] ) )
        r = self._ReadAnswer( 'LockControlPanel', 0x92 )

    # OK
    def StartAcquisition( self, start ):
        start = 0 if start else 1
        self._SendCommand( 'StartAcquisition', 0x012, array.array( 'B', [ 0x00, start ] ) )
        r = self._ReadAnswer( 'StartAcquisition', 0x92 )

    # OK
    def KeyTrigger( self, b1, b2 ):
        self._SendCommand( 'KeyTrigger', 0x013, array.array( 'B', [ b1, b2 ] ) )
        r = self._ReadAnswer( 'KeyTrigger', 0x93 )

    # OK
    def Screenshot( self ):
        self._SendCommand( 'Screenshot', 0x20, array.array( 'B' ) )
        r = array.array( 'B' )
        while( True ):
            d = self._ReadAnswer( 'Screenshot', 0xA0 )
            if( d[4] == 0x01 ):
                r = r + d[5:-1]
            else:
                # checksum???
                break;
        r = np.frombuffer( bytearray(r), dtype=np.uint16 ).reshape( 480, 800 )
        return r

    # OK
    def ReadSystemTime( self ):
        self._SendCommand( 'ReadSystemTime', 0x21, array.array( 'B' ) )
        r = self._ReadAnswer( 'ReadSystemTime', 0xA1 )
        r = '%04d-%02d-%02d %02d:%02d:%02d' % ( r[5]*0xFF + r[4] + 7, r[6], r[7], r[8], r[9], r[10] )
        return r

    # OK
    def RemoteShell( self, cmdline ):
        self._SendCommand( 'RemoteShell', 0x11, array.array( 'B', bytearray( cmdline, 'utf8' ) ), True )
        r = self._ReadAnswer( 'RemoteShell', 0x91 )
        r = ''.join( [ chr( c ) for c in r ] )
        return r

