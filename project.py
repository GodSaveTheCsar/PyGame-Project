import pygame
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import os
from random import randrange, choice
import sqlite3

SIZE = 1000
FPS = 120
CELL_SIZE = 30
BUILDINGS = {'Fort': '100 wood, 50 iron', 'Sawmill': '150 wood, 100 iron, 75 food', 'Pyramid': '300 wood, 200 iron',
             'Shaft': '150 wood, 100 iron, 100 food', 'Farm': '75 wood, 75 iron, 200 food'}


# рисование фона
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


# обычное поле
class Field(Tile):
    def __init__(self, x, y, sprites, cell_size):
        super().__init__(x, y, sprites)
        self.image = pygame.transform.scale(load_image('Field.png'), (cell_size, cell_size))
        self.rect = self.image.get_rect().move(y*CELL_SIZE + TOPLEFT, x*CELL_SIZE + TOPLEFT)
        self.name = 'field'
        self.x = x
        self.y = y

    def get_building_name(self):
        return 'pyramid'

    def get_coords(self):
        return self.x, self.y

    def build(self, building, board):
        if building == 'Fort':
            player.castle = True
            board.list[self.x][self.y] = Castle(self.x, self.y, all_sprites)
        else:
            board.list[self.x][self.y] = Pyramid(self.x, self.y, all_sprites, 30)
            board.passive['brilliant'] += 25


# классы зданий
class Building(Tile):
    def __init__(self, x, y, name, sprites, cell_size):
        super().__init__(x, y, sprites)
        self.image = pygame.transform.scale(load_image(f'{name}.png'), (cell_size, cell_size))
        self.rect = self.image.get_rect().move(y*CELL_SIZE + TOPLEFT, x*CELL_SIZE + TOPLEFT)
        self.name = name


class Pyramid(Building):
    def __init__(self, x, y, sprites, cell_size):
        super().__init__(x, y, sprites)
        self.image = pygame.transform.scale(load_image('pyramid.png'), (cell_size, cell_size))
        self.rect = self.image.get_rect().move(y*CELL_SIZE + TOPLEFT, x*CELL_SIZE + TOPLEFT)
        self.name = 'pyramid'


class Castle(Building):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(load_image('Fort.png'), (30, 30))
        self.rect = self.image.get_rect().move(y*CELL_SIZE + TOPLEFT, x*CELL_SIZE + TOPLEFT)


# класс самого игрока
class Player:
    def __init__(self):
        self.resources = {
            'iron': 0,
            'food': 0,
            'wood': 0,
            'brilliant': 0
        }
        self.hp = 100
        self.castle = False

    def update_resources(self, name, val):
        self.resources[name] += val

    def hp_update(self, val):
        self.hp += val


# ресурсы
class Resource(Tile):
    def __init__(self, x, y, name, sprites):
        super().__init__(x, y, sprites)
        self.x = x
        self.y = y
        self.name = name
        self.is_mining = False
        if name == 'wood':
            self.image = pygame.transform.scale(load_image('tree.png'), (30, 30))
            self.rect = self.image.get_rect().move(y*CELL_SIZE + TOPLEFT, x*CELL_SIZE + TOPLEFT)
        if name == 'iron':
            self.image = pygame.transform.scale(load_image('iron.png'), (30, 30))
            self.rect = self.image.get_rect().move(y*CELL_SIZE + TOPLEFT, x*CELL_SIZE + TOPLEFT)
        if name == 'food':
            self.image = pygame.transform.scale(load_image('food.png'), (30, 30))
            self.rect = self.image.get_rect().move(y*CELL_SIZE + TOPLEFT, x*CELL_SIZE + TOPLEFT)

    def mine(self):
        # добыча ресурса
        value = get_primer(self.name)
        if value:
            player.resources[self.name] += value
            Field(self.x, self.y, all_sprites, 30)

    def get_coords(self):
        return self.x, self.y

    def get_building_name(self):
        # получение названия здания, на которое ресурс будет поставлен
        if self.name == 'wood':
            name = 'sawmill'
        if self.name == 'iron':
            name = 'shaft'
        if self.name == 'food':
            name = 'farm'
        return name

    def build(self, building, board):
        # строительство здания
        if building == 'Sawmill':
            self.image = pygame.transform.scale(load_image('sawmill.png'), (30, 30))
            self.rect = self.image.get_rect().move(self.y*CELL_SIZE + TOPLEFT, self.x*CELL_SIZE + TOPLEFT)
            board.passive[self.name] += 25
        if building == 'Shaft':
            self.image = pygame.transform.scale(load_image('shaft.png'), (30, 30))
            self.rect = self.image.get_rect().move(self.y*CELL_SIZE + TOPLEFT, self.x*CELL_SIZE + TOPLEFT)
            board.passive[self.name] += 25
        if building == 'Farm':
            self.image = pygame.transform.scale(load_image('farm.png'), (30, 30))
            self.rect = self.image.get_rect().move(self.y*CELL_SIZE + TOPLEFT, self.x*CELL_SIZE + TOPLEFT)
            board.passive[self.name] += 25
        elif building == 'Fort':
            self.image = pygame.transform.scale(load_image('fort.png'), (30, 30))
            self.rect = self.image.get_rect().move(self.y*CELL_SIZE + TOPLEFT, self.x*CELL_SIZE + TOPLEFT)
            player.castle = True
        board.list[self.x][self.y] = Building(self.x, self.y, building, all_sprites, 30)


