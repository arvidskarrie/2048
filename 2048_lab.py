'''
Created on 4 nov. 2018

@author: Arvid
'''

import numpy as np
import matplotlib.pyplot as plt
import random
import msvcrt
import time
import sys
import tkinter as tk
from builtins import print
from unicodedata import bidirectional

    
def main():
    
    def callback(event):
        frame.focus_set()
        print('clicked at', event.x, event.y)
        
    def initiate_frames():
        
        frameList = []
        
        for i in range(16):
            frame = tk.Frame(outer_frame, width=100, height=100)
            
            row_idx = i // 4
            column_idx = i % 4
            frame.grid(row = row_idx, column = column_idx)
            
            frameList.append(frame)
            
        return frameList
        
    root = tk.Tk()
    outer_frame = tk.Frame(root, width=400, height=400)
    
    frameList = initiate_frames()

    frameList[3].configure(background='blue')
    frameList[8].configure(background='red')
    outer_frame.pack()
    
    root.mainloop()

    print('quit')

main()
 

