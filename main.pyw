import pygame, sys, time, random


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


pygame.init()
clock = pygame.time.Clock()
screen_w, screen_h = windowed_w, windowed_h = WIDTH, HEIGHT
fullscreen = START_FULLSCREEN
screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
pygame.display.set_caption("DVD")

image = pygame.image.load(LOGO_IMAGE_FILE).convert_alpha()

logos = []
logos_count = 0
corner_hits = 0


class Logo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.pos = pygame.math.Vector2(START_X, START_Y)
        self.w = round(LOGO_W * LOGO_SCALE_FACTOR)
        self.h = round(LOGO_H * LOGO_SCALE_FACTOR)
        if RANDOM_SPAWN_COORD:
            try:               self.pos.x = random.randint(0, screen_w - self.w)
            except ValueError: self.pos.x = random.randint(0, screen_w)
            try:               self.pos.y = random.randint(0, screen_h - self.h)
            except ValueError: self.pos.y = random.randint(0, screen_h)
        self.color = None
        self.size(LOGO_W, LOGO_H, LOGO_SCALE_FACTOR)
        self.speed_x = DEFAULT_SPEED
        self.speed_y = DEFAULT_SPEED
        self.velocity = pygame.math.Vector2(self.speed_x, self.speed_y)
        
    def size(self, w, h, scale):
        scale **= 0.5
        if windowed_w > 0 and h > 0:
            new_w = round(w * scale)
            new_h = round(h * scale)
        elif w == 0 and h == 0:
            new_w = round(image.get_width() * scale)
            new_h = round(image.get_height() * scale)
        elif w != 0:
            new_w = round(w * scale)
            new_h = round(w * (image.get_height() / image.get_width()) * scale)
        else:
            new_h = round(h * scale)
            new_w = round(h * (image.get_width() / image.get_height()) * scale)
        x_offset = round((self.w - new_w) / 2)
        y_offset = round((self.h - new_h) / 2)
        self.w, self.h = new_w, new_h
        self.pos.x += x_offset
        self.pos.y += y_offset
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
        self.image = pygame.transform.smoothscale(image, self.rect.size)
        if self.color: fill_logo(self.image, self.color)

    def change_speed(self, x, y):
        x_sign = -1 if self.velocity.x < 0 else 1
        y_sign = -1 if self.velocity.y < 0 else 1
        self.speed_x = x * x_sign
        self.speed_y = y * y_sign
        self.velocity = pygame.math.Vector2(self.speed_x, self.speed_y)
    
    def set_color(self, color):
        self.color = color
        fill_logo(self.image, self.color)


