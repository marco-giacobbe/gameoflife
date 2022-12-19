import pygame
from matrix import Matrix
import time
import threading

from config import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((HEIGHT, WIDTH))
        self.matrix = Matrix(HEIGHT//AUTOMATON_SIZE, WIDTH//AUTOMATON_SIZE)
        self.handler_event = threading.Thread(target=self.handle_event)
        self.handler_event.start()
        self.lclicking = False
        self.rclicking = False
        self.game = False

    def run(self):
        while True:
            # check if handler_event Thread is dead
            if not self.handler_event.is_alive():
                raise SystemExit
            self.draw()
            if self.lclicking:
                # draw automaton on the matrix
                self.matrix.draw()
            elif self.rclicking:
                # erease automaton on the matrix
                self.matrix.erease()
            if self.game:
                # Automaton can evolve
                time.sleep(TIME_SLEEP)
                self.matrix.update()

    def handle_event(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if self.game:
                        if event.key == pygame.K_r:
                            self.matrix.randomize()
                        elif event.key == pygame.K_SPACE:
                            self.matrix.z_fill()
                            self.game = False
                    else:
                        if event.key == pygame.K_r:
                            self.matrix.randomize()
                            self.game = True
                        elif event.key == pygame.K_SPACE:
                            self.game = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.lclicking = True
                    elif event.button == 3:
                        self.rclicking = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.lclicking = False
                    elif event.button == 3:
                        self.rclicking = False

    def draw(self):
        # draw automatons and update display
        self.draw_automaton()
        self.draw_grid()
        pygame.display.update()

    def draw_automaton(self):
        y_coordinate = 0
        x_coordinate = 0
        for row in self.matrix.matrix:
            for automaton in row:
                if automaton[0]:
                    pygame.draw.rect(self.screen, DEAD_COLOR,
                                     (x_coordinate, y_coordinate, AUTOMATON_SIZE, AUTOMATON_SIZE))
                else:
                    pygame.draw.rect(self.screen, ALIVE_COLOR,
                                     (x_coordinate, y_coordinate, AUTOMATON_SIZE, AUTOMATON_SIZE))
                x_coordinate += AUTOMATON_SIZE
            y_coordinate += AUTOMATON_SIZE
            x_coordinate = 0

    def draw_grid(self):
        for line in range(0, HEIGHT, AUTOMATON_SIZE):
            pygame.draw.rect(self.screen, GRID_COLOR,
                (line, 0, 1, HEIGHT))
        for line in range(0, WIDTH, AUTOMATON_SIZE):
            pygame.draw.rect(self.screen, GRID_COLOR,
                (0, line, HEIGHT, 1))
