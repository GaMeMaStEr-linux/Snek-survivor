# Improting libraries/classes
import pygame
import random
import math
from WaveManager import Wavemanager
from player import Player
from hazards import Bullet
from hazards import Sniper_bullet
from hazards import Sickle
from hazards import Sine_wave

# window
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snek Survivor")
clock = pygame.time.Clock()

# player spawn
player = Player(400, 300)
player.hitbox_rect.center = (400, 300)
player.x = float(player.hitbox_rect.x)
player.y = float(player.hitbox_rect.y)
wave_mgr = Wavemanager()
hazards = []
rain_spawn_timer = 0.0 
RAIN_SPAWN_INTERVAL = 0.30
sniper_spawn_timer = 0.0
SNIPER_SPAWN_INTERVAL = 2.0
sickle_spawn_timer = 0.0
SICKLE_SPAWN_INTERVAL = 0.30
sinewave_spawn_timer = 0.0
SINEWAVE_SPAWN_INTERVAL = 5.0
font = pygame.font.Font(None, 36) 

# MAIN LOOP
running = True
while running: 
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if wave_mgr.state == "DODGE":
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
                sy = random.choice([-10, HEIGHT + 10])
            else:
                sx = random.randint(-10, WIDTH)
                sy = random.randint(-10, HEIGHT)
            hazards.append(Sniper_bullet(sx, sy, player.x, player.y))

        sickle_spawn_timer += dt
        if sickle_spawn_timer >= SICKLE_SPAWN_INTERVAL:
            sickle_spawn_timer = 0.0
            speed = random.randint(100, 180)
            #cse is sickle spawn edge
            cse  = random.randint(1, 4)
            if cse == 1 :
                cx = WIDTH + 30
                cy = random.randint(10, HEIGHT - 10)
                vx = -speed
                vy = 0
            elif cse == 2:
                cx = random.randint(10, WIDTH - 10)
                cy = HEIGHT + 30
                vx = 0
                vy = -speed
            elif cse == 3:
                cx = -30 
                cy = random.randint(10, HEIGHT - 10)
                vx = speed
                vy = 0
            elif cse == 4:
                cx = random.randint(10, WIDTH - 10)
                cy = -30 
                vx = 0
                vy = speed
            hazards.append(Sickle(cx, cy, vx, vy))
        sinewave_spawn_timer += dt
        if sinewave_spawn_timer >= SINEWAVE_SPAWN_INTERVAL:
                sinewave_spawn_timer = 0.0
                speed = 300
                sinex = random.choice([100, 200, 300, 400, 500, 600, 700])
                spacing = 20
                for i in range(100):
                    siney = -10 - (i * spacing)
                    hazards.append(Sine_wave(sinex, siney, speed = 300, amplitude = 60 , frequency = 0.015))
                    hazards.append(Sine_wave(sinex, siney, speed = speed, amplitude = 60, frequency = 0.015, phase=math.pi))
                    
            
    else:
        hazards.clear()
    for hazard in hazards[:]:
        if hazard.is_offscreen(WIDTH, HEIGHT):
            hazards.remove(hazard)
        else:
            hazard.update(dt)
        if player.hitbox_rect.colliderect(hazard.hitbox_rect):
            player.take_damage(hazard.damage)
            hazards.remove(hazard)

    wave_mgr.update(dt)
    player.update_timer(dt)
    if player.hp <= 0:
        running = False  
    player.move()
    screen.fill((0, 0, 0))
    player.draw(screen)
    for bullet in hazards:
        bullet.draw(screen)
        
    # HUD
    state_color = (255, 50, 50) if wave_mgr.state == "DODGE" else (50, 255, 50)
    wave_surf = font.render(f"WAVE: {wave_mgr.current_wave}", True, (255, 255, 255))
    timer_surf = font.render(f"{wave_mgr.state}: {max(0.0, wave_mgr.time_remaining):.1f}s", True, state_color)
    screen.blit(wave_surf, (20, 20))
    screen.blit(timer_surf, (20, 50))
    pygame.display.flip()
pygame.quit()