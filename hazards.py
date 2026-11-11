import pygame
import math

class Bullet:
    def __init__(self, x, y, vx, vy, radius=8, damage = 1, color=(255, 255, 255)):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy 
        self.radius = radius 
        self.color = color
        self.damage = damage
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
    def __init__(self, x, y, px, py, lenght = 30, thickness = 7, damage = 3, speed = 350, color = (230, 222, 9)):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.length = lenght
        self.thickness = thickness
        self.damage = damage
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
    def __init__ (self, x, y, vx, vy, damage = 5, angle = 0.0 , width = 30, height = 30, color = (200, 25, 227)):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy 
        self.color = color
        self.angle = angle
        self.damage = damage
        self.rot_speed = 200.0
        self.hitbox_rect = pygame.Rect(int(self.x), int(self.y), width, height)
        self.original_image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.original_image.fill(self.color)
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.hitbox_rect.x = int(self.x)
        self.hitbox_rect.y = int(self.y)
        self.angle = (self.angle + self.rot_speed * dt) % 360
    def is_offscreen(self, w, h):
        return (self.x < -50 or self.x > w + 50
                or self.y < -50 or self.y > h + 50 )
    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.hitbox_rect.center)
        surface.blit(rotated_image, rotated_rect)

class Sine_wave:
    def __init__(self, x, y, speed, damage = 1, amplitude = 60, frequency = 0.015, phase = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.damage = damage
        self.time_active = 0.0
        self.color = (252, 111, 3)
        self.hitbox_rect = pygame.Rect(int(self.x), int(self.y), 12, 12)
    def update(self, dt):
        self.time_active += dt 
        self.y += self.speed * dt
        wave_offset = math.sin((self.y * self.frequency) + self.phase) * self.amplitude 
        calc_x = self.x + wave_offset 
        self.hitbox_rect.x = int(calc_x)
        self.hitbox_rect.y = int(self.y)
    def is_offscreen(self, w, h):
        return self.y > h + 50
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.hitbox_rect.center, 6)