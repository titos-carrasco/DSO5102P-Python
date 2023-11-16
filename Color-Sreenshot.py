#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import cv2
import os

from rcr.dso5102p.DSO5102P import DSO5102P

def main():
    dso = DSO5102P(  0x049f, 0x505a, False )

    print( 'Getting the screenshot' )
    r = dso.Screenshot()
      
    print( 'Converting image...' )
    im = np.zeros((480,800,3))
    for h in range(0,r.shape[0]):
        for v in range(0,r.shape[1]):
            Pixel = r[h,v]
            match Pixel:
               # color comments based on GUI color = Black setting
               # only tested Black and Blue GUI color setting
               case 0 | 160 | 108:  #black background
                  im[h,v,0] = 0
                  im[h,v,1] = 0
                  im[h,v,2] = 0
               case 224 | 102 | 198 | 64: ##CH1, DC/AC indication bottom bar yellow
                  im[h,v,0] = 0
                  im[h,v,1] = 255
                  im[h,v,2] = 255
               case 170 | 147: #bottom bar darker grey
                  im[h,v,0] = 85
                  im[h,v,1] = 85
                  im[h,v,2] = 85
               case 174: #right menu lighter grey
                  im[h,v,0] = 118
                  im[h,v,1] = 118
                  im[h,v,2] = 118
               case 255 | 115 | 217 | 223 | 230 | 249:   #CH2 blue
                  im[h,v,0] = 255   #blue
                  im[h,v,1] = 255   #green
                  im[h,v,2] = 0     #red
               case 251: #border menu right, border signal window even lighter grey
                  im[h,v,0] = 220
                  im[h,v,1] = 220
                  im[h,v,2] = 220
               case 215: #frame shadow light grey
                  im[h,v,0] = 190
                  im[h,v,1] = 190
                  im[h,v,2] = 190
               case 4: #frame shadow dark grey
                  im[h,v,0] = 34
                  im[h,v,1] = 34
                  im[h,v,2] = 34
               case 44: #button shadow grey
                  im[h,v,0] = 100
                  im[h,v,1] = 100
                  im[h,v,2] = 100
               case 31: #math color purple
                  im[h,v,0] = 255
                  im[h,v,1] = 0
                  im[h,v,2] = 255
               case 140 | 6 | 12:  #bottom bar bandwidth limit indicator
                  im[h,v,0] = 0
                  im[h,v,1] = 0
                  im[h,v,2] = 255
               case 121 | 127 | 57:  #printer icon, cursor indicator border light blue
                  im[h,v,0] = 155
                  im[h,v,1] = 207
                  im[h,v,2] = 155
               case 125:  #menu right X icon, white
                  im[h,v,0] = 255
                  im[h,v,1] = 255
                  im[h,v,2] = 255
               case 128:  #X icon, red
                  im[h,v,0] = 0
                  im[h,v,1] = 0
                  im[h,v,2] = 255
               case 130:  #channel/slope indicator left top menu dark grey
                  im[h,v,0] = 18
                  im[h,v,1] = 18
                  im[h,v,2] = 18
               case 134:  #border period top right, dark grey
                  im[h,v,0] = 50
                  im[h,v,1] = 50
                  im[h,v,2] = 50
               case 19: #purple
                  im[h,v,0] = 155
                  im[h,v,1] = 0
                  im[h,v,2] = 54
               case 192: #selected menu item red
                  im[h,v,0] = 0
                  im[h,v,1] = 154
                  im[h,v,2] = 255
               case 204 | 96: #yellow-grey
                  im[h,v,0] = 0
                  im[h,v,1] = 173
                  im[h,v,2] = 173
               case 211: #light grey
                  im[h,v,0] = 155
                  im[h,v,1] = 155
                  im[h,v,2] = 155
               case 254: #almost white/blue cursor indicator text
                  im[h,v,0] = 246 #blue
                  im[h,v,1] = 255 #green
                  im[h,v,2] = 255 #red
               case 32 | 38: #red top menu time/base indicator
                  im[h,v,0] = 0
                  im[h,v,1] = 101
                  im[h,v,2] = 255
               case 40: #menu title bar background, disabled feature dark grey
                  im[h,v,0] = 65
                  im[h,v,1] = 65
                  im[h,v,2] = 65
               case 63: #cursor indicator background blue
                  im[h,v,0] = 255
                  im[h,v,1] = 101
                  im[h,v,2] = 54
               case 81: #button shadow top light gray
                  im[h,v,0] = 138
                  im[h,v,1] = 138
                  im[h,v,2] = 138
               case 85 | 51: #menu title bar border
                  im[h,v,0] = 172
                  im[h,v,1] = 172
                  im[h,v,2] = 172
               case _:
                  print('unmapped pixel value:')     # 243 159   
                  print(Pixel)
                  im[h,v,0] = 0
                  im[h,v,1] = 0
                  im[h,v,2] = 0
    im = im.astype(np.uint8)
    
    print( 'Saving ...' )
    #cv2.imwrite( 'greyscale.png', r )   #greyscale
    cv2.imwrite( 'screenshot.png', im )  #color

main()
