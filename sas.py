import pygame
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
from random import randrange

pygame.init()
SIZE = 1000
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites):
        super().__init__(sprites)
        self.x = x
        self.y = y


class Pole(Tile):
    def __init__(self, x, y, sprites):
        super().__init__(x, y, sprites)
        self.image = pygame.transform.scale(load_image('pole.png'), (28, 28))
        self.cell_size = 20
        self.image = pygame.transform.rotate(self.image, 45)
        self.rect = self.image.get_rect().move(400, 400)


class Castle(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        pass


class Player:
    def __init__(self):
        self.resources = {
            'wood': 0,
            'iron': 0
        }

    def update_resources(self, name, val):
        self.resourses[name] += val


class Resource(Tile):
    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.name = name
        self.is_mining = False

        if name == 'wood':
            self.image = load_image('wood.png')
            self.image = pygame.transform.scale(self.image, (28, 28))

    def mine(self):
        if not self.is_mining:
            self.is_mining = True
            print('добывается')



class MyWidget(QMainWindow):
    def __init__(self):
        global SIZE
        super().__init__()
        uic.loadUi('untitled.ui', self)  # Загружаем дизайн
        self.is_pushed = False
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.run)

    def run(self):
        self.size = int(self.sender().text().split('(')[1][0:2]) * 30
        self.board_size = int(self.sender().text().split('(')[1][0:2])
        self.is_pushed = True
        self.close()


def start_screen():
    pygame.init()
    clock = pygame.time.Clock()
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    while True:
        if ex.is_pushed:
            return ex.size, ex.board_size
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)


class Board():
    def __init__(self):
        self.list = [[None for _ in range(SIZE // 30)] for _ in range(SIZE // 30)]
        self.width = self.height = BOARD_SIZE
        self.side_size = int(SIZE // 30)
        self.cell_size = 30
        self.top = (SIZE - self.width * self.cell_size) / 2
        self.left = (SIZE - self.width * self.cell_size) / 2

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if mouse_pos[0] > self.top + j * self.cell_size and mouse_pos[1] > self.top + i * self.cell_size and \
                        mouse_pos[0] < self.cell_size + self.top + j * self.cell_size and \
                        mouse_pos[1] < self.cell_size + self.top + i * self.cell_size:
                    return (i, j)


    def on_click(self, cell_coords):
        print(cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def render(self):
        fon = pygame.transform.scale(load_image('fon.jpg'), (SIZE, SIZE))
        screen = pygame.display.set_mode((SIZE, SIZE))
        screen.blit(fon, (0, 0))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255), (self.top + j * self.cell_size,
                                                           self.top + i * self.cell_size,
                                                           self.cell_size, self.cell_size), 1)


class Human(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, board):
        super().__init__(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.board = board
        self.cell_size = 30
        self.image = load_image('player_stand.png')
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect().move(self.y * self.cell_size, self.x * self.cell_size)
        self.is_clicked = False
        self.board.list[pos_x][pos_y] = 'player'

    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect = self.image.get_rect().move(self.y * self.cell_size, self.x * self.cell_size)

    def can_move(self, coords):
        x = coords[0]
        y = coords[1]
        if x == self.x:
            if y == self.y:
                return False
            if y + 1 == self.y or y - 1 == self.y:
                return True
        if y == self.y:
            if x == self.x:
                return False
            if x + 1 == self.x or x - 1 == self.x:
                return True
        if x + 1 == self.x:
            if y == self.y:
                return False
            if y + 1 == self.y or y - 1 == self.y:
                return True
        if y + 1 == self.y:
            if x == self.x:
                return False
            if x + 1 == self.x or x - 1 == self.x:
                return True
        if x - 1 == self.x:
            if y == self.y:
                return False
            if y + 1 == self.y or y - 1 == self.y:
                return True
        if y - 1 == self.y:
            if x == self.x:
                return False
            if x + 1 == self.x or x - 1 == self.x:
                return True
    def clicked(self):
        if self.is_clicked:
            self.is_clicked = False
        else:
            self.is_clicked = True
        '''for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.x + 2):
                self.board.list[x][y] = 'selected_blue'
                '''


if __name__ == '__main__':
    pygame.init()
    SIZE, BOARD_SIZE = start_screen()
    screen = pygame.display.set_mode((SIZE, SIZE))
    board = Board()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True
    human = Human(randrange(SIZE // 30 // 2 - 2, SIZE // 30 // 2 + 2),
                  randrange(SIZE // 30 // 2 - 2, SIZE // 30 // 2 + 2), board)
    screen.fill((0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    human.clicked()
                if human.is_clicked and event.button == 3:
                    if human.can_move(board.get_cell(event.pos)):
                        x, y = board.get_cell(event.pos)
                        human.move(x, y)
                else:
                    board.get_click(event.pos)
        board.render()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()