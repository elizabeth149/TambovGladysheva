import pygame
import random
import copy
import os

pygame.init()
size = width1, height1 = 900, 900
screen = pygame.display.set_mode(size)
background = pygame.image.load('back.jpg')
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
        self.board = [[1] * self.width for _ in range(self.height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.rast()

    def drawWindow(self):
        if pygame.mouse.get_focused():
            fullname = os.path.join('data', 'curs.png')
            image = pygame.image.load(fullname).convert()
            pygame.mouse.set_visible(False)
            MANUAL_CURSOR = pygame.image.load(
                fullname).convert_alpha()
            screen.blit(MANUAL_CURSOR, (pygame.mouse.get_pos()))

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

    def render(self):
        a = 0
        b = 0
        for y in range(self.width):
            for x in range(self.height):
                if self.board[x][y] == 1:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (x * self.cell_size +
                                      self.left,
                                      y *
                                      self.cell_size +
                                      self.top,
                                      self.cell_size,
                                      self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, (255, 0, 0),
                                     (x * self.cell_size +
                                      self.left,
                                      y *
                                      self.cell_size +
                                      self.top,
                                      self.cell_size,
                                      self.cell_size), 0)
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (x * self.cell_size +
                                      self.left,
                                      y *
                                      self.cell_size +
                                      self.top,
                                      self.cell_size,
                                      self.cell_size), 1)

    def open_cell(self, mouse_pos):
        a, b = mouse_pos
        min = 0
        x1 = (a - self.left) // self.cell_size
        y1 = (b - self.top) // self.cell_size
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
            font = pygame.font.Font(None, 25)
            text = font.render(str(min), True, (0, 255, 0))
            screen.blit(text, [x1 * self.cell_size + self.left,
                               y1 * self.cell_size + self.top])
        elif x1 == 0 and y1 == 0 and self.board[x1][y1] != 10:
            if self.board[x1 + 1][y1] == 10:
                min += 1
            if self.board[x1 + 1][y1 + 1] == 10:
                min += 1
            if self.board[x1][y1 + 1] == 10:
                min += 1
            font = pygame.font.Font(None, 25)
            text = font.render(str(min), True, (0, 255, 0))
            screen.blit(text, [x1 * self.cell_size + self.left,
                               y1 * self.cell_size + self.top])
        elif x1 == 0 and 0 < y1 < self.width - 1 and self.board[x1][y1] != 10:
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
            font = pygame.font.Font(None, 25)
            text = font.render(str(min), True, (0, 255, 0))
            screen.blit(text, [x1 * self.cell_size + self.left,
                               y1 * self.cell_size + self.top])
        elif x1 == 0 and y1 == self.width - 1 and self.board[x1][y1] != 10:
            if self.board[x1][y1 - 1] == 10:
                min += 1
            if self.board[x1 + 1][y1 - 1] == 10:
                min += 1
            if self.board[x1 + 1][y1] == 10:
                min += 1
            font = pygame.font.Font(None, 25)
            text = font.render(str(min), True, (0, 255, 0))
            screen.blit(text, [x1 * self.cell_size + self.left,
                               y1 * self.cell_size + self.top])
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
            font = pygame.font.Font(None, 25)
            text = font.render(str(min), True, (0, 255, 0))
            screen.blit(text, [x1 * self.cell_size + self.left,
                               y1 * self.cell_size + self.top])
        elif x1 == self.height - 1 and y1 == self.width - 1 and self.board[x1][
            y1] != 10:
            if self.board[x1 - 1][y1] == 10:
                min += 1
            if self.board[x1 - 1][y1 - 1] == 10:
                min += 1
            if self.board[x1][y1 - 1] == 10:
                min += 1
            font = pygame.font.Font(None, 25)
            text = font.render(str(min), True, (0, 255, 0))
            screen.blit(text, [x1 * self.cell_size + self.left,
                               y1 * self.cell_size + self.top])
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
            font = pygame.font.Font(None, 25)
            text = font.render(str(min), True, (0, 255, 0))
            screen.blit(text, [x1 * self.cell_size + self.left,
                               y1 * self.cell_size + self.top])
        elif x1 == self.height - 1 and y1 == 0 and self.board[x1][y1] != 10:
            if self.board[x1 - 1][y1] == 10:
                min += 1
            if self.board[x1 - 1][y1 + 1] == 10:
                min += 1
            if self.board[x1][y1 + 1] == 10:
                min += 1
            font = pygame.font.Font(None, 25)
            text = font.render(str(min), True, (0, 255, 0))
            screen.blit(text, [x1 * self.cell_size + self.left,
                               y1 * self.cell_size + self.top])
        elif 0 < x1 < self.height - 1 and y1 == 0 and self.board[x1][y1] != 10:
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
            font = pygame.font.Font(None, 25)
            text = font.render(str(min), True, (0, 255, 0))
            screen.blit(text, [x1 * self.cell_size + self.left,
                               y1 * self.cell_size + self.top])



minesweeper = Minesweeper(15, 15, 10)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            minesweeper.open_cell(event.pos)
        if event.type != pygame.MOUSEBUTTONDOWN and fl:
            screen.blit(background, (0, 0))
        minesweeper.render()
        sap.drawWindow()

    pygame.display.flip()
pygame.quit()  # точное закрытие окна
