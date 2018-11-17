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

#color_scheme = ['gray', 'light gray', 'beige', 'dark orange', 'brown', 'dark red', 'red', 'purple']
# TODO: Better colors!
#color_scheme = ['grey', 'light grey', 'light yellow', 'orange', 'red', 'purple', 'blue', 'green', 
#                'dark green', 'dark blue', 'purple', 'dark red', 'yellow']


color_scheme = ['grey', 'tomato', '#fdaa48', '#fffe7a', 'OliveDrab1', 'green2', '#56fca2', 'DodgerBlue2', 'orchid1',
                '#ff000d', '#ff5b00', 'yellow', '#01ff07', 'blue2', '#7e1e9c', '#fe01b1'] 
# To reach 2048 11 colors are needed except grey and black

def initiate_frames(outer_frame):
        frame_list = []
        for i in range(16):
            frame = tk.Frame(outer_frame, width=100, height=100)
            row_idx = i // 4
            column_idx = i % 4
            frame.grid(row = row_idx, column = column_idx)
            frame_list.append(frame)
        return frame_list
    
def get_dir_from_char(char):
            if char is ord('w'): return UP
            elif char is ord('s'): return DOWN
            elif char is ord('d'): return RIGHT
            elif char is ord('a'): return LEFT
            else: return 
            
class game_of_2048:
    def __init__(self):
        self.initiate_board()
        
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
        else:
            print('game lost')
            quit(0)
        
    def move(self, direction): 
        old_board = self.board
        self.rotate(direction)
        self.pack_n_merge()
        
        if self.changes_made:
            self.rotate(-1 * direction)
            self.insert_brick()
            
            #TODO: Check if game over 
            return True
        else:
            self.board = old_board
            return False
        
    def pack_n_merge(self):
        self.changes_made = False
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
                        
                        if self.board[4 * row + column] != 0:
                            self.changes_made = True
                            
                        
    def merge(self):
        for column in range(4):
            for row in range(3):
                if self.board[4 * row + column] != 0:
                    if self.board[4 * row + column] == self.board[4 * (row + 1) + column]:
                        self.board[4 * row + column] *= 2
                        self.board[4 * (row + 1) + column] = 0
                        self.changes_made = True
                        
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
    
    def put_numbers(self, frame_list, text_list):
        
        for i in range(16):
            text_list[i].pack_forget()
            #frame_list[i].pack_forget()
            board_value = self.board[i]
            frame_color = (color_scheme[0] if board_value is 0 else  color_scheme[int(np.log2(board_value))])
            
            text_list[i].delete('1.0', tk.END)
            text_list[i].insert(tk.END, '\n  ')
            text_list[i].config(bg = frame_color)
            text_list[i].insert(tk.END, str(board_value))
            text_list[i].pack()
                
        
        return
    
def main():
    board = game_of_2048()
    
    def make_a_move(event):
        dir = get_dir_from_char(ord(event.char))
        
        if dir in [UP, DOWN, LEFT, RIGHT]:
            board.move(dir)
        else:
            print('error:', ord(event.char))
            
        repaint()
        
    def repaint():
        outer_frame.pack_forget()
        board.put_numbers(frame_list, text_list)
        outer_frame.pack()
        
    
    root = tk.Tk()
    root.bind('<Key>', make_a_move)
    outer_frame = tk.Frame(root, width=400, height=400)
    
    frame_list = initiate_frames(outer_frame)
    
    text_list = []
    for i in range(16): text_list.append(tk.Text(frame_list[i], height=3, width=7))
    
    board.board = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 2*4096, 4*4096, 8*4096]
    
    repaint()
    
    root.mainloop()

    print('quit')

main()
 
# def callback(event):
#     frame.focus_set()
#     print('clicked at', event.x, event.y)
