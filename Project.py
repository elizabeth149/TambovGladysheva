import pygame
import random
import copy
import os

pygame.init()
size = width1, height1 = 900, 900
screen = pygame.display.set_mode(size)
background = pygame.image.load('back.jpg')
field = pygame.image.load('поле.png')
pygame.display.set_caption("Сапер")


class Sap:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.count = 5
        self.board = [[1] * self.width for _ in range(self.height)]
        self.left = 10
        self.top = 10
        self.fps = 45
        self.board = [[1] * self.width for _ in range(self.height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.rast()

    def rast(self):
        for i in range(self.count):
            a = random.randint(0, self.height - 1)
            b = random.randint(0, self.width - 1)
            self.board[a][b] = 10


class Minesweeper(Sap):
    def __init__(self, width, height, count):
        self.width = width
        self.height = height
        self.count = count
        self.board = [[1] * width for _ in range(height)]
        self.left = 230
        self.top = 300
        self.cell_size = 30
        self.rast()
        self.cor = []

    def render(self):
        a = 0
        b = 0
        for y in range(self.width):
            for x in range(self.height):
                pygame.draw.rect(screen, (210, 180, 140),
                                 (x * self.cell_size +
                                  self.left,
                                  y *
                                  self.cell_size +
                                  self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    def open_cell(self, mouse_pos, button):
        a, b = mouse_pos
        min = 0
        x1 = (a - self.left) // self.cell_size
        y1 = (b - self.top) // self.cell_size
        if button == 1:
            if 0 < x1 < self.height - 1 and 0 < y1 < self.width - 1 and \
                    self.board[x1][y1] != 10:
                if self.board[x1 - 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 - 1][y1] == 10:
                    min += 1
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 + 1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 + 1] == 10:
                    min += 1
                self.cor.append([str(min), x1, y1])
            elif x1 == 0 and y1 == 0 and self.board[x1][y1] != 10:
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 + 1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                self.cor.append([str(min), x1, y1])
            elif x1 == 0 and 0 < y1 < self.width - 1 and self.board[x1][
                y1] != 10:

                if self.board[x1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 + 1] == 10:
                    min += 1
                self.cor.append([str(min), x1, y1])
            elif x1 == 0 and y1 == self.width - 1 and self.board[x1][y1] != 10:
                if self.board[x1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                self.cor.append([str(min), x1, y1])
            elif 0 < x1 < self.height - 1 and y1 == self.width - 1 and \
                    self.board[x1][y1] != 10:

                if self.board[x1 - 1][y1] == 10:
                    min += 1
                if self.board[x1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 - 1] == 10:
                    min += 1
                self.cor.append([str(min), x1, y1])
            elif x1 == self.height - 1 and y1 == self.width - 1 and \
                    self.board[x1][
                        y1] != 10:

                if self.board[x1 - 1][y1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1][y1 - 1] == 10:
                    min += 1
                self.cor.append([str(min), x1, y1])
            elif x1 == self.height - 1 and 0 < y1 < self.width - 1 and \
                    self.board[x1][y1] != 10:

                if self.board[x1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 - 1][y1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 + 1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                self.cor.append([str(min), x1, y1])

            elif x1 == self.height - 1 and y1 == 0 and self.board[x1][
                y1] != 10:
                if self.board[x1 - 1][y1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 + 1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                self.cor.append([str(min), x1, y1])

            elif 0 < x1 < self.height - 1 and y1 == 0 and self.board[x1][
                y1] != 10:

                if self.board[x1 - 1][y1] == 10:
                    min += 1
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 + 1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 + 1] == 10:
                    min += 1
                self.cor.append([str(min), x1, y1])

    def draw(self):
        for i in self.cor:
            min = i[0]
            x1 = i[1]
            y1 = i[2]
            font = pygame.font.Font(None, 25)
            text = font.render(min, True, (0, 255, 0))
            screen.blit(text, [int(x1) * self.cell_size + self.left,
                           int(y1) * self.cell_size + self.top])


minesweeper = Minesweeper(15, 15, 20)
sap = Sap()
running = True
fl = True
while running:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            fl = False
            minesweeper.open_cell(event.pos, event.button)
        if event.type != pygame.MOUSEBUTTONDOWN:
            screen.blit(background, (0, 0))
            screen.blit(field, (230, 300))
            minesweeper.render()
            minesweeper.draw()
    pygame.display.flip()
pygame.quit()  # точное закрытие окна
