'''
Created on 4 nov. 2018

@author: Arvid
'''

import numpy as np
#import matplotlib as plt
from datetime import date
import time
import os
import random
import tkinter as tk
from color_scheme import get_color_scheme
#from unicodedata import bidirectional

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
UNDO = 5
SAVE = 6
SAVE_LAST = 7
QUIT = 8
STOP_PAUSE = 9

color_scheme = get_color_scheme()
    
def neighbours_equal(board):
    # Looking for vertical merges
    for col in range(4):
        for row in range(3):
            if board[row][col] != 0 and board[row][col] == board[row + 1][col]:
                return True 
    # Looking for horizontal merges
    for row in range(4):
        for col in range(3):
            if board[row][col] != 0 and board[row][col] == board[row][col + 1]:
                return True
    #Nothing is mergable
    return False 
    
def save_board(board, moves, undos, qs_pressed):
    file_name = os.path.normpath('C:/Users/Arvid/Documents/GitHub/2048/logs/' + str(date.today()) + '.txt')
    
    f = open(file_name, 'a')
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
    f.write('number of moves:' + str(moves) + '\n')
    f.write('number of undos:' + str(undos) + '\n')
    f.write('number of warnings:' + str(qs_pressed) + '\n')
        
    f.write('\nself.board = ' + str(board) + '\n')
    f.write('\n----------\n\n')

def print_game_over(board, nrof_moves_made, nrof_undos):
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
    print('moves:', nrof_moves_made)
    print('undos:', nrof_undos)

def empty_board():
    empty_board = [[0, 0, 0, 0] for _ in range(4)]
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
            
        return text_list
    
def get_input_from_char(char):
            if char is ord('w'): return UP
            elif char is ord('s'): return DOWN
            elif char is ord('d'): return RIGHT
            elif char is ord('a'): return LEFT
            elif char is ord('u'): return UNDO
            elif char is ord('i'): return SAVE
            elif char is ord('o'): return SAVE_LAST
            elif char is ord('p'): return QUIT
            elif char is ord('q'): return STOP_PAUSE
            else: return 
            
