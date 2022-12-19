import random
import pygame

from config import *


class Matrix:
    def __init__(self, cols, rows):  # columns and rows
        """
            matrix is composed by a list of lists of automatons
            each automaton is represented by a list with state and number of neighbours
            each rows is represented by a list of automaton
        """
        self.matrix = list()
        self.cols = cols
        self.rows = rows
        self.z_fill()

    def z_fill(self):
        # fill matrix with dead automatons
        self.matrix = list()
        for row in range(self.rows):
            new_line = list()
            for col in range(self.cols):
                new_line.append([False, None])
            self.matrix.append(new_line)

    def randomize(self):
        # fill matrix with random automatons
        self.matrix = list()
        for row in range(self.rows):
            new_line = list()
            for col in range(self.cols):
                if random.randint(0, 1):
                    new_line.append([True, None])
                else:
                    new_line.append([False, None])
            self.matrix.append(new_line)

    def calculate_neighbours(self):
        # calculate neighbours number of each automaton
        for row in range(self.rows):
            if row == 0:
                y_start = 0
                y_end = row+2
            elif row == self.rows-1:
                y_start = row-1
                y_end = self.rows-1
            else:
                y_start = row-1
                y_end = row+2
            for col in range(self.cols):
                if col == 0:
                    x_start = 0
                    x_end = col+2
                elif col == self.cols-1:
                    x_start = col-1
                    x_end = self.cols-1
                else:
                    x_start = col-1
                    x_end = col+2
                counter = 0
                for i in range(y_start, y_end):
                    for j in range(x_start, x_end):
                        if not (j == col and i == row):
                            if self.matrix[i][j][0]:
                                counter += 1
                self.matrix[row][col][1] = counter

    def update(self):
        # update automaton's state starting neighbour's number
        self.calculate_neighbours()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j][0] and (self.matrix[i][j][1] < 2 or self.matrix[i][j][1] > 3):
                    self.matrix[i][j][0] = False
                elif not self.matrix[i][j][0] and (self.matrix[i][j][1] == 3):
                    self.matrix[i][j][0] = True

    def draw(self):
        # draw automatons starting from user input
        x, y = pygame.mouse.get_pos()
        self.matrix[y//AUTOMATON_SIZE][x//AUTOMATON_SIZE][0] = True

    def erease(self):
        #erease automatons
        x, y = pygame.mouse.get_pos()
        self.matrix[y//AUTOMATON_SIZE][x//AUTOMATON_SIZE][0] = False