def get_primer(name):
    # получить пример для добычи ресурса
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
                    return int(20/(pygame.time.get_ticks() - start_ticks)*100000)
                else:
                    return 10
            if event.type == pygame.QUIT or ex1.closed:
                return 0
        clock.tick(FPS)


# меню, возникающее при нажатии на молоток
class Build_menu(QWidget):
    def __init__(self, player, tile):
        super().__init__()
        uic.loadUi('build_menu.ui', self)  # Загружаем дизайн
        self.player = player
        self.button_1.clicked.connect(self.run)
        self.button_2.clicked.connect(self.run)
        self.tile = tile
        name = tile.get_building_name().capitalize()
        self.resources = BUILDINGS[name].split(',')
        self.building_1.setText(name)
        self.price_1.setText(BUILDINGS[name])
        self.can_build = False
        if player.castle:
            self.price_2.hide()
            self.building_2.hide()
            self.build.hide()
        else:
            self.price_2.setText(BUILDINGS['Fort'])
            self.building_2.setText('Fort')

    def run(self):
        a = True
        for i in self.resources:
            i = i.strip().split(' ')
            name = i[1]
            price = int(i[0])
            if player.resources[name] >= price:
                player.resources[name] -= price
                continue
            else:
                a = False
                self.error.setText('Not enough resources')
        if a:
            print(player.resources)
            self.can_build = True
            self.selected_building = self.tile.get_building_name().capitalize() if self.sender() \
                                                                                   == self.button_1 else 'Fort'
            self.close()


# меню, возникающее при нажатии на кирку
# неоюходимо для получения ресурсов
class MyWidget_primer(QMainWindow):
    def __init__(self, name):
        super().__init__()
        uic.loadUi('primer.ui', self)  # Загружаем дизайн
        self.is_pushed = False
        self.closed = False
        con = sqlite3.connect("data/equations.db")
        cur = con.cursor()
        if name == 'wood':
            self.result = choice(cur.execute("""SELECT * FROM primeri WHERE type = 'example'""").fetchall())
        if name == 'food':
            self.result = choice(cur.execute("""SELECT * FROM primeri WHERE type = 'lin_equation'""").fetchall())
        if name == 'iron':
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


class Game_information(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('information.ui', self)


# меню, где можно выбрать размер карты и узнать правила игры
class Start_menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('start_menu.ui', self)  # Загружаем дизайн
        self.is_pushed = False
        self.small.clicked.connect(self.run)
        self.medium.clicked.connect(self.run)
        self.big.clicked.connect(self.run)
        self.information.clicked.connect(self.get_information)

    def run(self):
        size = int(self.sender().text().split('(')[1][0:2])
        self.size = size*30 + 320
        self.board_size = int(self.sender().text().split('(')[1][0:2])
        self.topleft = int((self.size - size*CELL_SIZE)/2)
        self.is_pushed = True
        self.close()

    def get_information(self):
        app = QApplication(sys.argv)
        info = Game_information()
        info.show()
        app.exec_()


# Интро
def start_screen():
    pygame.init()
    clock = pygame.time.Clock()
    app = QApplication(sys.argv)
    ex = Start_menu()
    ex.show()
    while True:
        if ex.is_pushed:
            return ex.size, ex.board_size, ex.topleft
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)


