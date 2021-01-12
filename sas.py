import pygame
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
from random import randrange, choice
import sqlite3

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
        self.is_clicked = False

    def click(self):
        self.is_clicked = True
        object_screen(self)

    def unclick(self):
        self.is_clicked = False
        object_screen(self)


class Field(Tile):
    def __init__(self, x, y, sprites, cell_size):
        super().__init__(x, y, sprites)
        self.image = pygame.transform.scale(load_image('Field.png'), (cell_size, cell_size))
        self.rect = self.image.get_rect().move(y * CELL_SIZE + TOPLEFT, x * CELL_SIZE + TOPLEFT)
        self.name = 'field'
        self.x = x
        self.y = y

    def build(self):
        board.list[self.x][self.y] = Pyramid(self.x, self.y, all_sprites, CELL_SIZE)

    def get_coords(self):
        return (self.x, self.y)


class Pyramid(Tile):
    def __init__(self, x, y, sprites, cell_size):
        super().__init__(x, y, sprites)
        self.image = pygame.transform.scale(load_image('pyramid.png'), (cell_size, cell_size))
        self.rect = self.image.get_rect().move(y * CELL_SIZE + TOPLEFT, x * CELL_SIZE + TOPLEFT)
        self.name = 'pyramid'
        board.passive_update('brilliant', 2)


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
            'iron': 0,
            'food': 0,
            'tree': 0,
            'brilliant': 0
        }
        self.hp = 100

    def update_resources(self, name, val):
        self.resources[name] += val

    def hp_update(self, val):
        self.hp += val


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
        if name == 'food':
            self.image = pygame.transform.scale(load_image('food.png'), (30, 30))
            self.rect = self.image.get_rect().move(y * CELL_SIZE + TOPLEFT, x * CELL_SIZE + TOPLEFT)

    def mine(self):
        player.resources[self.name] += get_primer(self.name)

    def get_coords(self):
        return (self.x, self.y)

    def build(self):
        if self.name == 'tree':
            self.name = 'samwill'
            self.image = pygame.transform.scale(load_image('samwill.png'), (30, 30))
            self.rect = self.image.get_rect().move(self.y * CELL_SIZE + TOPLEFT, self.x * CELL_SIZE + TOPLEFT)
            board.passive_update('tree', 2)
        if self.name == 'iron':
            self.name = 'shaft'
            self.image = pygame.transform.scale(load_image('shaft.jpg'), (30, 30))
            self.rect = self.image.get_rect().move(self.y * CELL_SIZE + TOPLEFT, self.x * CELL_SIZE + TOPLEFT)
            board.passive_update('iron', 2)
        if self.name == 'food':
            self.name = 'farm'
            self.image = pygame.transform.scale(load_image('farm.jpg'), (30, 30))
            self.rect = self.image.get_rect().move(self.y * CELL_SIZE + TOPLEFT, self.x * CELL_SIZE + TOPLEFT)
            board.passive_update('food', 2)
        if self.name == 'brilliant':
            self.name = 'oracle'
            self.image = pygame.transform.scale(load_image('tree.png'), (30, 30))
            self.rect = self.image.get_rect().move(self.y * CELL_SIZE + TOPLEFT, self.x * CELL_SIZE + TOPLEFT)
            board.passive_update('ora', 2)




def get_primer(name):
    pygame.init()
    clock = pygame.time.Clock()
    app = QApplication(sys.argv)
    start_ticks = pygame.time.get_ticks()
    ex1 = MyWidget_primer(name)
    ex1.show()
    while True:
        for event in pygame.event.get():
            if ex1.is_pushed:
                if ex1.is_true:
                    return int(20 / (pygame.time.get_ticks() - start_ticks) * 100000)
                else:
                    return 10
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)


class MyWidget_primer(QMainWindow):
    def __init__(self, name):
        super().__init__()
        uic.loadUi('primer.ui', self)  # Загружаем дизайн
        self.is_pushed = False
        con = sqlite3.connect("data/equations.db")
        cur = con.cursor()
        if name == 'tree' or name == 'iron':
            self.result = choice(cur.execute("""SELECT * FROM primeri WHERE type = 'example'""").fetchall())
        if name == 'food':
            self.result = choice(cur.execute("""SELECT * FROM primeri WHERE type = 'lin_equation'""").fetchall())
        if name == 'brilliant':
            self.result = choice(cur.execute("""SELECT * FROM primeri WHERE type = 'quad_equation'""").fetchall())
        self.pushButton.clicked.connect(self.run)
        self.label.setText(str(self.result[1]))
        self.otvet = str(self.result[-1])

    def run(self):
        self.is_pushed = True
        if self.lineEdit.text().strip() == self.otvet:
            self.is_true = True
        else:
            self.is_true = False
        self.close()



