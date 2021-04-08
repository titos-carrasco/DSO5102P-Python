#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import cv2
from rcr.dso5102p.DSO5102P import DSO5102P

def main():
    dso = DSO5102P( 0x049f, 0x505a, False )
    running = True
    while( running ):
        img = dso.Screenshot()
        img = cv2.applyColorMap( img, cv2.COLORMAP_HOT )
        cv2.imshow( "DSO5102P", img )
        if( cv2.waitKey(100) == 27 ):
            running = False
    cv2.destroyAllWindows()

# show time
main()
