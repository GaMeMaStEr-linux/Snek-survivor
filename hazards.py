import pygame
import math

class Bullet:
    def __init__(self, x, y, vx, vy, radius=8, color=(255, 255, 255)):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy 
        self.radius = radius 
        self.color = color
        self.hitbox_rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.hitbox_rect.x = int(self.x - self.radius)
        self.hitbox_rect.y = int(self.y - self.radius)

    def is_offscreen(self, width, height):
        return (self.x < -50 or self.x > width + 50 or
                self.y < -50 or self.y > height + 50)
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Sniper_bullet:
    def __init__(self, x, y, px, py, lenght = 30, thickness = 7, speed = 350, color = (230, 222, 9)):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.length = lenght
        self.thickness = thickness
        self.hitbox_rect = pygame.Rect(int(self.x), int(self.y), self.length, self.thickness)
        dx = px - self.x 
        dy = py - self.y
        dist = math.hypot(dx, dy)
        self.speed = speed
        if dist != 0:
            self.vx = (dx / dist) * speed 
            self.vy = (dy / dist) * speed
        else:
            self.vx = 0
            self.vy = speed
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt 

        self.hitbox_rect.x = int(self.x)
        self.hitbox_rect.y = int(self.y)
    def is_offscreen(self, w, h):
        return (self.x < -50 or self.x > w + 50
                or self.y < -50 or self.y > h + 50 )
    def draw(self, surface):
        dir_x = self.vx / self.speed 
        dir_y = self.vy / self.speed

        end_x = self.x + (dir_x * self.length)
        end_y = self.y + (dir_y * self.length)
        pygame.draw.line(surface, self.color, (int(self.x), int(self.y)), (int(end_x), int(end_y)), self.thickness )

class Sickle:
    def __init__ (self, x, y, vx, vy, width = 30, height = 30, color = (200, 25, 227)):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy 
        self.color = color
        self.hitbox_rect = pygame.Rect(int(self.x), int(self.y), width, height)
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.hitbox_rect.x = int(self.x)
        self.hitbox_rect.y = int(self.y)
    def is_offscreen(self, w, h):
        return (self.x < -50 or self.x > w + 50
                or self.y < -50 or self.y > h + 50 )
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.hitbox_rect)