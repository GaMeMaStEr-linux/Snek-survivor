import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox_width = 28
        self.hitbox_height = 28
        self.speed = 3
        self.max_hp = 100
        self.hp = 100
        self.i_timer = 0.0
        self.hitbox_rect = pygame.Rect(x, y, self.hitbox_width, self.hitbox_height)

    def take_damage(self, amount):
        if self.i_timer <= 0:
            self.hp -= amount
            self.i_timer = 0.5
        if self.hp < 0 :
            self.hp = 0

    def update_timer(self, dt):
        if self.i_timer > 0:
            self.i_timer -= dt 

    def draw(self, surface):
        if self.i_timer < 0 :
            pygame.draw.rect(surface, (250, 0, 0), self.hitbox_rect) 
        else:
            pygame.draw.rect(surface, (250,0,0), self.hitbox_rect)
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
        if self.x < 0:
            self.x = 0
        if self.x > 800 - self.hitbox_width:
            self.x = 800 - self.hitbox_width
        if self.y < 0:
            self.y = 0
        if self.y > 600 - self.hitbox_height:
            self.y = 600 - self.hitbox_height

        self.hitbox_rect.x = self.x
        self.hitbox_rect.y = self.y
