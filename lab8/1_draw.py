import pygame as pg
from pygame.draw import *
pg.init()

screen = pg.display.set_mode((300, 200))
pg.display.update()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()