class CornerHitMessage():
    show_remaining = 0

    def show():
        text = 'CORNER!'
        font = pygame.font.Font(pygame.font.get_default_font(), 60)
        color = (255, 255, 255)
        text_width = font.size(text)[0]
        label = font.render(text, True, color)
        screen.blit(label, ((screen_w - text_width) // 2, 100))


class OnScreenText():
    def  __init__(self):
        self.hud_size = 20
        self.hud_font = pygame.font.Font(pygame.font.get_default_font(), self.hud_size)
        self.hud_color = (255, 255, 255)
        self.hud_lines = [''] * 5

        self.update_menu_size()
        self.help_color = (255, 255, 255)
        self.help_lines = [
            'HELP MENU',
            '',
            'C or ENTER  –  Spawn new DVD logo',
            'X or DEL  –  Remove last DVD logo',
            'ARROW RIGHT or PLUS SIGN  –  Increase logos size',
            'ARROW LEFT or MINUS SIGN  –  Decrease logos size',
            'ARROW UP  –  Increase movement speed',
            'ARROW DOWN  –  Decrease movement speed',
            'F or F11  –  Toggle fullscreen',
            'S or TAB  –  Show/hide stats',
            'R  –  Reset corner count'
            'D  –  Draw rectangles',
            'ESC  –  Exit the program',
            '',
            'SPACE  –  Open/close this menu'
        ]

    def update_menu_size(self):
        self.help_bg = pygame.Surface((screen_w, screen_h))
        self.help_bg.set_alpha(200)
        self.help_bg.fill((0, 0, 0))
        self.help_size = screen_h // 25
        self.help_font = pygame.font.Font(pygame.font.get_default_font(), self.help_size)

    def show_HUD(self, fps):
        self.hud_lines[0] = f'FPS: {fps}'
        self.hud_lines[1] = f'Corner hits: {corner_hits}'
        self.hud_lines[2] = f'Logos count: {logos_count}'
        self.hud_lines[3] = f'Scale: {float(LOGO_SCALE_FACTOR)}'
        self.hud_lines[4] = f'Speed: {DEFAULT_SPEED}'
        for line in enumerate(self.hud_lines):
            text = self.hud_font.render(line[1], True, self.hud_color)
            screen.blit(text, (5, 5 + line[0] * (self.hud_size + 5)))

    def show_help(self):
        screen.blit(self.help_bg, (0, 0))
        for line in enumerate(self.help_lines):
            line_width = self.help_font.size(line[1])[0]
            text = self.help_font.render(line[1], True, self.help_color)
            screen.blit(text, ((screen_w - line_width) // 2, (screen_h - len(self.help_lines) * (self.help_size + 5)) // 2 + line[0] * (self.help_size + 5)))


def spawn_logo():
    global logos, logos_count
    logos.append(Logo())
    logos_count += 1
    if SPAWN_COLORED:
        logos[-1].set_color((random.randint(50, 250), random.randint(50, 250), random.randint(50, 250)))

def kill_logo():
    global logos, logos_count
    if logos_count > 0:
        logos.pop()
        logos_count -= 1

def check_corner(logo):
    global corner_hits
    if logo.pos.y < CORNER_TOLERANCE or logo.pos.y + logo.h > screen_h - CORNER_TOLERANCE:
        if ENABLE_CORNER_HIT_MESSAGE:
            CornerHitMessage.show_remaining = 1
        corner_hits += 1

def edge_collision(logo):
    if logo.pos.x < 0 or logo.pos.x + logo.w > screen_w:
        logo.velocity.x *= -1
        if logo.pos.x < 0:
            logo.pos.x = 0
        if logo.pos.x + logo.w > screen_w:
            logo.pos.x = screen_w - logo.w
        if CHANGE_COLOR_AFTER_EDGE_BOUNCING:
            logo.set_color((random.randint(50, 250), random.randint(50, 250), random.randint(50, 250)))
        check_corner(logo)
    
    if logo.pos.y < 0 or logo.pos.y + logo.h > screen_h:
        logo.velocity.y *= -1
        if logo.pos.y < 0:
            logo.pos.y = 0
        if logo.pos.y + logo.h > screen_h:
            logo.pos.y = screen_h - logo.h
        if CHANGE_COLOR_AFTER_EDGE_BOUNCING:
            logo.set_color((random.randint(50, 250), random.randint(50, 250), random.randint(50, 250)))

def object_collision(tolerance_x, tolerance_y):
    for i in range(logos_count):
        for j in range(i + 1, logos_count):
            first, first_rect = logos[i], logos[i].rect
            second, second_rect = logos[j], logos[j].rect
            if first_rect.colliderect(second_rect):
                if first.pos.x > second.pos.x:
                    if first.pos.x + first.w < screen_w:
                        first.pos.x += 1
                    if second.pos.x > 0:
                        second.pos.x -= 1
                else:
                    if second.pos.x + second.w < screen_w:
                        second.pos.x += 1
                    if first.pos.x > 0:
                        first.pos.x -= 1
                if first.pos.y > second.pos.y:
                    if first.pos.y + first.h < screen_h:
                        first.pos.y += 1
                    if second.pos.y > 0:
                        second.pos.y -= 1
                else:
                    if second.pos.y + second.h < screen_h:
                        second.pos.y += 1
                    if first.pos.y > 0:
                        first.pos.y -= 1
                first.rect.x = first.pos.x
                first.rect.y = first.pos.y
                second.rect.x = second.pos.x
                second.rect.y = second.pos.y

                if abs(second_rect.top - first_rect.bottom) < (int(tolerance_y + 0.5) + 1) * 2:
                    if first.velocity.y > 0: first.velocity.y *= -1
                    if second.velocity.y < 0: second.velocity.y *= -1
                    first.pos.y -= abs(second_rect.top - first_rect.bottom) / 2
                    second.pos.y += abs(second_rect.top - first_rect.bottom) / 2
                if abs(second_rect.bottom - first_rect.top) < (int(tolerance_y + 0.5) + 1) * 2:
                    if first.velocity.y < 0: first.velocity.y *= -1
                    if second.velocity.y > 0: second.velocity.y *= -1
                    first.pos.y += abs(second_rect.bottom - first_rect.top) / 2
                    second.pos.y -= abs(second_rect.bottom - first_rect.top) / 2
                if abs(second_rect.left - first_rect.right) < (int(tolerance_x + 0.5) + 1) * 2:
                    if first.velocity.x > 0: first.velocity.x *= -1
                    if second.velocity.x < 0: second.velocity.x *= -1
                    first.pos.x -= abs(second_rect.left - first_rect.right) / 2
                    second.pos.x += abs(second_rect.left - first_rect.right) / 2
                if abs(second_rect.right - first_rect.left) < (int(tolerance_x + 0.5) + 1) * 2:
                    if first.velocity.x < 0: first.velocity.x *= -1
                    if second.velocity.x > 0: second.velocity.x *= -1
                    first.pos.x += abs(second_rect.right - first_rect.left) / 2
                    second.pos.x -= abs(second_rect.right - first_rect.left) / 2
                
                if CHANGE_COLOR_AFTER_EACH_OTHER_BOUNCING:
                    first.set_color((random.randint(50, 250), random.randint(50, 250), random.randint(50, 250)))
                    second.set_color((random.randint(50, 250), random.randint(50, 250), random.randint(50, 250)))

def fill_logo(surface, color=None, mask_color=None):
    w, h = surface.get_size()
    if color:
        new_r, new_g, new_b = color
        for x in range(w):
            for y in range(h):
                r, g, b, a = surface.get_at((x, y))
                if not mask_color or (r, g, b) == mask_color:
                    surface.set_at((x, y), pygame.Color(new_r, new_g, new_b, a))
    else:
        scaled_image = pygame.transform.smoothscale(image, (w, h))
        for x in range(w):
            for y in range(h):
                r, g, b, a = surface.get_at((x, y))
                if not mask_color or (r, g, b) == mask_color:
                    surface.set_at((x, y), scaled_image.get_at((x, y)))

def toggle_fullscreen(enable):
    global screen, fullscreen, screen_w, screen_h
    if enable:
        fullscreen = True
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_w = screen.get_width()
        screen_h = screen.get_height()
    else:
        fullscreen = False
        screen_w = windowed_w
        screen_h = windowed_h
        screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
        screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)

def main():
    global screen, screen_w, screen_h, windowed_w, windowed_h, corner_hits
    global DEFAULT_SPEED, LOGO_SCALE_FACTOR, LOGO_W, LOGO_H
    if fullscreen: toggle_fullscreen(True)
    spawn_logo()
    onscreen_text = OnScreenText()
    help_enabled = SHOW_HELP_ON_START
    stats_enabled = SHOW_STATS_ON_START
    draw_rectangles = False
    if LOGO_W < 0: LOGO_W = 0
    if LOGO_H < 0: LOGO_H = 0

    prev_frame_time = time.perf_counter()
    showFPS_sum = 0
    showFPS_count = 0
    showFPS_elapsed = 0
    fps_now = "-"
    while True:
        clock.tick(MAX_FPS)
        dt = time.perf_counter() - prev_frame_time
        prev_frame_time = time.perf_counter()
        dt_multiplier = dt * TARGET_FPS

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c or event.key == pygame.K_RETURN:
                    spawn_logo()
                elif event.key == pygame.K_x or event.key == pygame.K_DELETE:
                    kill_logo()
                elif event.key == pygame.K_f or event.key == pygame.K_F11:
                    toggle_fullscreen(not fullscreen)
                    onscreen_text.update_menu_size()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_EQUALS:
                    if LOGO_SCALE_FACTOR < 100: LOGO_SCALE_FACTOR = round(LOGO_SCALE_FACTOR + 0.1, 2)
                    for logo in logos: logo.size(LOGO_W, LOGO_H, LOGO_SCALE_FACTOR)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_MINUS:
                    if LOGO_SCALE_FACTOR > 0.1: LOGO_SCALE_FACTOR = round(LOGO_SCALE_FACTOR - 0.1, 2)
                    for logo in logos: logo.size(LOGO_W, LOGO_H, LOGO_SCALE_FACTOR)
                elif event.key == pygame.K_UP:
                    if DEFAULT_SPEED < 100: DEFAULT_SPEED += 1
                    for logo in logos: logo.change_speed(DEFAULT_SPEED, DEFAULT_SPEED)
                elif event.key == pygame.K_DOWN:
                    if DEFAULT_SPEED > 0: DEFAULT_SPEED -= 1
                    for logo in logos: logo.change_speed(DEFAULT_SPEED, DEFAULT_SPEED)
                elif event.key == pygame.K_s or event.key == pygame.K_TAB:
                    stats_enabled = not stats_enabled
                    if not stats_enabled:
                        showFPS_sum = 0
                        showFPS_count = 0
                        showFPS_elapsed = 0
                        fps_now = "-"
                elif event.key == pygame.K_SPACE:
                    help_enabled = not help_enabled
                elif event.key == pygame.K_d:
                    draw_rectangles = not draw_rectangles
                elif event.key == pygame.K_r:
                    corner_hits = 0
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    screen_w = windowed_w = event.w
                    screen_h = windowed_h = event.h
                    onscreen_text.update_menu_size()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((10,10,10))

        for logo in logos:
            logo.pos += logo.velocity * dt_multiplier
            logo.pos.x = logo.pos.x
            logo.pos.y = logo.pos.y
            edge_collision(logo)
            logo.rect.x = round(logo.pos.x)
            logo.rect.y = round(logo.pos.y)

        if logos:
            tolerance_x = max([abs(logo.velocity.x) for logo in logos]) * dt_multiplier
            tolerance_y = max([abs(logo.velocity.y) for logo in logos]) * dt_multiplier
            object_collision(tolerance_x, tolerance_y)

        for logo in logos:
            logo.rect.x = round(logo.pos.x)
            logo.rect.y = round(logo.pos.y)
            if draw_rectangles:
                pygame.draw.rect(screen, (50, 50, 50), logo.rect)
            screen.blit(logo.image, logo.rect)

        if CornerHitMessage.show_remaining > 0:
            CornerHitMessage.show()
            CornerHitMessage.show_remaining -= dt

        if stats_enabled:
            showFPS_sum += clock.get_fps()
            showFPS_count += 1
            showFPS_elapsed += dt
            if showFPS_elapsed >= FPS_STATS_UPDATE_INTERVAL:
                fps_now = int(showFPS_sum / showFPS_count)
                showFPS_sum = 0
                showFPS_count = 0
                showFPS_elapsed = 0
            onscreen_text.show_HUD(fps_now)
        if help_enabled:
            onscreen_text.show_help()

        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()