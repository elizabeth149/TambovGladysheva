import pygame
import random
import copy

pygame.init()
size = width1, height1 = 500, 700
screen = pygame.display.set_mode(size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()