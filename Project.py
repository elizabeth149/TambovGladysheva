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
win = pygame.image.load('data/win.png')
field = pygame.image.load('поле.png')
pygame.display.set_caption("Сапер")
FPS = 200
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
cor = []
count_flags = 30
time = pygame.image.load('data/time.png')
pygame.mixer.music.load('fon.mp3')
pygame.mixer.music.play()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["                 САПЕР", "", "                Правила:", '',
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
                  "вы не откроете все не заминированные ячейки.",
                  "6. Если вы хотите проверить правильность ",
                  "указанных бомб флажками, нажмите ",
                  "на 'колесико' мышки."
                  "             Для продолжения ",
                  "                                       нажать любую из клавиш",
                  "",
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
    def __init__(self, sheet, columns, rows, xy):
        super().__init__(all_sprites)
        x, y = xy
        self.cut_sheet(sheet, columns, rows, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows, x, y):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        self.frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        for i in self.frames:
            image = i.convert_alpha()
            screen.blit(image, (x - 50, y - 50))
            pygame.display.flip()
            clock.tick(100)
            screen.blit(background, (0, 0))
            screen.blit(field, (230, 300))
            minesweeper.render()
            screen.blit(time, (6, 350))
            draw()
        global fl
        fl = False
        screen.blit(background, (0, 0))
        screen.blit(field, (230, 300))
        screen.blit(time, (6, 350))
        minesweeper.render()
        draw()


class Sap:
    def __init__(self):
        self.fps = 45
        self.cell_size = 30

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
        self.board = []
        self.left = 230
        self.top = 300
        self.cell_size = 30
        self.rast()

    def rast(self):
        self.board = [[1] * 15 for _ in range(15)]
        for bomba in range(30):
            a = random.randint(0, 14)
            b = random.randint(0, 14)
            if self.board[a][b] != 10:
                self.board[a][b] = 10
            else:
                while self.board[a][b] == 10:
                    a = random.randint(0, 14)
                    b = random.randint(0, 14)
                else:
                    self.board[a][b] = 10

    def render(self):
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
        global count_flags
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
                if [55555, x1, y1] not in cor:
                    cor.append([str(min), x1, y1])
            elif x1 == 0 and y1 == 0 and self.board[x1][y1] != 10:
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 + 1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                if [55555, x1, y1] not in cor:
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
                if [55555, x1, y1] not in cor:
                    cor.append([str(min), x1, y1])
            elif x1 == 0 and y1 == self.width - 1 and self.board[x1][y1] != 10:
                if self.board[x1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1 - 1] == 10:
                    min += 1
                if self.board[x1 + 1][y1] == 10:
                    min += 1
                if [55555, x1, y1] not in cor:
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
                if [55555, x1, y1] not in cor:
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
                if [55555, x1, y1] not in cor:
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
                if [55555, x1, y1] not in cor:
                    cor.append([str(min), x1, y1])

            elif x1 == self.height - 1 and y1 == 0 and self.board[x1][
                y1] != 10:
                if self.board[x1 - 1][y1] == 10:
                    min += 1
                if self.board[x1 - 1][y1 + 1] == 10:
                    min += 1
                if self.board[x1][y1 + 1] == 10:
                    min += 1
                if [55555, x1, y1] not in cor:
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
                if [55555, x1, y1] not in cor:
                    cor.append([str(min), x1, y1])
            elif 0 <= x1 <= self.height - 1 and 0 <= y1 <= self.width - 1:
                if self.board[x1][y1] == 10:
                    cor.append([10, x1, y1])
        elif button == 3 and 0 <= x1 < self.height and 0 <= y1 < self.width:
            global count_flags
            if [55555, x1, y1] in cor:
                d = cor.index([55555, x1, y1])
                del cor[d]
                count_flags += 1
            else:
                if count_flags != 0:
                    cor.append([55555, x1, y1])
                    count_flags -= 1
        elif button == 2:
            win_flag = True
            if count_flags == 0:
                for i in cor:
                    if i[0] == 55555:
                        if self.board[i[1]][i[2]] != 10:
                            win_flag = False
                if win_flag:
                    global winner
                    global fl
                    fl = False
                    winner = True


def draw():
    global count_flags
    font = pygame.font.Font(None, 100)
    text = font.render(str(count_flags), True, (255, 235, 205))
    screen.blit(text, [60, 415])
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


minesweeper = Minesweeper(15, 15, 30)
sap = Sap()
running = True
fl = True
start_screen()
screen.blit(load_image("time.png"), (150, 290))
winner = False
run = 0
while running:
    for event in pygame.event.get():
        if fl:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                minesweeper.open_cell(event.pos, event.button)
                for i in cor:
                    min = i[0]
                    x1 = i[1]
                    y1 = i[2]
                    if min == 10:
                        pygame.mixer.music.pause()
                        pygame.mixer.music.load('boom.mp3')
                        pygame.mixer.music.play()
                        dragon = AnimatedSprite(load_image("bomb.png"), 9, 9,
                                                event.pos)
            screen.blit(background, (0, 0))
            screen.blit(field, (230, 300))
            minesweeper.render()
            screen.blit(time, (6, 350))
            draw()
            sap.drawWindow()
            pygame.time.delay(1)
            pygame.display.flip()
            pygame.mixer.music.unpause()
            pygame.mixer.music.set_volume(0.5)


        else:
            if not winner:
                if run == 0:
                    pygame.mixer.music.load('end.mp3')
                    pygame.mixer.music.play()
                    run += 1
                screen.blit(end, (0, 0))
                pygame.display.flip()
            else:
                if run == 0:
                    pygame.mixer.music.load('win.mp3')
                    pygame.mixer.music.play()
                    run += 1
                screen.blit(win, (0, 0))
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
pygame.quit()  # точное закрытие окна
