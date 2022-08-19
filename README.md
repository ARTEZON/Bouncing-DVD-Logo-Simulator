# Ultimate Bouncing DVD Logo Simulator

**Features:**
- Customizable logo speed and size
- Windowed/fullscreen mode
- Stats overlay with corner hit count
- Ability to spawn several logos with collision
- Random colors & color change at bounce (if enabled)

\
**Screenshots:**<br>
<p align="center">
<img src="https://user-images.githubusercontent.com/61311568/185705638-31edf83b-d588-421e-ae1c-04a734635952.png" width="30%" alt="Screenshot 1">
<img src="https://user-images.githubusercontent.com/61311568/185705706-64113dfd-2405-4d09-bcd7-50fe15b11332.png" width="30%" alt="Screenshot 2">
<img src="https://user-images.githubusercontent.com/61311568/185705751-bd6ebed0-437f-4705-a1ab-e40b3edf6c7f.png" width="30%" alt="Screenshot 3">
<img src="https://user-images.githubusercontent.com/61311568/185705730-c6963cb2-ad02-446d-8f6c-c5cd57e4c3eb.png" width="30%" alt="Screenshot 4">
<img src="https://user-images.githubusercontent.com/61311568/185705744-084b7c39-07eb-4db3-975d-33a4e06d54ea.png" width="30%" alt="Screenshot 5">
</p>

\
**Requirements:**
- Python 3.8+
- Pygame library (install: `pip install pygame`)

\
**How to use:**
1. Make sure you have ***Pygame*** installed
2. Download source code
3. Launch ***main.pyw*** file
4. Read help menu
5. Have fun!

\
**Customization:**
- Basic changes can be done in-game using hotkeys:

```
SPACE                     –  Open/close help menu
C or ENTER                –  Spawn new DVD logo
X or DEL                  –  Remove last DVD logo
ARROW RIGHT or PLUS SIGN  –  Increase logos size
ARROW LEFT or MINUS SIGN  –  Decrease logos size
ARROW UP                  –  Increase movement speed
ARROW DOWN                –  Decrease movement speed
F or F11                  –  Toggle fullscreen
S or TAB                  –  Show/hide stats
R                         –  Reset corner count
D                         –  Draw rectangles
ESC                       –  Exit the program
```
- If you want to change defaults or tweak more settings, edit source file. Here are all the available settings:
```
SHOW_HELP_ON_START = True
SHOW_STATS_ON_START = False
ENABLE_CORNER_HIT_MESSAGE = True
START_FULLSCREEN = False
WIDTH, HEIGHT = 900, 500 # window size

LOGO_IMAGE_FILE = "logo.png"
LOGO_W, LOGO_H = 200, 0 # logo size in pixels, set to (0, 0) to preserve original image resolution or to (x, 0) or (0, x) to maintain aspect ratio
LOGO_SCALE_FACTOR = 1 # default image size multiplier

RANDOM_SPAWN_COORD = True
START_X, START_Y = 100, 50 # only if random spawn is set to false

DEFAULT_SPEED = 3

SPAWN_COLORED = True
CHANGE_COLOR_AFTER_EDGE_BOUNCING = False
CHANGE_COLOR_AFTER_EACH_OTHER_BOUNCING = False

CORNER_TOLERANCE = 5 # in pixels

MAX_FPS = 0 # 0 means unlimited
TARGET_FPS = 60 # affects speed, do not change (better modify DEFAULT_SPEED setting above)
FPS_STATS_UPDATE_INTERVAL = 0.5
```

\
**Troubleshooting:**
- If the window doesn't show up, rename ***main.pyw*** to ***main.py*** and check info in console
- The project was made using Pygame version ***2.1.2***. If you have an older version, you may need to upgrade.
