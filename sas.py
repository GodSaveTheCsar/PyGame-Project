import pygame
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QMainWindow
import os

pygame.init()
SIZE = 0
FPS = 50


def start_screen():
    pygame.init()
    clock = pygame.time.Clock()
    ex = MyWidget()
    ex.show()
    while True:
        if ex.a:
            return ex.size
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)


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


player_image = load_image('player_stand.png')
tile_width = tile_height = 28


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)  # Загружаем дизайн
        self.a = False
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.run)

    def run(self):
        self.size = int(self.sender().text().split('(')[1][0:2]) * 40
        self.a = True
        self.close()


class Board():
    def __init__(self):
        self.board = [[None for _ in range(SIZE // 40)] for _ in range(SIZE // 40)]
        print(len(self.board), len(self.board[0]))
        self.top = SIZE / 2
        self.left = 0

    def get_cell(self, mouse_pos):
        pass

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def render(self):
        top = self.top
        left = self.left
        for i in range(int(SIZE / 40) + 1):
            pygame.draw.line(screen, (255, 255, 255), (left, top), (left + SIZE / 2, top - SIZE / 2), 1)
            top += 20
            left += 20
        top = self.top
        left = self.left
        for i in range(int(SIZE / 40) + 1):
            pygame.draw.line(screen, (255, 255, 255), (left, top), (left + SIZE / 2, top + SIZE / 2), 1)
            top -= 20
            left += 20
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == 'selected_blue':
                    pygame.draw.polygon(screen, 'blue', (x * 28, y * 28 - 14),
                                        ((x + 1) * 28 - 14, (y-1) * 28), ((x + 1) * 28, y * 28 - 14),(x * 28 - 14, y * 28))


class Human(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, board):
        super().__init__(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.board = board
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.is_clicked = False
        self.board[pos_x][pos_y] = 'player'

    def clicked(self):
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.x + 2):
                self.board[x][y] = 'selected_blue'


if __name__ == '__main__':
    pygame.init()
    SIZE = start_screen()
    screen = pygame.display.set_mode((SIZE, SIZE))
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    board = Board()
    clock = pygame.time.Clock()
    running = True
    player = None
    screen.fill((0, 0, 0))
    human = Human(10, 10, board)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()
