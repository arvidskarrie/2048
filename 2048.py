'''
Created on 4 nov. 2018

@author: Arvid
'''

import numpy as np
import matplotlib as plt
from datetime import date
import time
import os
import random
import tkinter as tk
from color_scheme import get_color_scheme
from unicodedata import bidirectional

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
UNDO = 5
SAVE = 6
SAVE_LAST = 7
QUIT = 8

color_scheme = get_color_scheme()
    
    
def save_board(board):
    dir = os.path.normpath('C:/Users/Arvid/Documents/GitHub/2048/logs/' + str(date.today()) + '.txt')
    #filename = str(10) #str(datetime.today())
    #file_dir = dir + filename + '.txt'
    
    f = open(dir, 'a')
    d = str(time.strftime('%X'))
    f.write(d + ':\n\n')
    
    
    for i in board:
        f.write(str(i) + '\n')
    
    points = 0
    biggest_brick = 0
    for i in board:
        points += sum(i)
        biggest_brick = max(biggest_brick, max(i))
        
    f.write('\ntotal points:' + str(points) + '\n')
    f.write('biggest brick:' + str(biggest_brick) + '\n')
        
    f.write('\n' + str(board) + '\n')
    f.write('\n----------\n\n')

def print_game_over(board):
    print('game over:')
    for i in board:
        print(i)
        
    points = 0
    biggest_brick = 0
    for i in board:
        points += sum(i)
        biggest_brick = max(biggest_brick, max(i))
        
    print('total points:', points)
    print('biggest brick:', biggest_brick)

def empty_board():
    empty_board = [[0, 0, 0, 0] for i in range(4)]
    return empty_board

def initiate_frames(outer_frame):
        frame_list = []
        text_list = []
        
        for i in range(16):
            frame = tk.Frame(outer_frame, width=100, height=100)
            row_idx = i // 4
            column_idx = i % 4
            frame.grid(row = row_idx, column = column_idx)
            frame_list.append(frame)
            text_list.append(tk.Text(frame_list[i], height=3, width=7))
            text_list[i].tag_configure("center", justify='center')
            
        return frame_list, text_list
    
def get_dir_from_char(char):
            if char is ord('w'): return UP
            elif char is ord('s'): return DOWN
            elif char is ord('d'): return RIGHT
            elif char is ord('a'): return LEFT
            elif char is ord('u'): return UNDO
            elif char is ord('i'): return SAVE
            elif char is ord('o'): return SAVE_LAST
            elif char is ord('p'): return QUIT
            else: return 
            
class game_of_2048:
    def __init__(self):
        self.initiate_board()
        self.last_board = self.board
        
    def initiate_board(self):
        random.seed()
        
        self.board = empty_board()
         
        self.insert_brick()
    
    def insert_brick(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        
        while (self.board[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
            
        insert_value = 2 if (random.random() > 0.1) else 4
        self.board[row][col] = insert_value
        
        if self.is_game_lost():
            print_game_over(self.board)
            
    def is_game_lost(self):
        board = self.board
        
        for row in range(4):
            if 0 in board[row]:
                return False        
        
        for idx_1 in range(3):
            for idx_2 in range(4):
                if board[idx_1][idx_2] == board[idx_1 + 1][idx_2] or board[idx_2][idx_1] == board[idx_2][idx_1 + 1]:
                    return False
                
        return True
            
    def move(self, direction):
        self.rotate(direction)
        self.pack_n_merge()
        self.rotate(-1 * direction)
        
        return self.changes_made
        
    def pack_n_merge(self):
        self.changes_made = False
        self.pack()
        self.merge() 
        self.pack()
    
    def pack(self):
        for column in range(4):
            for repetitions in range(3):
                for row in range(3):
                    if (self.board[row][column] == 0) and (self.board[row + 1][column] != 0):
                        
                        self.board[row][column] = self.board[row + 1][column]
                        self.board[row + 1][column] = 0
                        
                        self.changes_made = True
                        
    def merge(self):
        for column in range(4):
            for row in range(3):
                if self.board[row][column] != 0:
                    if self.board[row][column] == self.board[row + 1][column]:
                        self.board[row][column] *= 2
                        self.board[row + 1][column] = 0
                        self.changes_made = True
                        
    def rotate(self, direction):
        if direction < 0:
            direction += 4
             
        new_board = empty_board()
        old_board = self.board
        
        if direction == UP:
            new_board = old_board
            
        elif direction == LEFT: #90 degrees clockwise
            for row in range(4):
                for column in range(4):
                    new_board[row][column] = old_board[3-column][row]
                    
        elif direction == DOWN: # Down
            for row in range(4):
                for column in range(4):
                    new_board[row][column] = old_board[3-row][3-column]
                    
                
        elif direction == RIGHT: #90 degrees ccw
            for row in range(4):
                for column in range(4):
                    new_board[row][column] = old_board[column][3-row]
        else:
            print('impossible move, direction:', direction)
            quit(0)
        
        self.board = new_board 
    
    def put_numbers(self, text_list):
        for i in range(16):
            text_list[i].pack_forget()
            board_value = self.board[i//4][i%4]
            frame_color = (color_scheme[0] if board_value is 0 else color_scheme[int(np.log2(board_value))])
             
            text_list[i].delete('1.0', tk.END)
            text_list[i].insert(tk.END, '\n ')
            if board_value < 1000:
                text_list[i].insert(tk.END, ' ')
                if board_value < 10:
                    text_list[i].insert(tk.END, ' ')
                
                
            text_list[i].config(bg = frame_color)
            text_list[i].insert(tk.END, str(board_value))
            
            text_list[i].pack()
        return
    
    def detect_warnings(self):
        real_board = self.board
        
        self.move(DOWN)
        board = self.board
        num_zeros = []
        
        for i in board:
            num_zeros.append(i.count(0))
        
        
        warning_list = [[4, 4, 4, 1], [4, 4, 1, 0], [4, 1, 0, 0]]
        
        self.board = real_board
        
        return num_zeros in warning_list
        
def main():
    board = game_of_2048()
    
    def make_a_move(event):
        dir = get_dir_from_char(ord(event.char))
        
        if dir in [UP, DOWN, LEFT, RIGHT]:
            last_board = board.board
            if board.move(dir):
                board.insert_brick()
                board.last_board = last_board
        elif dir is UNDO:
            board.board = board.last_board
            # TODO: implement full undo
        elif dir is SAVE:
            save_board(board.board)
        elif dir is SAVE_LAST:
            save_board(board.last_board)
        elif dir is QUIT:
            print_game_over(board.board)
            quit(0)
        else:
            print('error:', ord(event.char))
        
        repaint()
        
    def repaint():
        outer_frame.pack_forget()
        board.put_numbers(text_list)
        if board.detect_warnings():
            print('warning!')
        outer_frame.pack()
    
    root = tk.Tk()
    root.bind('<Key>', make_a_move)
    outer_frame = tk.Frame(root, width=400, height=400)
    
    frame_list, text_list = initiate_frames(outer_frame)
    
    text_list = []
    for i in range(16): text_list.append(tk.Text(frame_list[i], height=3, width=7))
    
    #board.board = [[0, 2, 4, 2],[ 16, 32, 64, 128],[ 256, 512, 1024, 2048],[ 4096, 2*4096, 4*4096, 8*4096]]
    
    board.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2], [2, 2, 0, 0]]
    
    print('undo: u')
    print('save current: i')
    print('save last: o')
    print('quit: p')
    
    repaint()
    
    root.mainloop()

    print('quit')

main()

