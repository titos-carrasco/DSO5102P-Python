#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time
from rcr.dso5102p.DSO5102P import DSO5102P

def main():
    dso = DSO5102P(  0x049f, 0x505a, False )

    print( 'Listing /*.inf' )
    r = dso.RemoteShell( 'ls /*.inf' )
    print( r )


    print( 'Getting keyprotocol.inf' )
    r = dso.ReadFile( '/keyprotocol.inf' )
    f=open( './inf/keyprotocol.inf', 'w' )
    f.write( r )
    f.close()

    print( 'Getting protocol.inf' )
    r = dso.ReadFile( '/protocol.inf' )
    f=open( './inf/protocol.inf', 'w' )
    f.write( r )
    f.close()

    print( 'Getting sys.inf' )
    r = dso.ReadFile( '/sys.inf' )
    f=open( './inf/sys.inf', 'w' )
    f.write( r )
    f.close()


# show time
main()