class game_of_2048:
    def __init__(self):
        self.initiate_board()
        self.warnings = False
        self.just_pressed_q = False
        self.nrof_qs_pressed = 0
        
        #self.board = [[0, 2, 4, 8], [16, 32, 64, 128],[ 256, 512, 1024, 2048],[ 4096, 2*4096, 4*4096, 8*4096]]
        #self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 4, 0, 2]]
        #self.board = [[0, 2, 0, 0], [2, 0, 4, 4], [64, 32, 16, 4], [4096, 512, 256, 32]]
        #self.board = [[0, 0, 0, 0], [8, 0, 0, 0], [4, 0, 0, 0], [4, 0, 0, 4]]
        #self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [4, 2, 0, 8], [4, 2, 4, 8]]
        #self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 4, 2, 2]]
        self.board = [[4, 2, 0, 0], [16, 4, 2, 0], [128, 64, 32, 16], [8192, 512, 256, 64]]
        
        self.board_history[0] = self.board
        
    def __copy__(self):
        # TODO: fix or remove
        return game_of_2048(self.board)
            
    def initiate_board(self):
        random.seed()
        
        self.board = empty_board()
        self.board_history = []
        
         
        self.insert_brick()
        
        self.nrof_moves_made = 0
        self.nrof_undos = 0
        self.board_history.append(self.board)
        
    def insert_brick(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        
        while (self.board[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
            
        insert_value = 2 if (random.random() > 0.1) else 4
        self.board[row][col] = insert_value
        
        if self.is_game_lost():
            print_game_over(self.board, self.nrof_moves_made, self.nrof_undos)
            
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
        if neighbours_equal(self.board): self.merge() 
        self.pack()
    
    def pack(self):
        for column in range(4):
            for _ in range(3):
                for row in range(3):
                    if (self.board[row][column] == 0) and (self.board[row + 1][column] != 0):
                        self.board[row][column] = self.board[row + 1][column]
                        self.board[row + 1][column] = 0
                        
                        self.changes_made = True
        return self.changes_made
                        
    def merge(self):
        for column in range(4):
            for row in range(3):
                if self.board[row][column] != 0:
                    if self.board[row][column] == self.board[row + 1][column]:
                        self.board[row][column] *= 2
                        self.board[row + 1][column] = 0
                        self.changes_made = True
        return self.changes_made
                        
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
    
    def put_numbers(self, text_list, warnings = False):
        for i in range(16):
            text_list[i].pack_forget()
            board_value = self.board[i//4][i%4]
            if self.warnings and not self.just_pressed_q:
                frame_color = 'red'
            else:
                frame_color = color_scheme[0] if board_value is 0 else color_scheme[int(np.log2(board_value))]
             
            text_list[i].delete('1.0', tk.END)
            text_list[i].insert(tk.END, '\n ')
            if board_value < 1000:
                text_list[i].insert(tk.END, ' ')
                if board_value < 10:
                    text_list[i].insert(tk.END, ' ')
                
                
            text_list[i].config(bg = frame_color)
            text_list[i].insert(tk.END, str(board_value))
            
            text_list[i].pack()
    
    def detect_warnings(self, attempted_move):
        # TODO: Fix unit test
        num_zeros = [0, 0, 0, 0]
        test_board = game_of_2048()
        
        # TODO: Fix real copy function for board
        for i in range(4): 
            for j in range(4): 
                test_board.board[i][j] = self.board[i][j]
        
        to_test = test_board.move(attempted_move)
        if to_test:
            for i in range(4): num_zeros[i] = test_board.board[i].count(0)
                
            warning_list = [[4, 4, 4, 1], [4, 4, 1, 0], [4, 1, 0, 0]]
            # TODO: Increase to involve full left and right layers as well.
            
            if num_zeros in warning_list:
                if not neighbours_equal(test_board.board):
                    return True
        # No move resulted in warnings:
        return False
        
def main():
    board = game_of_2048()
     
    def make_a_move(event):
        action_input = get_input_from_char(ord(event.char))
        
        if action_input is STOP_PAUSE: 
            board.just_pressed_q = True
            board.nrof_qs_pressed += 1
            repaint()
            
        elif action_input in [UP, DOWN, LEFT, RIGHT]:
            if not board.just_pressed_q:
                board.warnings = board.detect_warnings(action_input) or board.warnings
           
                
                    
            if (not board.warnings) or board.just_pressed_q:
                if board.move(action_input): #This returns true if an actual move has been made
                    
                    board.insert_brick()
                     
                    board.nrof_moves_made += 1
                     
                    if board.nrof_moves_made == len(board.board_history):
                        board.board_history.append([])
                     
                    board.board_history[board.nrof_moves_made] = board.board
                    repaint()
                    board.just_pressed_q = False
                    board.warnings = False
            else: 
                repaint()
                
        elif action_input is UNDO:
            board.nrof_moves_made -= 1
            board.nrof_undos += 1
            board.board = board.board_history[board.nrof_moves_made]
            
            repaint()
            
        elif action_input is SAVE:
            save_board(board.board, board.nrof_moves_made, board.nrof_undos, board.nrof_qs_pressed)
            print('saved at move', board.nrof_moves_made)
        elif action_input is QUIT:
            print_game_over(board.board, board.nrof_moves_made, board.nrof_undos)
            quit(0)
        else:
            print('error:', ord(event.char))
    
    def repaint():
        outer_frame.pack_forget()
        board.put_numbers(text_list)
        outer_frame.pack()
     
    root = tk.Tk()
    root.bind('<Key>', make_a_move)
    outer_frame = tk.Frame(root, width=400, height=400)
     
    text_list = initiate_frames(outer_frame)
     
    print('undo: u')
    print('save current: i')
    # print('save last: o')
    print('quit: p')
     
    repaint()
     
    root.mainloop()
 
    print('quit')

def detect_warnings_test():
    def test_subroutine(board, test_dir, warnings_expected):
        test = game_of_2048()
        
        test.board = board
        test.board_history[0] = test.board
        
        return (warnings_expected is (test.detect_warnings(test_dir) or test.board_history[0] != test.board))
    
    board_list = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 2, 0, 2], [4, 2, 0, 0]],
                  [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2], [4, 2, 0, 0]],
                  [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2], [4, 2, 0, 0]],
                  [[0, 0, 0, 0], [0, 0, 2, 0], [4, 2, 0, 8], [20, 40, 50, 60]],
                  [[0, 0, 0, 0], [8, 4, 16, 16], [64, 32, 64, 32], [32, 64, 32, 64]]]
    
    dir_list = [DOWN, DOWN, LEFT, DOWN, LEFT]
    bool_list = [False, True, False, False, True]
    
    for i, board, dir, bool in zip(range(len(board_list)), board_list, dir_list, bool_list):
        if not test_subroutine(board, dir, bool): 
            print('test', i, 'failed')
            quit(0)
    print('detect_warnings_test okay')

  
detect_warnings_test()
main()

