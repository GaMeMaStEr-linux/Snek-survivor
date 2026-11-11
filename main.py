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
last_wave = -1
active_hazards = []
font = pygame.font.Font(None, 36) 

# MAIN LOOP
running = True
while running: 
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if wave_mgr.state == "DODGE":
        wave = wave_mgr.current_wave

        
        if wave != last_wave:
            last_wave = wave
            wave_types = ["rain", "sniper", "sickle", "sinewave"]
            if wave == 1:
                active_hazards = ["rain"]
            elif wave == 2:
                active_hazards = ["sniper"]
            elif wave == 3:
                active_hazards = ["sickle"]
            elif wave == 4:
                active_hazards = ["sinewave"]
            elif 5 <= wave <= 9:
                active_hazards = random.sample(wave_types, 2)
            elif 10 <= wave <= 14:
                active_hazards = random.sample(wave_types, 3)
            else:
                active_hazards = wave_types
        if 1 <= wave <= 10:
            diff_mult = 1.0 + (wave - 1) * 0.10
        elif 11 <= wave <= 20:
            diff_mult = 1.0 + (wave - 1) * 0.20
        else:
            diff_mult = 1.0 + (wave - 1) * 0.30

        if "rain" in active_hazards:
            rain_spawn_timer += dt
            if rain_spawn_timer >= (RAIN_SPAWN_INTERVAL / diff_mult):
                rain_spawn_timer = 0.0 
                rx = random.randint(20, WIDTH - 20)
                ry = -10
                vy = random.randint(180, 280) * diff_mult
                hazards.append(Bullet(rx, ry, 0, vy))

        if "sniper" in active_hazards:
            sniper_spawn_timer += dt
            if sniper_spawn_timer >= (SNIPER_SPAWN_INTERVAL / diff_mult):
                sniper_spawn_timer = 0.0
                if random.choice([True, False]):
                    sx = random.choice([-10, WIDTH + 10])
                    sy = random.choice([-10, HEIGHT + 10])
                else:
                    sx = random.randint(-10, WIDTH)
                    sy = random.randint(-10, HEIGHT)
                hazards.append(Sniper_bullet(sx, sy, player.x, player.y))

        if "sickle" in active_hazards:
            sickle_spawn_timer += dt
            if sickle_spawn_timer >= (SICKLE_SPAWN_INTERVAL / diff_mult):
                sickle_spawn_timer = 0.0
                speed = random.randint(100, 180) * diff_mult
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

        if "sinewave" in active_hazards:
            sinewave_spawn_timer += dt
            if sinewave_spawn_timer >= (SINEWAVE_SPAWN_INTERVAL/ diff_mult):
                sinewave_spawn_timer = 0.0
                speed = 300 * diff_mult
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
    timer_surf = font.render(f"{wave_mgr.state}: {max(0.0, wave_mgr.time_remaining):.0f}s", True, state_color)
    screen.blit(wave_surf, (20, 20))
    screen.blit(timer_surf, (20, 50))
    pygame.display.flip()
pygame.quit()