class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)  # Загружаем дизайн
        self.is_pushed = False
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.run)

    def run(self):
        size = int(self.sender().text().split('(')[1][0:2])
        self.size = size * 30 + 320
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


def name_to_text(name):
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(name, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    text_coord = SIZE // 2 - 25
    intro_rect.left = text_coord
    intro_rect.y = SIZE - 100
    screen.blit(string_rendered, intro_rect)
    
class Frame(pygame.sprite.Sprite):
    def __init__(self, sprites, obj):
        super().__init__(sprites)
        self.image = load_image('frame.png')
        self.rect = self.image.get_rect()
        self.rect.x = SIZE // 2 - 150
        self.rect.y = SIZE
        self.obj = obj

    def call(self, obj):
        obj = self.obj
        if obj.__class__.__name__ == 'Resource':
            pickaxe = pygame.sprite.Sprite(object_sprites)
            pickaxe.image = pygame.transform.scale(load_image('pickaxe.png'), (40, 80))
            pickaxe.rect = pickaxe.image.get_rect()
            pickaxe.rect.x = self.rect.x + 50
            pickaxe.rect.y = self.rect.y + 25
            object = pygame.sprite.Sprite(object_sprites)
            object.image = pygame.transform.scale(obj.image, (100, 100))
            object.rect = object.image.get_rect()
            object.rect.x = self.rect.x + 200
            object.rect.y = self.rect.y
            while self.rect.y > SIZE - 100:
                self.rect.y -= 600 / FPS
                if self.rect.y < SIZE - 100:
                    self.rect.y = SIZE - 100
                pickaxe.rect.y = self.rect.y + 25
                object.rect.y = self.rect.y
                object_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)
        elif obj.name == 'builder':
            pickaxe = pygame.sprite.Sprite(object_sprites)
            pickaxe.image = pygame.transform.scale(load_image('hammer.png'), (80, 80))
            pickaxe.rect = pickaxe.image.get_rect()
            pickaxe.rect.x = self.rect.x + 50
            pickaxe.rect.y = self.rect.y + 25
            object = pygame.sprite.Sprite(object_sprites)
            object.image = pygame.transform.scale(obj.image, (100, 100))
            object.rect = object.image.get_rect()
            object.rect.x = self.rect.x + 200
            object.rect.y = self.rect.y
            while self.rect.y > SIZE - 100:
                self.rect.y -= 600 / FPS
                if self.rect.y < SIZE - 100:
                    self.rect.y = SIZE - 100
                pickaxe.rect.y = self.rect.y + 25
                object.rect.y = self.rect.y
                object_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)
        else:
            object = pygame.sprite.Sprite(object_sprites)
            object.image = pygame.transform.scale(obj.image, (100, 100))
            object.rect = object.image.get_rect()
            object.rect.x = self.rect.x + 200
            object.rect.y = self.rect.y
            while self.rect.y > SIZE - 100:
                self.rect.y -= 600 / FPS
                if self.rect.y < SIZE - 100:
                    self.rect.y = SIZE - 100
                object.rect.y = self.rect.y
                object_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)


def object_screen(obj):
    global object_sprites
    board.frames = []
    board.frames.append(Frame(object_sprites, obj))
    if obj.is_clicked:
        board.frames[-1].call(1)


def mine_or_build_click(x, y):
    if x > SIZE // 3 and x < SIZE // 3 + 100:
        if y > SIZE - 150:
            return True




class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.turn = 1
        self.image = self.image = pygame.transform.scale(load_image('knopka.jpg'), (100, 100))
        self.rect = self.image.get_rect().move(SIZE - 100, 50)

    def next_turn_click(self, x, y):
        if x > SIZE - 100 and y > 50 and y < 150:
            self.turn += 1
            board.next_turn()
            print(self.turn)
            return True
        else:
            return False


def lose():
    running = False


