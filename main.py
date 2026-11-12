# Improting libraries/classes
import pygame
import random
import math
import sys
from pathlib import Path
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

if getattr(sys, 'frozen', False):
    ASSETS_DIR = Path(sys._MEIPASS) / "assets"
    SAVE_DIR = Path(sys.executable).parent
else:
    ASSETS_DIR = Path(__file__).parent / "assets"
    SAVE_DIR = Path(__file__).parent

def load_sprite(filename, scale=1):
    img = pygame.image.load(ASSETS_DIR / filename).convert_alpha()
    if scale != 1:
        w, h = img.get_size()
        img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
    return img

Snek_img = load_sprite("Snek.png", scale = 3.2)
rain_img = load_sprite("rain.png", scale = 3)
Sickle_img = load_sprite("Sickle.png", scale = 2)
Gameover_img = load_sprite("Gameover.png", scale = 2)
Sniper_img = load_sprite("Sniper.png", scale = 2)
title_img = load_sprite("title.png", scale = 2)
Dna_img = load_sprite("Dna.png", scale = 2)
hp_frames = [load_sprite(f"HP/HP_{i}.png", scale=3) for i in range(1, 21)]

# player spawn
player = Player(400, 300, Snek_img)
player.hitbox_rect.center = (400, 300)
player.x = float(player.hitbox_rect.x)
player.y = float(player.hitbox_rect.y)

# Varable defining 
wave_mgr = Wavemanager()
hazards = []
rain_spawn_timer = 0.0 
RAIN_SPAWN_INTERVAL = 0.30
sniper_spawn_timer = 0.0
SNIPER_SPAWN_INTERVAL = 2.0
sickle_spawn_timer = 0.0
SICKLE_SPAWN_INTERVAL = 0.4
sinewave_spawn_timer = 0.0
SINEWAVE_SPAWN_INTERVAL = 3.0
last_wave = -1
active_hazards = []
font = pygame.font.Font(None, 36) 
game_state = "MENU"
prompt_surf = font.render("PRESS SPACE TO START", True, (255, 255, 255))
prompt_rect = prompt_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
over_surf = font.render("PRESS SPACE TO RESTART", True, (255, 60, 60))
over_rect = over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
hs_file = SAVE_DIR / "highscore.txt"
high_score = int(hs_file.read_text().strip()) if hs_file.exists() and hs_file.read_text().strip() else 1
high_score_surf = font.render(f"HIGHEST WAVE IS {high_score}", True, (255, 255, 255))
high_score_rect = high_score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
title_rect = title_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
gameover_rect = Gameover_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))


# MAIN LOOP
running = True
while running: 
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state in ("MENU", "OVER"):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "PLAYING"

    if game_state == "PLAYING":        
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
                diff_mult = 1.0 + (wave - 1) * 0.05
            elif 11 <= wave <= 20:
                diff_mult = 1.0 + (wave - 1) * 0.1
            else:
                diff_mult = 1.0 + (wave - 1) * 0.15

            if "rain" in active_hazards:
                rain_spawn_timer += dt
                if rain_spawn_timer >= (RAIN_SPAWN_INTERVAL / diff_mult):
                    rain_spawn_timer = 0.0 
                    rx = random.randint(20, WIDTH - 20)
                    ry = -10
                    vy = random.randint(180, 280) * diff_mult
                    hazards.append(Bullet(rx, ry, 0, vy, rain_img))

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
                    hazards.append(Sniper_bullet(sx, sy, player.x, player.y, Sniper_img))

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
                    hazards.append(Sickle(cx, cy, vx, vy, Sickle_img))

            if "sinewave" in active_hazards:
                sinewave_spawn_timer += dt
                if sinewave_spawn_timer >= (SINEWAVE_SPAWN_INTERVAL/ diff_mult):
                    sinewave_spawn_timer = 0.0
                    speed = 300 * diff_mult
                    sinex = random.choice([100, 200, 300, 400, 500, 600, 700])
                    spacing = 20
                    for i in range(100):
                        siney = -10 - (i * spacing)
                        hazards.append(Sine_wave(sinex, siney, speed, Dna_img, amplitude=60, frequency=0.015))
                        hazards.append(Sine_wave(sinex, siney, speed, Dna_img, amplitude=60, frequency=0.015, phase=math.pi))
        
            if wave_mgr.current_wave > high_score:
                                    high_score = wave_mgr.current_wave
                                    hs_file.write_text(str(high_score))
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
            game_state = "OVER"
            player.hp = 20
            player.hitbox_rect.center = (400, 300)
            hazards.clear()
            last_wave = -1
            wave_mgr = Wavemanager()
        player.move()
        screen.fill((0, 0, 0)) 
        player.draw(screen)
        for bullet in hazards:
            bullet.draw(screen)
        
    # HUD

     
    if game_state == "MENU":
        screen.fill((0, 0, 0)) 
        screen.blit(title_img, title_rect)
        screen.blit(prompt_surf, prompt_rect)
        screen.blit(high_score_surf, high_score_rect)
    if game_state == "OVER":
        screen.fill((0, 0, 0)) 
        screen.blit(Gameover_img, gameover_rect)
        screen.blit(over_surf, over_rect)
        screen.blit(high_score_surf, high_score_rect)
    state_color = (255, 50, 50) if wave_mgr.state == "DODGE" else (50, 255, 50)
    if game_state == "PLAYING":
        wave_surf = font.render(f"WAVE: {wave_mgr.current_wave}", True, (255, 255, 255))
        timer_surf = font.render(f"{wave_mgr.state}: {max(0.0, wave_mgr.time_remaining):.0f}s", True, state_color)
        screen.blit(wave_surf, (20, 20))
        screen.blit(timer_surf, (20, 50))
        hp_index = max(0, min(19, player.hp - 1))
        screen.blit(hp_frames[hp_index], (20, 85))
    pygame.display.flip()
pygame.quit()