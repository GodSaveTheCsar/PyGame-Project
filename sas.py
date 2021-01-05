import pygame
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
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

class MyWidget(QMainWindow):
    def __init__(self):
        global SIZE
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

def start_screen():
    pygame.init()
    clock = pygame.time.Clock()
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    while True:
        if ex.a:
            return ex.size
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(FPS)

class Board():
    def __init__(self):
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


if __name__ == '__main__':
    pygame.init()
    SIZE = start_screen()
    screen = pygame.display.set_mode((SIZE, SIZE))
    board = Board()
    clock = pygame.time.Clock()
    running = True
    player = None
    screen.fill((0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()