class Board():
    def __init__(self):
        self.side_size = int(SIZE // 30)
        self.cell_size = 30
        self.width = self.height = BOARD_SIZE
        self.list = [[Field(i, j, all_sprites, self.cell_size) for i in range(self.width)] for j in range(self.height)]
        self.frames = []
        self.passive = {
            'iron': 0,
            'food': 0,
            'tree': 0,
            'brilliant': 0
        }
        self.turn = 1
        #  случайная генерация железа, дерева и еды
        for x_iron in range(0, self.width, 4):
            for y_iron in range(0, self.width, 3):
                for x in range(randrange(2, 4)):
                    for y in range(randrange(2, 4)):
                        if x * (x_iron + 1) >= self.width or y * (y_iron + 1) >= self.width:
                            continue
                        if self.list[x * (x_iron + 1)][y * (y_iron + 1)].__class__.__name__ == 'Resource':
                            continue
                        self.list[x * (x_iron + 1)][y * (y_iron + 1)] = Resource(x * (x_iron + 1), y * (y_iron + 1),
                                                                                 'iron', all_sprites)
        for x_tree in range(0, self.width, 2):
            for y_tree in range(0, self.width, 2):
                for x in range(randrange(2, 4)):
                    for y in range(randrange(1, 4)):
                        if x * (x_tree + 1) >= self.width or y * (y_tree + 1) >= self.width:
                            continue
                        if self.list[x * (x_tree + 1)][y * (y_tree + 1)].__class__.__name__ == 'Resource':
                            continue
                        self.list[x * (x_tree + 1)][y * (y_tree + 1)] = Resource(x * (x_tree + 1), y * (y_tree + 1),
                                                                                 'tree', all_sprites)
        for x_food in range(0, self.width, 2):
            for y_food in range(0, self.width, 2):
                for x in range(3):
                    for y in range(randrange(1, 3)):
                        if x * (x_food + 1) >= self.width or y * (y_food + 1) >= self.width:
                            continue
                        if self.list[x * (x_food + 1)][y * (y_food + 1)].__class__.__name__ == 'Resource':
                            continue
                        self.list[x * (x_food + 1)][y * (y_food + 1)] = Resource(x * (x_food + 1), y * (y_food + 1),
                                                                                 'food', all_sprites)

        self.top = (SIZE - self.width * self.cell_size) / 2
        self.left = (SIZE - self.width * self.cell_size) / 2
        self.units = []
        self.units.append(Builder(randrange(SIZE // 30 // 2 - 2, SIZE // 30 // 2 + 2),
                                  randrange(SIZE // 30 // 2 - 2, SIZE // 30 // 2 + 2), self))
        self.units.append(Scout(randrange(SIZE // 30 // 2 - 2, SIZE // 30 // 2 + 2),
                                randrange(SIZE // 30 // 2 - 2, SIZE // 30 // 2 + 2), self))
        self.scout_can_go = True
        self.builder_can_go = True

    def next_turn(self):
        self.turn += 1
        player.update_resources('tree', self.passive['tree'])
        player.update_resources('iron', self.passive['iron'])
        player.update_resources('food', self.passive['food'])
        player.update_resources('brilliant', self.passive['brilliant'])
        self.scout_can_go = True
        self.builder_can_go = True
        if self.turn % 10 == 0:
            player.hp_update(-10 * ((turn % 10) * 0.7)**2)
        if player.hp <= 0:
            lose()



    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if self.top + j * self.cell_size <= mouse_pos[0] <= self.cell_size + self.top + j * self.cell_size and \
                        self.top + i * self.cell_size <= mouse_pos[1] <= self.cell_size + self.top + i * self.cell_size:
                    return i, j

    def on_click(self, cell_coords, event):
        if event.button == 1:
            button.next_turn_click(event.pos[0], event.pos[1])
            for i in self.units:
                if i.get_coords() == cell_coords:
                    if i.is_clicked:
                        self.list[cell_coords[0]][cell_coords[1]].click()
                        i.unclick()
                        break
                    else:
                        i.click()
                        break
                else:
                    i.unclick()
            else:
                for i in range(len(self.list)):
                    for e in range(len(self.list)):
                        if (i, e) == cell_coords:
                            tile = self.list[i][e]
                            if tile.is_clicked:
                                tile.unclick()
                            else:
                                tile.click()
                        else:
                            tile = self.list[i][e]
                            tile.unclick()
        if event.button == 3:
            if mine_or_build_click(event.pos[0], event.pos[1]):
                print([i.obj for i in board.frames])
                if board.frames[-1].obj.__class__.__name__ == 'Resource':
                    for i in self.list:
                        for j in i:
                            print(1)
                            if j.is_clicked and j.__class__.__name__ == 'Resource':
                                print(2)
                                j.mine()
                if board.frames[-1].obj.__class__.__name__ == 'Builder':
                    for i in self.units:
                        if i.is_clicked and i.__class__.__name__ == 'Builder':
                            i.build()
            else:
                for i in self.units:
                    if (i.__class__.__name__ == 'Builder' and self.builder_can_go) or (i.__class__.__name__ == 'Scout' and self.scout_can_go):
                        if i.is_clicked and i.can_move(cell_coords):
                            i.move(cell_coords[0], cell_coords[1])
                            if i.__class__.__name__ == 'Builder':
                                self.builder_can_go = False
                            else:
                                self.scout_can_go = False
                            break

    def passive_update(self, name, val):
        self.passive[name] += val

    def get_click(self, mouse_pos, event):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, event)

    def render(self):
        self.top = (SIZE - self.width * self.cell_size) / 2
        self.left = (SIZE - self.width * self.cell_size) / 2
        for i in range(self.height):
            for j in range(self.width):
                for e in self.units:
                    if e.is_clicked:
                        name_to_text(e.name)
                        break
                else:
                    if self.list[i][j].is_clicked:
                        name_to_text(self.list[i][j].name)
                pygame.draw.rect(screen, (255, 255, 255), (self.top + j * self.cell_size, self.top + i
                                                           * self.cell_size, self.cell_size, self.cell_size), 1)


class Human(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, board):
        super().__init__(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.board = board
        self.cell_size = 30
        self.is_clicked = False

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

    def click(self):
        self.is_clicked = True
        object_screen(self)

    def unclick(self):
        self.is_clicked = False
        object_screen(self)

    def get_coords(self):
        return self.x, self.y


class Builder(Human):
    def __init__(self, pos_x, pos_y, board):
        super().__init__(pos_x, pos_y, board)
        self.image = load_image('player_stand.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect().move(self.y * self.cell_size + TOPLEFT, self.x * self.cell_size + TOPLEFT)
        self.name = 'builder'

    def can_move(self, coords):
        x = coords[0]
        y = coords[1]
        if x == self.x:
            if y == self.y:
                return False
            if y + 1 == self.y or y - 1 == self.y:
                return (x, y) not in [i.get_coords() for i in self.board.units]
        if y == self.y:
            if x == self.x:
                return False
            if x + 1 == self.x or x - 1 == self.x:
                return (x, y) not in [i.get_coords() for i in self.board.units]
        if x + 1 == self.x:
            if y == self.y:
                return False
            if y + 1 == self.y or y - 1 == self.y:
                return (x, y) not in [i.get_coords() for i in self.board.units]
        if y + 1 == self.y:
            if x == self.x:
                return False
            if x + 1 == self.x or x - 1 == self.x:
                return (x, y) not in [i.get_coords() for i in self.board.units]
        if x - 1 == self.x:
            if y == self.y:
                return False
            if y + 1 == self.y or y - 1 == self.y:
                return (x, y) not in [i.get_coords() for i in self.board.units]
        if y - 1 == self.y:
            if x == self.x:
                return False
            if x + 1 == self.x or x - 1 == self.x:
                return (x, y) not in [i.get_coords() for i in self.board.units]

    def build(self):
        for i in self.board.list:
            for j in i:
                if j.__class__.__name__ == 'Resource' and (self.x, self.y) == j.get_coords():
                    j.build()
                if j.__class__.__name__ == 'Field' and (self.x, self.y) == j.get_coords():
                    j.build()


class Scout(Human):
    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        self.image = load_image('scout.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect().move(self.y * self.cell_size + TOPLEFT, self.x * self.cell_size + TOPLEFT)
        self.name = 'scout'

    def can_move(self, coords):
        x = coords[0]
        y = coords[1]
        if abs(self.x - x) <= 2 and abs(self.y - y) <= 2 and (x, y) not in [i.get_coords() for i in self.board.units]:
            return True
        else:
            return False


def lose_window():
    pass


if __name__ == '__main__':
    SIZE, BOARD_SIZE, TOPLEFT = start_screen()
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    object_sprites = pygame.sprite.Group()
    resources_sprites = pygame.sprite.Group()
    board = Board()
    button = Button()
    clock = pygame.time.Clock()
    running = True
    screen.fill((0, 0, 0))
    player = Player()
    plus = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos, event)
        fon_paint()
        all_sprites.draw(screen)
        object_sprites.draw(screen)
        board.render()
        resources_screen(player.resources)
        resources_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
lose_window()
