import pygame
import random
import copy
import os
import sys

pygame.init()
size = width1, height1 = 900, 900
screen = pygame.display.set_mode(size)
background = pygame.image.load('back.jpg')
end = pygame.image.load('data/end.jpg')
field = pygame.image.load('поле.png')
pygame.display.set_caption("Сапер")
FPS = 200
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
cor = []
bomb = False


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["                САПЕР", "",
                  "", "",
                  "1. Число в ячейке показывает, сколько мин",
                  "скрыто вокруг данной ячейки."
                  "Это число поможет понять вам,",
                  "где находятся безопасные ячейки, а где находятся бомбы. ",
                  "2. Если рядом с открытой ячейкой есть ",
                  "пустая ячейка, то она откроется автоматически. ",
                  "3. Если вы открыли ячейку с миной, то ",
                  "игра проиграна. ",
                  "4. Что бы пометить ячейку, в которой ",
                  "находится бомба, нажмите её правой кнопкой мыши.",
                  "5. Игра продолжается до тех пор, пока ",
                  "вы не откроете все не заминированные ячейки."
                  ]

    fon = pygame.transform.scale(load_image('fon.jpg'), (900, 900))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return False
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, xy, flag=False):
        super().__init__(all_sprites)
        x, y = xy
        self.cut_sheet(sheet, columns, rows, x, y, flag)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows, x, y, flag):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        self.frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

        screen.blit(background, (0, 0))
        screen.blit(field, (230, 300))
        minesweeper.render()
        draw()
        if flag:
            for i in self.frames:
                image = i.convert_alpha()
                screen.blit(image, (x - 50, y - 50))
                pygame.display.flip()
                clock.tick(100)
                screen.blit(background, (0, 0))
                screen.blit(field, (230, 300))
                minesweeper.render()
                draw()
            global fl
            fl = False


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

    def drawWindow(self):
        if pygame.mouse.get_focused():
            fullname = os.path.join('data', 'curs.png')
            image = pygame.image.load(fullname).convert()
            pygame.mouse.set_visible(False)
            MANUAL_CURSOR = pygame.image.load(
                fullname).convert_alpha()
            screen.blit(MANUAL_CURSOR, (pygame.mouse.get_pos()))


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
                pygame.draw.rect(screen, (210, 180, 140),
                                 (x * self.cell_size +
                                  self.left,
                                  y *
                                  self.cell_size +
                                  self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    def open_cell(self, mouse_pos, button):
        global cor
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
                cor.append([str(min), x1, y1])
            elif x1 == 0 and y1 == 0 and self.board[x1][y1] != 10:
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 + 1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                cor.append([str(min), x1, y1])
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
                cor.append([str(min), x1, y1])
            elif x1 == 0 and y1 == self.width - 1 and self.board[x1][y1] != 10:
                if self.board[x1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                cor.append([str(min), x1, y1])
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
                cor.append([str(min), x1, y1])
            elif x1 == self.height - 1 and y1 == self.width - 1 and \
                    self.board[x1][
                        y1] != 10:

                if self.board[x1 - 1][y1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1][y1 - 1] == 10:
                    min += 1
                cor.append([str(min), x1, y1])
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
                cor.append([str(min), x1, y1])

            elif x1 == self.height - 1 and y1 == 0 and self.board[x1][
                y1] != 10:
                if self.board[x1 - 1][y1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 + 1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                cor.append([str(min), x1, y1])

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
                cor.append([str(min), x1, y1])
            elif self.board[x1][y1] == 10:
                cor.append([10, x1, y1])
        else:
            cor.append([55555, x1, y1])


def draw():
    for i in cor:
        min = i[0]
        x1 = i[1]
        y1 = i[2]
        if min != 55555 and min != 10:
            font = pygame.font.Font(None, 25)
            text = font.render(min, True, (255, 235, 205))
            screen.blit(text, [int(x1) * 30 + 230,
                               int(y1) * 30 + 300])
        elif min == 55555:
            fullname = os.path.join('data', 'flag.png')
            MANUAL_CURSOR = pygame.image.load(
                fullname).convert_alpha()
            screen.blit(MANUAL_CURSOR, (x1 * 30 + 230,
                                        y1 * 30 + 300))
        else:
            global bomb
            bomb = True


minesweeper = Minesweeper(15, 15, 20)
sap = Sap()
running = True
fl = True
start_screen()
while running:
    for event in pygame.event.get():
        if fl:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                minesweeper.open_cell(event.pos, event.button)
                dragon = AnimatedSprite(load_image("bomb.png"), 9,
                                        9,
                                        event.pos, bomb)
            screen.blit(background, (0, 0))
            screen.blit(field, (230, 300))
            minesweeper.render()
            draw()
            sap.drawWindow()
            pygame.time.delay(20)
            pygame.display.flip()
        else:
            screen.blit(end, (0, 0))
            pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
pygame.quit()  # точное закрытие окна
