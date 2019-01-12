import pygame
from pygame.locals import *
from PIL import Image
import math
import sys
import numpy as np


BLACK = (0, 0, 0) 
GREEN = (0, 255, 0)


class Bullet():
    def __init__(self, angle=None):
        self.width = 10
        self.height = 10      #총알의 크기 기본값

        if angle is None:
            self.angle = 0
        else:
            self.angle = angle      #총알이 날라갈 각도 받음

        self.setvertex()


    def setvertex(self): #변하는 점 vertex 구하기
        seta = self.angle + 90
        mvx = math.cos(math.radians(seta)) * 150 + 400
        mvy = -math.sin(math.radians(seta)) * 150 + 600

        self.vertex = np.array([mvx, mvy])

        self.point = []
        self.point.append(self.vertex)


    def update(self):       #클릭 각도로 총알을 쏜다
        rad = self.angle
        newPoint = []
        speed = 8
        for pt in self.point:
            x = np.sin(math.radians(rad))
            y = np.cos(math.radians(rad))
            velocity = np.array([x, y])
            velocity *= speed
            pt = np.subtract(pt, velocity)
            newPoint.append(pt)
        self.point = newPoint
        #print(self.point)
        print(self.angle)
        print(self.vertex)



class Cannon():
    def __init__(self):     #포구 크기, 각도 기본값
        self.orig_image = pygame.Surface([20,300]).convert_alpha()
        self.image = self.orig_image
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center = (game.cannon_centerx, game.cannon_centery))
        self.angle = 0


    def render(self):
        game.screen.blit(self.image, self.rect)


    def update(self):       #포구의 각도 조절
        
        mouse = pygame.mouse.get_pos()
        pos = (self.rect.centerx - mouse[0], self.rect.bottom - mouse[1])
        self.angle = math.degrees(math.atan2(*pos))
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center = old_center)
        #print(self.rect)



class Gamemain():
    done = True
    bullets = []

    def __init__(self, width=800, height=600, cannon_centerx=400, cannon_centery=600):
        pygame.init()
        self.width, self.height = width, height
        self.cannon_centerx, self.cannon_centery = cannon_centerx, cannon_centery
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cannon : pygame")

        self.distance = 750
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.game_init()


    def game_init(self):
        self.bullets = []


    def update(self):
        cannon.update()
        for c in self.bullets:
            c.update()


    def loop(self):
        while self.done:
            self.handle_events()
            self.update()
            self.draw()


    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.done = False
                sys.exit()
            elif event.type == KEYDOWN:
                if(event.key == K_ESCAPE):
                    self.done = False
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                self.bullets.append(Bullet(cannon.angle))


    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.circle(self.screen, GREEN, (self.cannon_centerx, self.cannon_centery), 65)
        cannon.render()
        for i, c in enumerate(self.bullets ):
            pygame.draw.rect(self.screen, GREEN, (c.point[0][0], c.point[0][1], bullet.width, bullet.height))
            offset = (self.cannon_centerx - c.point[0][0], self.cannon_centery - c.point[0][1])
            distance = math.sqrt(offset[0]**2 + offset[1]**2)
            if distance > 750:
                self.bullets.pop(i)
        pygame.display.flip()


if __name__ == '__main__' :
    game = Gamemain()
    cannon = Cannon()
    bullet = Bullet()
    game.loop()