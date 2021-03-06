#!/usr/bin/env python3
# Sorry windows, I never loved you

# pylint: disable=no-member

import sys
import random
import pygame as pg

# TODO:
# Make a GUI menu
# Add resize options
# Add option for speed increase
# Sounds?


pg.init()


### Options ###

EDGE_WRAP = False  # Whether hitting the edge kills you

BG_COLOR = 50, 50, 50

FPS = 5

SIZE = WIDTH, HEIGHT = 1600, 900  # Size of the game viewport
GRID = ROWS, COLUMNS = 16, 9  # Number of rows and columns

### ~~~~~~~ ###


box = box_width, box_height = int(WIDTH / ROWS), int(HEIGHT / COLUMNS)


class Seg:
    def __init__(self, arg1, arg2=None):
        if isinstance(arg1, tuple):
            self.x = arg1[0]
            self.y = arg1[1]
        else:
            self.x = arg1
            self.y = arg2

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return str(self.get())

    def addSeg(self, coords):
        self.x = self.x + coords[0]
        self.y = self.y + coords[1]

    def add(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

    def subSeg(self, coords):
        self.x = self.x - coords[0]
        self.y = self.y - coords[1]

    def sub(self, x, y):
        self.x = self.x - x
        self.y = self.y - y

    def get_box_scale(self):
        return (self.x * box_width, self.y * box_height)

    def get_next_dir(self, seg):
        if seg.x - self.x == -1 or (seg.x == ROWS - 1 and self.x == 0):
            return "left"
        if seg.x - self.x == 1 or (seg.x == 0 and self.x == ROWS - 1):
            return "right"
        if seg.y - self.y == -1 or (seg.y == COLUMNS - 1 and self.y == 0):
            return "up"
        if seg.y - self.y == 1 or (seg.y == 0 and self.y == COLUMNS - 1):
            return "down"
        return "same"

    def get(self):
        return (self.x, self.y)

    def copy(self):
        return Seg(self.get())


snake = [Seg(1, 1), Seg(2, 1), Seg(3, 1)]
snake_len = len(snake)

food = Seg(0, 0)

move_dir = "right"

screen = pg.display.set_mode(SIZE)

clock = pg.time.Clock()

head_img = pg.transform.scale(pg.image.load(
    "Images/Head.png").convert_alpha(), box)
body_img = pg.transform.scale(pg.image.load(
    "Images/Body.png").convert_alpha(), box)
tail_img = pg.transform.scale(pg.image.load(
    "Images/Tail.png").convert_alpha(), box)
curvein_img = pg.transform.scale(pg.image.load(
    "Images/CurveIn.png").convert_alpha(), box)
curveout_img = pg.transform.scale(pg.image.load(
    "Images/CurveOut.png").convert_alpha(), box)
curveover_img = pg.transform.scale(pg.image.load(
    "Images/CurveOver.png").convert_alpha(), box)
food_img = pg.transform.scale(pg.image.load(
    "Images/Food.png").convert_alpha(), box)


def handle_collision():
    print("Game Over!")
    print("Score:", snake_len)
    sys.exit(0)


def new_food():
    global food
    while food in snake:
        food = Seg(random.randint(0, ROWS - 1), random.randint(0, COLUMNS - 1))


def move_snake():
    global snake_len

    snake.append(snake[-1].copy())

    if move_dir == "right":
        if snake[-1].x == ROWS - 1:
            if EDGE_WRAP:
                snake[-1].x = 0
            else:
                handle_collision()
        else:
            snake[-1].add(1, 0)
    if move_dir == "down":
        if snake[-1].y == COLUMNS - 1:
            if EDGE_WRAP:
                snake[-1].y = 0
            else:
                handle_collision()
        else:
            snake[-1].add(0, 1)
    if move_dir == "left":
        if snake[-1].x == 0:
            if EDGE_WRAP:
                snake[-1].x = ROWS - 1
            else:
                handle_collision()
        else:
            snake[-1].sub(1, 0)
    if move_dir == "up":
        if snake[-1].y == 0:
            if EDGE_WRAP:
                snake[-1].y = COLUMNS - 1
            else:
                handle_collision()
        else:
            snake[-1].sub(0, 1)

    if snake[-1] == food:
        snake_len += 1
        if snake_len == ROWS * COLUMNS:
            print("You Win!")
            sys.exit(0)
        new_food()

    for seg in snake[:-1]:
        if seg.get() == snake[-1].get():
            handle_collision()

    if len(snake) > snake_len:
        snake.pop(0)


def draw_snake():
    seg = snake[0]
    n_dir = seg.get_next_dir(snake[1])
    if n_dir == "right":
        screen.blit(pg.transform.flip(tail_img, True, False),
                    pg.Rect(seg.get_box_scale(), box))
    elif n_dir == "down":
        screen.blit(pg.transform.flip(pg.transform.rotate(
            tail_img, 90), True, False), pg.Rect(seg.get_box_scale(), box))
    elif n_dir == "left":
        screen.blit(tail_img, pg.Rect(seg.get_box_scale(), box))
    elif n_dir == "up":
        screen.blit(pg.transform.rotate(tail_img, 270),
                    pg.Rect(seg.get_box_scale(), box))

    for i in range(1, snake_len - 1):
        seg = snake[i]
        n_dir = seg.get_next_dir(snake[i + 1])
        p_dir = snake[i - 1].get_next_dir(seg)

        if n_dir == p_dir:
            if n_dir == "right":
                screen.blit(pg.transform.flip(body_img, True, False),
                            pg.Rect(seg.get_box_scale(), box))
            elif n_dir == "down":
                screen.blit(pg.transform.flip(pg.transform.rotate(
                    body_img, 90), True, False), pg.Rect(seg.get_box_scale(), box))
            elif n_dir == "left":
                screen.blit(body_img, pg.Rect(seg.get_box_scale(), box))
            elif n_dir == "up":
                screen.blit(pg.transform.rotate(body_img, 270),
                            pg.Rect(seg.get_box_scale(), box))
        elif (p_dir == "right" and n_dir == "down") or (p_dir == "up" and n_dir == "left"):
            screen.blit(curveout_img, pg.Rect(seg.get_box_scale(), box))
        elif (p_dir == "left" and n_dir == "up") or (p_dir == "down" and n_dir == "right"):
            screen.blit(curvein_img, pg.Rect(seg.get_box_scale(), box))
        elif (p_dir == "right" and n_dir == "up") or (p_dir == "down" and n_dir == "left"):
            screen.blit(pg.transform.flip(pg.transform.rotate(
                curveover_img, 90), True, False), pg.Rect(seg.get_box_scale(), box))
        elif (p_dir == "left" and n_dir == "down") or (p_dir == "up" and n_dir == "right"):
            screen.blit(curveover_img, pg.Rect(seg.get_box_scale(), box))

    seg = snake[-1].get_box_scale()
    if move_dir == "right":
        screen.blit(pg.transform.flip(
            head_img, True, False), pg.Rect(seg, box))
    elif move_dir == "down":
        screen.blit(pg.transform.flip(pg.transform.rotate(
            head_img, 90), True, False), pg.Rect(seg, box))
    elif move_dir == "left":
        screen.blit(head_img, pg.Rect(seg, box))
    elif move_dir == "up":
        screen.blit(pg.transform.rotate(head_img, 270), pg.Rect(seg, box))


def draw_food():
    screen.blit(food_img, pg.Rect(food.get_box_scale(), box))


screen.fill(BG_COLOR)
new_food()
draw_food()
draw_snake()
pg.display.flip()
clock.tick(FPS)

while 1:
    dir_temp = move_dir
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit(0)
        if event.type == pg.KEYDOWN:
            key = event.key
            if key == pg.K_ESCAPE:
                sys.exit(0)
            if key in (pg.K_UP, pg.K_w) and move_dir != "down":
                dir_temp = "up"
            if key in (pg.K_DOWN, pg.K_s) and move_dir != "up":
                dir_temp = "down"
            if key in (pg.K_LEFT, pg.K_a) and move_dir != "right":
                dir_temp = "left"
            if key in (pg.K_RIGHT, pg.K_d) and move_dir != "left":
                dir_temp = "right"
    move_dir = dir_temp

    screen.fill(BG_COLOR)

    move_snake()
    draw_food()
    draw_snake()

    pg.display.flip()
    clock.tick(FPS)
