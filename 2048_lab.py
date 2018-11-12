'''
Created on 4 nov. 2018

@author: Arvid
'''

import numpy as np
import matplotlib as plt
import random
import msvcrt
import time
import sys
import tkinter as tk
from builtins import print
from unicodedata import bidirectional

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class game_of_2048:
    def __init__(self):
        self.initiate_board()
        
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    
    def initiate_board(self):
        random.seed()
        
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.insert_brick()
    
    def insert_brick(self):
        if 0 in self.board:
            random_brick = random.randint(0,15)
            
            while (self.board[random_brick] != 0):
                random_brick = random.randint(0,15)
                
            insert_value = 2 if (random.random() > 0.1) else 4
            self.board[random_brick] = insert_value
            self.print_board()
        else:
            self.print_board()
            print('game lost')
            quit(0)
    
    def print_board(self):
        for i in range(4):
            print(self.board[4 * i:4 * (i + 1)])
        print('---------')
        
    def move(self, direction): 
        self.rotate(direction)
        self.pack_n_merge()
        self.rotate(-1 * direction)
        self.insert_brick()
        
    def pack_n_merge(self):
        self.pack()
        self.merge() 
        self.pack()
    
    def pack(self):
        for column in range(4):
            for repetitions in range(3):
                for row in range(3):
                    if self.board[4 * row + column] == 0:
                        self.board[4 * row + column] = self.board[4 * (row + 1) + column]
                        self.board[4 * (row + 1) + column] = 0
                        
    def merge(self):
        for column in range(4):
            for row in range(3):
                if self.board[4 * row + column] == self.board[4 * (row + 1) + column]:
                    self.board[4 * row + column] *= 2
                    self.board[4 * (row + 1) + column] = 0
                        
    def rotate(self, direction):
        if direction < 0:
            direction += 4
             
        newBoard = []
        if direction == UP:
            newBoard = self.board
        elif direction == LEFT: #90 degrees clockwise
            for column in range(4):
                for row in range(4):
                    newBoard.append(self.board[4 * (3 - row) + column])
        elif direction == DOWN: # Down
            for i in range(16):
                newBoard.append(self.board[15-i])
        elif direction == RIGHT: #90 degrees ccw
            for column in range(4):
                for row in range(4):
                    newBoard.append(self.board[4 * row + (3 - column)])
        else:
            print('impossible move, direction:', direction)
            quit(0)
        
        self.board = newBoard 
    

    
def main():
    board = game_of_2048()
    
    def make_a_move(event):
        key = event.char
        
        #print(key, ord(key))
        
        if ord(key) is ord('w'):
            print('up')
            board.move(UP)
        elif ord(key) is ord('s'):
            print('down')
            board.move(DOWN)
        elif ord(key) is ord('d'):
            print('right')
            board.move(RIGHT)
        if ord(key) is ord('a'):
            print('left')
            board.move(LEFT)
        else:
            print('error:', key)
    
    def callback(event):
        frame.focus_set()
        print('clicked at', event.x, event.y)
        
    root = tk.Tk()
    frame = tk.Frame(root, width=200, height=200)

    frame.bind('<Key>', make_a_move)
    frame.bind('<Button-1>', callback)
    frame.pack()
    frame.bind

    root.mainloop()

    print('quit')

main()
 

