import pygame
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
from random import randrange

pygame.init()
SIZE = 1000
FPS = 50
CELL_SIZE = 30


def fon_paint():
    fon = pygame.transform.scale(load_image('fon.jpg'), (SIZE, SIZE))
    screen = pygame.display.set_mode((SIZE, SIZE))
    screen.blit(fon, (0, 0))


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
        self.image = pygame.transform.scale(load_image('pole.png'), (30, 30))
        self.rect = self.image.get_rect().move(y * CELL_SIZE + TOPLEFT, x * CELL_SIZE + TOPLEFT)


class Castle(Tile):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(load_image('castle.jpg'), (30, 30))
        self.rect = self.image.get_rect().move(y * CELL_SIZE + TOPLEFT, x * CELL_SIZE + TOPLEFT)


class Player:
    def __init__(self):
        self.resources = {
            'wood': 0,
            'iron': 0,
            'jewelry': 0,
            'food': 0
        }

    def update_resources(self, name, val):
        self.resourses[name] += val


class Resource(Tile):
    def __init__(self, x, y, name, sprites):
        super().__init__(x, y, sprites)
        self.x = x
        self.y = y
        self.name = name
        self.is_mining = False
        if name == 'tree':
            self.image = pygame.transform.scale(load_image('tree.png'), (30, 30))
            self.rect = self.image.get_rect().move(y * CELL_SIZE + TOPLEFT, x * CELL_SIZE + TOPLEFT)
        if name == 'iron':
            self.image = pygame.transform.scale(load_image('iron.png'), (30, 30))
            self.rect = self.image.get_rect().move(y * CELL_SIZE + TOPLEFT, x * CELL_SIZE + TOPLEFT)
        if name == 'water':
            self.image = pygame.transform.scale(load_image('water.jpg'), (30, 30))
            self.rect = self.image.get_rect().move(y * CELL_SIZE + TOPLEFT, x * CELL_SIZE + TOPLEFT)
        if name == 'food':
            self.image = pygame.transform.scale(load_image('food.png'), (30, 30))
            self.rect = self.image.get_rect().move(y * CELL_SIZE + TOPLEFT, x * CELL_SIZE + TOPLEFT)

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
        size = int(self.sender().text().split('(')[1][0:2])
        self.size = size * 30
        if size == 25:
            self.size += 180
        if size == 20:
            self.size += 120
        if size == 15:
            self.size += 60
        self.board_size = int(self.sender().text().split('(')[1][0:2])
        self.topleft = int((self.size - size * CELL_SIZE) / 2)
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
            return ex.size, ex.board_size, ex.topleft
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)


