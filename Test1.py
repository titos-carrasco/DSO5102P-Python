#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time
from rcr.dso5102p.DSO5102P import DSO5102P

def main():
    dso = DSO5102P(  0x049f, 0x505a, False )

    r = dso.Echo( [ 1, 2, 3, 4, 5, 6 ] )
    print( 'Echo:', r )

    r = dso.ReadSystemTime()
    print( r )

    # see inf/keyprotocol.inf
    #   [FN-0-KEY] is 0x00, [MENU-ACQUIRE-KEY] is 0x0D and so on
    dso.KeyTrigger( 0x0C, 0x01 )            # MENU-MEASURE-KEY
    time.sleep( 4 )
    dso.KeyTrigger( 0x0D, 0x01 )            # MENU-ACQUIRE-KEY

    print( 'Lock Panel' )
    dso.LockControlPanel( True )
    time.sleep( 5 )
    print( 'Unlock Panel' )
    dso.LockControlPanel( False )

    print( 'Start Acquisition' )
    dso.StartAcquisition( True )
    time.sleep( 5 )
    print( 'Stop Acquisition' )
    dso.StartAcquisition( False )
    time.sleep( 5 )
    print( 'Start Acquisition' )
    dso.StartAcquisition( True )

# show time
main()
