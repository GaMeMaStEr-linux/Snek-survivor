# Snek-survivors
A fast pased wave-based bullet-hell game built in python with pygame, Dodge escalating patterns of projectiles and push the highscore to the max
HEAVILY INSPIRED FROM UNDERTALE AND VAMPIRE SURVIVORS
## LORE
you are Snek, the hero Python who has to save the survivors Ruby to seal the evil Dracula in his coffin
## GAMEPLAY & HAZARDS 
**Wave System:** Alternates between Dodge phases and a small rest for a breath

**The Hazards:**
there are 4 types of hazards in this game
- **Rain:-** acidic rain drops falling from above  (Does 1 damage)
- **Sniper:-** a bullet aimed at the player current position (Does 2 damage)
- **Sickle:-** a rotating death Sickle that does tons of damage (Does 3 damage)
- **SineWave:-** a lot of small circular bullets shaping a DNA like wall (Does 1 damage for each bullet)
## CONTROLS 
**Arrow Keys / WASD:-** Move

**Space Bar:-** start / restart the game
## INSTALL INSTRUCTIONS
### Option 1: Download the Executable (Recommended — No Python Required)
Grab the latest release from the [**Releases**](https://github.com/GaMeMaStEr-linux/Snek-survivor/releases) page:

#### Windows
1. Download **`SnekSurvivor.exe`**.
2. Double-click **`SnekSurvivor.exe`** to launch the game.
   > *Note: Because the executable is not code-signed, Windows SmartScreen may show a "Windows protected your PC" pop-up on the first launch. Click **More info** → **Run anyway** to start.*

#### Linux
1. Download **`SnekSurvivors_linux`**.
2. Open a terminal in your Downloads folder, make the file executable, and run it:
   ```bash
   chmod +x SnekSurvivors_linux
   ./SnekSurvivors_linux
   ```


### Option 2: Run or Build from Source
If you want to modify the code or run it directly with Python, you will need **Python 3.10+** and **`pygame-ce`** installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GaMeMaStEr-linux/Snek-survivor.git
   cd Snek-survivor
   ```

2. **Install dependencies:**
   ```bash
   pip install pygame-ce
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```
