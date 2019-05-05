#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import cv2
from rcr.dso5102p.DSO5102P import DSO5102P

def main():
    dso = DSO5102P(  0x049f, 0x505a, False )

    print( 'Getting the screenshot' )
    r = dso.Screenshot()

    print( 'Saving ...' )
    st = dso.ReadSystemTime()
    cv2.imwrite( './screenshot/' + st + '.png', r )

    print( 'Press ESC to exit ...' )
    cv2.imshow( st, r )
    while( cv2.waitKey(5) != 27 ):
        pass
    cv2.destroyAllWindows()

# show time
main()