def resources_screen(resources):
    pygame.init()
    resources_sprites = pygame.sprite.Group()
    food = pygame.transform.scale(load_image('food_icon.png'), (50, 50))
    image = load_image('frame_1.png')
    iron = pygame.transform.scale(load_image('iron_icon.png'), (50, 50))
    wood = pygame.transform.scale(load_image('wood_icon.png'), (50, 50))
    brilliant = pygame.transform.scale(load_image('brilliant_icon.png'), (40, 50))
    frame = pygame.sprite.Sprite(resources_sprites)
    wood_i = pygame.sprite.Sprite(resources_sprites)
    iron_i = pygame.sprite.Sprite(resources_sprites)
    food_i = pygame.sprite.Sprite(resources_sprites)
    brilliant_i = pygame.sprite.Sprite(resources_sprites)
    frame.image = image
    frame.rect = frame.image.get_rect()
    frame.rect.x = 0
    frame.rect.y = 0
    iron_i.image = iron
    iron_i.rect = iron_i.image.get_rect()
    iron_i.rect.x = 0
    iron_i.rect.y = 0
    food_i.image = food
    food_i.rect = food_i.image.get_rect()
    food_i.rect.x = SIZE // 4
    food_i.rect.y = 0
    wood_i.image = wood
    wood_i.rect = wood_i.image.get_rect()
    wood_i.rect.x = 2 * SIZE // 4
    wood_i.rect.y = 0
    brilliant_i.image = brilliant
    brilliant_i.rect = brilliant_i.image.get_rect()
    brilliant_i.rect.x = 3 * SIZE // 4
    brilliant_i.rect.y = 0
    font = pygame.font.Font(None, 30)
    resources_sprites.draw(screen)
    count = -1
    for i in resources:
        count += 1
        string_rendered = font.render(str(resources[i]), 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord = count * SIZE // 4 + 50
        intro_rect.left = text_coord
        intro_rect.y = 15
        screen.blit(string_rendered, intro_rect)

def builder_screen(builder):
    global builder_sprites
    if builder.is_clicked:
        hammer = pygame.transform.scale(load_image('hammer.png'), (50, 50))
        image = pygame.transform.scale(load_image('frame.png'), (300, 100))
        frame = pygame.sprite.Sprite(builder_sprites)
        build = pygame.sprite.Sprite(builder_sprites)
        build.image = hammer
        build.rect = build.image.get_rect()
        build.rect.x = SIZE // 2 - 100
        build.rect.y = SIZE + 25
        frame.image = image
        frame.rect = frame.image.get_rect()
        frame.rect.x = SIZE // 2 - 150
        frame.rect.y = SIZE
        builder_sprites.draw(screen)
        clock = pygame.time.Clock()
        while frame.rect.y > SIZE - 100:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            frame.rect.y -= 250 / FPS
            build.rect.y -= 250 / FPS
            builder_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
    else:
        builder_sprites = pygame.sprite.Group()


class Board():
    def __init__(self):
        xiron, yiron, xtree, ytree, xwater, ywater, xfood, yfood = [randrange(SIZE // 40 // 2 - 4, SIZE // 40 // 2 + 4)
                                                                    for i in range(8)]
        self.width = self.height = BOARD_SIZE
        self.list = [[0 for i in range(self.width)] for j in range(self.height)]
        for i in range(self.width):
            for j in range(self.height):
                self.list[i][j] = Pole(i, j, all_sprites)
        self.list[xiron][yiron] = Resource(xiron, yiron, 'iron', all_sprites)
        self.list[xtree][ytree] = Resource(xtree, ytree, 'tree', all_sprites)
        self.list[xwater][ywater] = Resource(xwater, ywater, 'water', all_sprites)
        self.list[xfood][yfood] = Resource(xfood, yfood, 'food', all_sprites)
        self.list[SIZE // 40 // 2][SIZE // 40 // 2] = Castle(SIZE // 40 // 2, SIZE // 40 // 2, all_sprites)
        self.side_size = int(SIZE // 30)
        self.cell_size = 30
        self.top = (SIZE - self.width * self.cell_size) / 2
        self.left = (SIZE - self.width * self.cell_size) / 2

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if mouse_pos[0] >= self.top + j * self.cell_size and mouse_pos[1] >= self.top + i * self.cell_size and \
                        mouse_pos[0] <= self.cell_size + self.top + j * self.cell_size and \
                        mouse_pos[1] <= self.cell_size + self.top + i * self.cell_size:
                    return (i, j)

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def render(self):
        '''fon = pygame.transform.scale(load_image('fon.jpg'), (SIZE, SIZE))
        screen = pygame.display.set_mode((SIZE, SIZE))
        screen.blit(fon, (0, 0))'''
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
        self.rect = self.image.get_rect().move(self.y * self.cell_size + TOPLEFT, self.x * self.cell_size + TOPLEFT)
        self.is_clicked = False
        self.board.list[pos_x][pos_y] = 'human'

    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect = self.image.get_rect().move(self.y * self.cell_size + TOPLEFT, self.x * self.cell_size + TOPLEFT)

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

    def get_coords(self):
        return self.rect.x + 1, self.rect.y + 1

class Builder(Human):
    def __init__(self, pos_x, pos_y, board):
        super().__init__(pos_x, pos_y, board)

    def clicked(self):
        if self.is_clicked:
            self.is_clicked = False
        else:
            self.is_clicked = True
        builder_screen(self)


if __name__ == '__main__':
    pygame.init()
    SIZE, BOARD_SIZE, TOPLEFT = start_screen()
    screen = pygame.display.set_mode((SIZE, SIZE))
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    builder_sprites = pygame.sprite.Group()
    resources_sprites = pygame.sprite.Group()
    board = Board()
    clock = pygame.time.Clock()
    running = True
    builder = Builder(randrange(SIZE // 30 // 2 - 2, SIZE // 30 // 2 + 2),
                      randrange(SIZE // 30 // 2 - 2, SIZE // 30 // 2 + 2), board)
    screen.fill((0, 0, 0))
    player = Player()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(board.get_cell(builder.get_coords()))
                    if board.get_cell(builder.get_coords()) == board.get_cell(event.pos):
                        builder.clicked()
                if builder.is_clicked and event.button == 3:
                    if builder.can_move(board.get_cell(event.pos)):
                        x, y = board.get_cell(event.pos)
                        builder.move(x, y)
                else:
                    board.get_click(event.pos)
        fon_paint()
        all_sprites.draw(screen)
        board.render()
        builder_sprites.draw(screen)
        #resources_screen(player.resources)
        resources_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
