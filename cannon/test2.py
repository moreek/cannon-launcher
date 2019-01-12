import pygame as pg
from pygame.locals import *
import sys
import math
import numpy as np
import random

RED = (255,0,0)
ElLLIPSE_WIDTH = 200
EILLIPSE_HEIGHT = 100


class Bullet :
    def __init__(self, start = None , angle = None) :
        print("Bullet create")
        self.width = 10
        self.height = 10
        # self.color = list(pg.color.THECOLORS.values())[random.choice(range(len(pg.color.THECOLORS)))]
        self.color = RED

        if start is None :
            self.start = np.array([300,200])
        else :
            self.start = start
        self.angle = angle

        self.point = []
        self.point.append(start)


    def update(self) :
        rad = self.angle
        newPoints = []
        speed = 3
        for pt in self.point :
            y = np.cos(math.radians(rad))
            x = np.sin(math.radians(rad))
            velocity = np.array([x,y])
            velocity *= speed
            pt = np.subtract(pt, velocity)
            newPoints.append(pt)
        self.point = newPoints


class Gun :
    def __init__(self) :
        print("Gun create")
        self.orig_image = pg.Surface([20,300]).convert_alpha()
        self.image = self.orig_image
        self.image.fill(RED)
        self.rect = self.image.get_rect(center = (game.screen_rect.centerx,game.screen_rect.bottom))
        self.angle = 0


    def render(self):
        game.screen.blit(self.image, self.rect)


    def update(self):
        mouse = pg.mouse.get_pos()
        offset = (self.rect.centerx - mouse[0], self.rect.bottom - mouse[1])
        self.angle = math.degrees(math.atan2(*offset))
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center = old_center)



class GameMain :
    running = True
    bullet = []
    gameImage = []
    def __init__(self, width = 600, height = 500 , bgcolor = None):
        pg.init()
        self.width, self.height = width , height
        self.screen = pg.display.set_mode((self.width,self.height))
        self.screen_rect = self.screen.get_rect()

        self.bgcolor = (50,50,50)

        self.clock = pg.time.Clock()
        self.limite_fps_max = 60
        self.game_init()


    def game_init(self):
        self.gameImage = []


    def loop(self) :
        while self.running :
            self.handle_event()
            self.update()
            self.draw()


    def update(self):
        gun.update()
        for c in self.bullet :
            c.update()


    def handle_event(self) :
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                self.running = False
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_SPACE :                    
                    self.bullet.append(Bullet((self.screen_rect.centerx,self.screen_rect.bottom), gun.angle))                    
            elif event.type == MOUSEBUTTONUP and event.button == 1 :
                pos = pg.mouse.get_pos()


    def draw(self) :
        self.screen.fill(self.bgcolor)
        pg.draw.ellipse(self.screen, RED, (self.screen_rect.centerx - 100 ,self.screen_rect.bottom - 50, ElLLIPSE_WIDTH, EILLIPSE_HEIGHT))
        gun.render()
        for  idx , c in enumerate(self.bullet) :
            r = Rect(c.point[0][0], c.point[0][1], c.width, c.height)
            offset = (self.screen_rect.centerx - c.point[0][0], self.screen_rect.bottom - c.point[0][1])
            distance = math.sqrt((offset[0] * offset[0]) + (offset[1] * offset[1]))
            if distance > 600 :
                self.bullet.pop(idx)
            self.screen.fill(c.color, r)
        pg.display.flip()



if __name__ == '__main__' :
    game = GameMain()
    gun = Gun()
    game.loop()