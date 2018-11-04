'''
Created on 4 nov. 2018

@author: Arvid
'''

import numpy as np
import matplotlib as plt
import random
import msvcrt
import time
from builtins import print



class game_of_2048:
    
    def __init__(self):
        self.initiate_board()
        #self.print_board()
    
    def initiate_board(self):
        random.seed()
        
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.insert_brick()
        
       
    
    def insert_brick(self):
        
        if 0 in self.board:
            print('0 is in list')
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
        
    
#     def pack_one_row(self, row):
#         for column in range(4):
#             repetitions = 0
#             while (repetitions < 4):
#                 if (self.board[4 * row + columns] == 0):
#                     for row_below_original row
#                     self.board[4 * row + columns] =
        
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
            
        
            
    def moveUp(self): 
        self.pack()
        self.merge() 
        self.pack()
        print('insert  brick:')
        self.insert_brick()
        
    
        
    
def main():
    board = game_of_2048()
    for move in range(100):
        print('Move', move)
        board.moveUp()
    #board.moveLeft
    print('quit')

main()
