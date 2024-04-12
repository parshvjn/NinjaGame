from random import *
import pygame
from math import atan2, cos, sin, sqrt
class Particle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.maxlife = randint(13 + 22, 27 + 44)
        self.life = self.maxlife
        self.dir = choice((-2, -1, 1, 2))
        self.sin = randint(-10, 10)/7
        self.sinr = randint(5, 10)
        self.r = randint(0,2)

        self.ox = randint(-1, 1)
        self.oy = randint(-1, 1)
        

class FireManager:
    def __init__(self, playerPosX, playerPosY, window, up = True):
        self.ox, self.oy = playerPosX, playerPosY
        self.j = 0
        self.dist = 0
        self.pX, self.pY = playerPosX, playerPosY
        self.particles = []
        self.dead = []
        self.res = 4
        self.mp = False
        self.palette = ((255, 255, 0),
            (255, 173, 51),
            (247, 117, 33),
            (191, 74, 46),
            (115, 61, 56),
            (61, 38, 48))[::-1]
        self.window = window
        self.up = up
        self.direction = True # if true then right if false then left

    def attack(self, direction = None):
        self.mp = True
        a = atan2(self.pY - self.oy, self.pX-self.ox)        
        for d in range(0, int(self.dist), 10):
            self._x = self.pX+cos(a)*d
            self._y = self.pY+sin(a)*d
            if self.mp:
                for _ in range(3): self.particles.append(Particle(self._x//self.res, self._y//self.res))
        else:
            if self.mp:
                for _ in range(3): self.particles.append(Particle(self.pX//self.res, self.pY//self.res))
        

        self.mp = False
        if self.direction != direction:
            self.direction = direction
            self.particles.clear()




    def update(self, pX, pY, wind = 0):
        self.j+=1
        if self.j>360: self.j = 0
        self.pX, self.pY = pX, pY
        self.dist = sqrt((pX-self.ox)**2+(pY-self.oy)**2)
        for p in self.particles:
            p.life -= 1
            if p.life == 0: self.dead.append(p); continue

            i = int((p.life/p.maxlife)*6)

            if self.up:
                p.y -= 2
                p.x += ((p.sin * sin(self.j/(p.sinr)))/2)*1 + wind
            else:
                if self.direction:
                    p.x += 2 # the 2 is the rise
                    p.y += ((p.sin * sin(self.j/(p.sinr)))/2)*1 + wind # the 1 is the spread, and 0 is the wind
                else:
                    p.x -= 2 # the 2 is the rise
                    p.y += ((p.sin * sin(self.j/(p.sinr)))/2)*1 + wind # the 1 is the spread, and 0 is the wind

            if not randint(0, 5): p.r += 0.88

            x, y = p.x, p.y

            x += p.ox*(5-i)
            y += p.oy*(5-i)

            alpha = 255
            if p.life < p.maxlife/4:
                alpha = int((p.life/p.maxlife)*255)

            pygame.draw.circle(self.window, self.palette[i] + (alpha,), (x, y), p.r, 0)

            if i == 0:
                pygame.draw.circle(self.window, (0, 0, 0, 0), (x+randint(-1, 1), y-4), p.r*(((p.maxlife-p.life)/p.maxlife)/0.88), 0)

            else:
                pygame.draw.circle(self.window, self.palette[i-1] + (alpha,), (x+randint(-1, 1), y-3), p.r/1.5, 0)

        for p in self.dead:
            self.particles.remove(p)
        self.dead.clear()
        self.ox, self.oy = self.pX, self.pY
            