# экран с ресурсами, находящийся сверху
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
    food_i.rect.x = SIZE//4
    food_i.rect.y = 0
    wood_i.image = wood
    wood_i.rect = wood_i.image.get_rect()
    wood_i.rect.x = 2*SIZE//4
    wood_i.rect.y = 0
    brilliant_i.image = brilliant
    brilliant_i.rect = brilliant_i.image.get_rect()
    brilliant_i.rect.x = 3*SIZE//4
    brilliant_i.rect.y = 0
    font = pygame.font.Font(None, 30)
    resources_sprites.draw(screen)
    count = -1
    for i in resources:
        count += 1
        string_rendered = font.render(str(resources[i]), 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord = count*SIZE//4 + 50
        intro_rect.left = text_coord
        intro_rect.y = 15
        screen.blit(string_rendered, intro_rect)


# перевод названия объекта в текст, который будет написан
def name_to_text(name, checker1=False):
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(name, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    if checker1:
        if name.startswith('hp'):
            text_coord = 0
            intro_rect.left = text_coord
            intro_rect.y = 100
        else:
            text_coord = 100
            intro_rect.left = text_coord
            intro_rect.y = 100
    else:
        text_coord = SIZE//2 - 25
        intro_rect.left = text_coord
        intro_rect.y = SIZE - 100
    screen.blit(string_rendered, intro_rect)


# рамка, всплывающая при нажатии
class Frame(pygame.sprite.Sprite):
    def __init__(self, sprites, obj):
        super().__init__(sprites)
        self.image = load_image('frame.png')
        self.rect = self.image.get_rect()
        self.rect.x = SIZE//2 - 150
        self.rect.y = SIZE
        self.obj = obj

    def call(self):
        # вызов рамки
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
                self.rect.y -= 600/FPS
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
            pickaxe.rect.y = self.rect.y + 10
            object = pygame.sprite.Sprite(object_sprites)
            object.image = pygame.transform.scale(obj.image, (75, 100))
            object.rect = object.image.get_rect()
            object.rect.x = self.rect.x + 200
            object.rect.y = self.rect.y
            while self.rect.y > SIZE - 100:
                self.rect.y -= 600/FPS
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
                self.rect.y -= 600/FPS
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
        board.frames[-1].call()


def mine_or_build_click(x, y):
    if SIZE//3 < x < SIZE//3 + 100:
        if y > SIZE - 150:
            return True


# кнопка для следующего хода
class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.turn = 1
        self.image = self.image = pygame.transform.scale(load_image('next_turn.png'), (50, 50))
        self.rect = self.image.get_rect().move(SIZE - 50, 50)

    def next_turn_click(self, x, y):
        if x > SIZE - 50 and 50 < y < 100:
            self.turn += 1
            board.next_turn()
            return True
        else:
            return False


def lose():
    global running
    running = False


# игровое поле
class Board:
    def __init__(self):
        self.side_size = int(SIZE//30)
        self.cell_size = 30
        self.width = self.height = BOARD_SIZE
        self.list = [[Field(i, j, all_sprites, self.cell_size) for i in range(self.width)] for j in range(self.height)]
        self.frames = []
        self.passive = {
            'iron': 0,
            'food': 0,
            'wood': 0,
            'brilliant': 0
        }
        self.turn = 1
        #  случайная генерация железа, дерева и еды
        for x_iron in range(0, self.width, 4):
            for y_iron in range(0, self.width, 3):
                for x in range(randrange(2, 4)):
                    for y in range(randrange(2, 4)):
                        if x*(x_iron + 1) >= self.width or y*(y_iron + 1) >= self.width:
                            continue
                        if self.list[x*(x_iron + 1)][y*(y_iron + 1)].__class__.__name__ == 'Resource':
                            continue
                        self.list[x*(x_iron + 1)][y*(y_iron + 1)] = Resource(x*(x_iron + 1), y*(y_iron + 1),
                                                                             'iron', all_sprites)
        for x_tree in range(0, self.width, 2):
            for y_tree in range(0, self.width, 2):
                for x in range(randrange(2, 4)):
                    for y in range(randrange(1, 4)):
                        if x*(x_tree + 1) >= self.width or y*(y_tree + 1) >= self.width:
                            continue
                        if self.list[x*(x_tree + 1)][y*(y_tree + 1)].__class__.__name__ == 'Resource':
                            continue
                        self.list[x*(x_tree + 1)][y*(y_tree + 1)] = Resource(x*(x_tree + 1), y*(y_tree + 1),
                                                                             'wood', all_sprites)
        for x_food in range(0, self.width, 2):
            for y_food in range(0, self.width, 2):
                for x in range(3):
                    for y in range(randrange(1, 3)):
                        if x*(x_food + 1) >= self.width or y*(y_food + 1) >= self.width:
                            continue
                        if self.list[x*(x_food + 1)][y*(y_food + 1)].__class__.__name__ == 'Resource':
                            continue
                        self.list[x*(x_food + 1)][y*(y_food + 1)] = Resource(x*(x_food + 1), y*(y_food + 1),
                                                                             'food', all_sprites)

        self.top = (SIZE - self.width*self.cell_size)/2
        self.left = (SIZE - self.width*self.cell_size)/2
        self.units = []
        self.units.append(Builder(randrange(SIZE//30//2 - 3, SIZE//30//2),
                                  randrange(SIZE//30//2 - 3, SIZE//30//2), self))
        self.scout_can_go = True
        self.builder_can_go = True

    def next_turn(self):
        # следующий ход
        self.turn += 1
        player.update_resources('wood', self.passive['wood'])
        player.update_resources('iron', self.passive['iron'])
        player.update_resources('food', self.passive['food'])
        player.update_resources('brilliant', self.passive['brilliant'])
        self.scout_can_go = True
        self.builder_can_go = True
        if self.turn%10 == 0:
            player.hp_update(int(-10*((self.turn/10)*3) ** 1.5))
        if player.hp <= 0:
            lose()
        checker.upd_text()

    def get_cell(self, mouse_pos):
        # отлавливание клетки, на которую нажал игрок
        for i in range(self.height):
            for j in range(self.width):
                if self.top + j*self.cell_size <= mouse_pos[0] <= self.cell_size + self.top + j*self.cell_size and \
                        self.top + i*self.cell_size <= mouse_pos[1] <= self.cell_size + self.top + i*self.cell_size:
                    return i, j

    def on_click(self, cell_coords, event):
        # реакция на клик
        if event.button == 1:
            changer_check(event.pos)
            button.next_turn_click(event.pos[0], event.pos[1])
            info.info_click(event.pos[0], event.pos[1])
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
        elif event.button == 3:
            if mine_or_build_click(event.pos[0], event.pos[1]):
                if board.frames[-1].obj.__class__.__name__ == 'Resource':
                    for i in self.list:
                        for j in i:
                            if j.is_clicked and j.__class__.__name__ == 'Resource':
                                j.mine()
                if board.frames[-1].obj.__class__.__name__ == 'Builder':
                    for i in self.units:
                        if i.is_clicked and i.__class__.__name__ == 'Builder':
                            i.build()
            else:
                for i in self.units:
                    if (i.__class__.__name__ == 'Builder' and self.builder_can_go) or (
                            i.__class__.__name__ == 'Scout' and self.scout_can_go):
                        if i.is_clicked and i.can_move(cell_coords):
                            i.move(cell_coords[0], cell_coords[1])
                            if i.__class__.__name__ == 'Builder':
                                self.builder_can_go = False
                            else:
                                self.scout_can_go = False
                            break

    def passive_update(self, name, val):
        # добавление ресурсов за здания
        self.passive[name] += val

    def get_click(self, mouse_pos, event):
        # преобразование координат мыши в координаты клетки
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, event)

    def render(self):
        # обновление поля
        self.top = (SIZE - self.width*self.cell_size)/2
        self.left = (SIZE - self.width*self.cell_size)/2
        for i in range(self.height):
            for j in range(self.width):
                for e in self.units:
                    if e.is_clicked:
                        name_to_text(e.name)
                        break
                else:
                    if self.list[i][j].is_clicked:
                        name_to_text(self.list[i][j].name)
                pygame.draw.rect(screen, (255, 255, 255), (self.top + j*self.cell_size, self.top + i
                                                           *self.cell_size, self.cell_size, self.cell_size), 1)

    def show_info(self):
        app = QApplication(sys.argv)
        inform = Game_information()
        inform.show()
        app.exec_()


def changer_check(coords):
    x = coords[0]
    y = coords[1]
    if x > SIZE//3 and x < 2*(SIZE//3) and y > 50 and y < 150:
        changer.change()


# обмен сапфиров на жизни
class Changer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.txt = 'обмен 10 алмазов на 3 жизней'
        self.image = pygame.transform.scale(load_image('checker.jpg'), (int(SIZE/3), 100))
        self.rect = self.image.get_rect().move(SIZE//3, 50)

    def change(self):
        if player.resources['brilliant'] >= 10:
            hp_up = player.resources['brilliant']//10*3
            player.resources['brilliant'] = player.resources['brilliant']%10
            player.hp += hp_up


# надписи на экране: какой сейчас ход и сколько у игрока осталось здоровья
class Turn_checker(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('checker.jpg'), (100, 100))
        self.rect = self.image.get_rect().move(0, 50)

    def upd_text(self):
        name_to_text('turn: ' + str(board.turn), checker1=True)
        name_to_text('hp: ' + str(player.hp), checker1=True)


class Info_button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('info_button.png'), (50, 50))
        self.rect = self.image.get_rect().move(SIZE - 100, 50)

    def info_click(self, x, y):
        if SIZE - 50 > x > SIZE - 100 and 50 < y < 100:
            board.show_info()
            return True
        else:
            return False


# класс человека
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
        self.rect = self.image.get_rect().move(self.y*self.cell_size + TOPLEFT, self.x*self.cell_size + TOPLEFT)

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


# строитель
class Builder(Human):
    def __init__(self, pos_x, pos_y, board):
        super().__init__(pos_x, pos_y, board)
        self.image = load_image('builder.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect().move(self.y*self.cell_size + TOPLEFT, self.x*self.cell_size + TOPLEFT)
        self.name = 'builder'

    def can_move(self, coords):
        # проверка, может ли ходить
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
        # строительство
        for i in self.board.list:
            for j in i:
                if j.__class__.__name__ == 'Resource' and (self.x, self.y) == j.get_coords():
                    self.building_menu(player, j)
                if j.__class__.__name__ == 'Field' and (self.x, self.y) == j.get_coords():
                    self.building_menu(player, j)

    def building_menu(self, player, name):
        # вызов меню
        app = QApplication(sys.argv)
        build_menu = Build_menu(player, name)
        build_menu.show()
        app.exec_()
        if build_menu.can_build:
            building = build_menu.selected_building
            name.build(building, self.board)


# разведчик
class Scout(Human):
    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        self.image = load_image('scout.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect().move(self.y*self.cell_size + TOPLEFT, self.x*self.cell_size + TOPLEFT)
        self.name = 'scout'

    def can_move(self, coords):
        x = coords[0]
        y = coords[1]
        if abs(self.x - x) <= 2 and abs(self.y - y) <= 2 and (x, y) not in [i.get_coords() for i in self.board.units]:
            return True
        else:
            return False


class Lose_Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('lose_window.ui', self)  # Загружаем дизайн
        x = board.turn
        self.label.setText(f'Поздравляем! вы продержались столько ходов: {x}')


def lose_window():
    app = QApplication(sys.argv)
    lose_window1 = Lose_Window()
    lose_window1.show()
    app.exec_()


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
    info = Info_button()
    checker = Turn_checker()
    changer = Changer()
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
        checker.upd_text()
        pygame.display.flip()
        clock.tick(FPS)
lose_window()
