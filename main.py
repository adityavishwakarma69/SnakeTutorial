import pygame
from pygame.locals import *
from random import randint
pygame.init()


CELL_SIZE = 25
GRID_SIZE_X = 20
GRID_SIZE_Y = 20
WIN_SIZE = (CELL_SIZE * GRID_SIZE_X, CELL_SIZE * GRID_SIZE_Y)

def draw_text(surface, text, font, colorfg, pos, size):
    font = pygame.font.Font(font, size)
    font_surface = font.render(text, True, colorfg)
    surface.blit(font_surface, pos)

class Snake:
    def __init__(self, cell_size, grid_size_x, grid_size_y):
        self.rect = pygame.Rect(0, 0, cell_size, cell_size)
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.cell_size = cell_size
        self.tail = [self.rect]
        self.tail_len = 1
        self.movement = [0, 0]
        self.margin = 2

    def draw(self, surface):
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        for block in self.tail:
            pygame.draw.rect(surface, (0, 255, 0), (block.x + self.margin, block.y + self.margin, self.cell_size - self.margin, self.cell_size - self.margin))

    def move(self):
        self.rect.x += self.movement[0] * self.rect.width
        self.rect.y += self.movement[1] * self.rect.height

    def set_movement(self, move):
        if move == "UP" and self.get_movement() != "DOWN":
            self.movement[0] = 0
            self.movement[1] = -1
        elif move == "DOWN" and self.get_movement() != "UP":
            self.movement[0] = 0
            self.movement[1] = 1
        elif move == "LEFT" and self.get_movement() != "RIGHT":
            self.movement[0] = -1
            self.movement[1] = 0
        elif move == "RIGHT" and self.get_movement() != "LEFT":
            self.movement[0] = 1
            self.movement[1] = 0

    def get_movement(self):
        if self.movement[0] == 0 and self.movement[1] == 0:
            return "STILL"
        elif self.movement[0] == 0 and self.movement[1] == -1:
            return "UP"
        elif self.movement[0] == 0 and self.movement[1] == 1:
            return "DOWN"
        elif self.movement[0] == 1 and self.movement[1] == 0:
            return "RIGHT"
        elif self.movement[0] == -1 and self.movement[1] == 0:
            return "LEFT"

    def check_collision(self, rect):
        return self.rect.x == rect.x and self.rect.y == rect.y

    def update(self):
        self.tail.append(pygame.Rect(self.rect))
        if len(self.tail) > self.tail_len:
            self.tail.pop(0)

        if self.rect.x//self.cell_size >= self.grid_size_x or self.rect.y//self.cell_size >= self.grid_size_y or self.rect.x < 0 or self.rect.y < 0 or self.rect in self.tail[:-1]:
            return -1
        return 0

class Food:
    def __init__(self, cell_size, grid_size_x, grid_size_y):
        self.rect = pygame.Rect(0, 0, cell_size, cell_size)
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.cell_size = cell_size
        self.margin = 2

    def spawn(self, snake):
        while self.rect in snake.tail:
            self.rect.x = randint(0, self.grid_size_x - 1) * self.cell_size
            self.rect.y = randint(0, self.grid_size_y - 1) * self.cell_size

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x + self.margin, self.rect.y + self.margin, self.rect.width - self.margin, self.rect.height - self.margin))

screen = pygame.display.set_mode((WIN_SIZE))
snake = Snake(CELL_SIZE, GRID_SIZE_X, GRID_SIZE_Y)
food = Food(CELL_SIZE, GRID_SIZE_X, GRID_SIZE_Y)
food.spawn(snake)

move_event = pygame.USEREVENT + 100
pygame.time.set_timer(move_event, 300)

snake.set_movement("RIGHT")

event_queue = []
event_queue_limit = 3

score = 0
try:
    with open('.highscore', 'r') as hsf:
        highscore = int(hsf.read())
except:
    with open('.highscore', 'w') as hsf:
        hsf.write('0')
        highscore = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        elif event.type == move_event:
            if len(event_queue) > 0:
                key =  event_queue.pop(0)
                if key == K_UP:
                    snake.set_movement("UP")
                elif key == K_DOWN:
                    snake.set_movement("DOWN")
                elif key == K_LEFT:
                    snake.set_movement("LEFT")
                elif key == K_RIGHT:
                    snake.set_movement("RIGHT")
            snake.move()
            update_code = snake.update()
            if update_code == -1:
                if score > highscore:
                    with open('.highscore', 'w') as hsf:
                        hsf.write(str(score))
                exit()
            if snake.check_collision(food.rect):
                food.spawn(snake)
                snake.tail_len += 1
                score += 1

        elif event.type == KEYDOWN:
            if len(event_queue) < event_queue_limit:
                event_queue.append(event.key)


    screen.fill((0, 0, 0))

    draw_text(screen, '󰫣 ' + f"{score} : {highscore}", "ProFontIIxNerdFont-Regular.ttf", (0, 255, 0), (0, 0), 20)
    snake.draw(screen)
    food.draw(screen)

    pygame.display.flip()
