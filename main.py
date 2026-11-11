#Improting libraries/classes
import pygame
from player import Player
from WaveManager import Wavemanager
from hazards import Bullet
import random
from hazards import Sniper_bullet

#window
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snek Survivor")
clock = pygame.time.Clock()
#player spawn
player = Player(400,300)
player.hitbox_rect.center = (400,300)
player.x = float(player.hitbox_rect.x)
player.y = float(player.hitbox_rect.y)
wave_mgr = Wavemanager()
hazards = []
rain_spawn_timer = 0.0 
RAIN_SPAWN_INTERVAL = 0.30
sniper_spawn_timer = 0.0
SNIPER_SPAWN_INTERVAL = 2.0
font = pygame.font.Font(None, 36) 
#MAIN LOOP
running = True
while running: 
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if wave_mgr.state == "DODGE" :
        rain_spawn_timer += dt
        if rain_spawn_timer >= RAIN_SPAWN_INTERVAL:
            rain_spawn_timer = 0.0 
            rx = random.randint(20, WIDTH - 20)
            ry = -10
            vy = random.randint(180, 280)
            hazards.append(Bullet(rx, ry, 0, vy))
        sniper_spawn_timer += dt
        if sniper_spawn_timer >= SNIPER_SPAWN_INTERVAL:
            sniper_spawn_timer = 0.0
            if random.choice([True, False]):
             sx = random.choice([-10, WIDTH + 10])
             sy = random.choice([-10, HEIGHT + 50])
            else:
             sx = random.randint(-10, WIDTH)
             sy = random.randint(-10, HEIGHT)
            hazards.append(Sniper_bullet(sx, sy, player.x, player.y))
    else :klmpm;klm;lm;lm
          hazards.clear()
    for bullet in hazards[:]:
        if bullet.is_offscreen(WIDTH, HEIGHT):
                hazards.remove(bullet)
        bullet.update(dt)
    wave_mgr.update(dt)
    player.update_timer(dt)
    if player.hp <= 0:
                running = False  
    player.move()
    screen.fill((0,0,0))
    player.draw(screen)
    for bullet in hazards:
        bullet.draw(screen)
    #HUD
    state_color = (255, 50, 50) if wave_mgr.state == "DODGE" else (50, 255, 50)
    wave_surf = font.render(f"WAVE: {wave_mgr.current_wave}", True, (255, 255, 255))
    timer_surf = font.render(f"{wave_mgr.state}: {max(0.0, wave_mgr.time_remaining):.1f}s", True, state_color)
    screen.blit(wave_surf, (20,20))
    screen.blit(timer_surf, (20, 50))
    pygame.display.flip()
pygame.quit()