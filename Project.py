import pygame
import random
import copy
from os import path

pygame.init()
size = width1, height1 = 500, 700
screen = pygame.display.set_mode(size)
img_dir = path.join(path.dirname(__file__), 'img')


class Sap:
    def __init__(self):
        pygame.display.set_caption("Супер сапер")
        self.width = 50
        self.height = 50
        self.count = 5
        self.board = [[1] * self.width for _ in range(self.height)]
        self.left = 10
        self.top = 10
        self.fps = 45


sap = Sap()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
