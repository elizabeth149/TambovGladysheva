import pygame
import random
import copy
import os

pygame.init()
size = width1, height1 = 1024, 600
screen = pygame.display.set_mode(size)
background = pygame.image.load('back1.png')
field = pygame.image.load('поле.png')
field1 = pygame.image.load('поле.png')
pygame.display.set_caption("Морской бой")


class Sap:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.count = 5
        self.board = [[1] * self.width for _ in range(self.height)]
        self.left = 10
        self.top = 10
        self.fps = 45

    def drawWindow(self):
        if pygame.mouse.get_focused():
            fullname = os.path.join('data', 'curs.png')
            image = pygame.image.load(fullname).convert()
            pygame.mouse.set_visible(False)
            MANUAL_CURSOR = pygame.image.load(
                fullname).convert_alpha()
            screen.blit(MANUAL_CURSOR, (pygame.mouse.get_pos()))


sap = Sap()
running = True
fl = True
while running:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type != pygame.QUIT and fl:
            screen.blit(background, (0, 0))
            screen.blit(field, (50, 170))
            screen.blit(field1, (550, 170))
        else:
            fl = False
        sap.drawWindow()
    pygame.display.flip()
pygame.quit()  # точное закрытие окна
