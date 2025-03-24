#level editor version 1

# The first version of a level editor. Made to work with SSB2 Enhanced Edition
# The main game was written before generative AI blew up. The foundation for this editor was 
#   written using ChatGPT and tweaked/fixed by me.

# Written in Python using pygame
# Made by Michael Onate
# March 21, 2025





import os
import sys
import pygame
import time
import subprocess

# -------------------- INITIAL SETUP --------------------

pygame.init()
pygame.mixer.init()

# Window dimensions and grid settings
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 50
GRID_COLS = 16
GRID_ROWS = 15
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)

# Filenames
CUSTOM_WORLDS_FILE = "customWorlds.txt"  # file to hold custom levels

# -------------------- LOAD ASSETS --------------------

# Background (same as main game)
background = pygame.image.load('textures/bg_1.jpg')

# UI images for panels/buttons
shopbg = pygame.image.load('ui/shopbg.png')
play_btn_img = pygame.image.load('ui/restart.png')  # Using play button as "Create" button
pencil_img = pygame.image.load('ui/leveledit.png')
selected_img = pygame.image.load('ui/selected.png')  # checkmark image
exit_img = pygame.image.load('ui/exit.png')
loading_img = pygame.image.load('ui/loading.png')

# Additional UI assets for level management
pencil_img = pygame.image.load('ui/leveledit.png')
trash_img = pygame.image.load('ui/trash.png')
crosshair_img = pygame.image.load('ui/crosshair.png')
crosshair_img = pygame.transform.scale(crosshair_img, (TILE_SIZE, TILE_SIZE))

# Sounds
msclick_sound = pygame.mixer.Sound('sfx/msclick.wav')
chaching_sound = pygame.mixer.Sound('sfx/chaching.wav')
err_sound = pygame.mixer.Sound('sfx/error.wav')

#Music 
pygame.mixer.music.load('sfx/wiishop.mp3')
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1)

# -------------------- TILE OPTIONS --------------------
# Map tile id to its texture (using same textures as in your game)
tile_options = {
    1: pygame.image.load('textures/dirttxt.png'),
    2: pygame.image.load('textures/grasstxt.png'),
    3: pygame.image.load('textures/grass_r_edge_txt.png'),
    4: pygame.image.load('textures/watertxt.png'),
    5: pygame.image.load('textures/cratetxt.png'),
    6: pygame.image.load('textures/dirt_r_edge_txt.png'),
    7: pygame.image.load('textures/float_l_grass.png'),
    8: pygame.image.load('textures/float_c_grass.png'),
    9: pygame.image.load('textures/float_r_grass.png'),
    10: pygame.image.load('textures/sbush.png'),
    11: pygame.image.load('enemy/leaf.png'),
    12: pygame.image.load('textures/lava.png'), #Half-sized lava blocks
    13: pygame.image.load('textures/forcefield.png'),  #OG 'barrier.png' couldnt be seen in-editor. Used this to see forcefields.
    14: pygame.image.load('textures/olava.png'),
    15: pygame.image.load('textures/startxt.png')
}

# Scale each tile option to the tile size
for key in tile_options:
    tile_options[key] = pygame.transform.scale(tile_options[key], (TILE_SIZE, TILE_SIZE))

# -------------------- SCREEN & CLOCK --------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SSB Level Editor")
icon = pygame.image.load('ui/editor_icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# -------------------- FONTS --------------------
font_title = pygame.font.SysFont("Calibri", 50)
font_small = pygame.font.SysFont("Calibri", 19)

# -------------------- HELPER CLASSES --------------------
class Button:
    def __init__(self, x, y, image, text="", font=None, text_color=WHITE):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.font = font
        self.text_color = text_color
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.text and self.font:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# -------------------- STATE MANAGEMENT --------------------
STATE_HOME = 0
STATE_EDITOR = 1
current_state = STATE_HOME

# -------------------- GLOBAL VARIABLES --------------------
# For custom worlds
current_world_name = ""  # name of the world currently being edited
prompting_name = False
name_input = ""
music_muted = False




# For All Worlds Panel
all_worlds_panel_visible = False
all_worlds_edit_buttons = []  # list of tuples (rect, world_dict)
all_worlds_delete_buttons = []  # list of tuples (rect, world_dict)
all_worlds_play_buttons = []

# -------------------- HOME SCREEN UI --------------------
# "Main" buttons
create_button = Button(WIDTH // 2 - 130, HEIGHT // 2, pencil_img, "CREATE", font_small)
switch_button = Button(WIDTH // 2 - 30, HEIGHT // 2, play_btn_img, "Return", font_small)
exit_button = Button(switch_button.rect.right + 20, switch_button.rect.top, exit_img, "Exit", font_small)


# "All Worlds" button (visible if more than 5 worlds exist)
all_worlds_button = Button(WIDTH - 150, HEIGHT - 80, pygame.Surface((120, 40)), "Show All", font_small)
all_worlds_button.image.fill(GREY)




def load_custom_worlds():
    """Load custom levels from CUSTOM_WORLDS_FILE.
    Expected format for each world:
    #WORLD: <world_name>
    <row1>
    <row2>
    ...
    <row15>
    ===
    Returns a list of dicts with keys 'name' and 'grid'."""
    worlds = []
    if os.path.exists(CUSTOM_WORLDS_FILE):
        with open(CUSTOM_WORLDS_FILE, 'r') as f:
            lines = f.read().splitlines()
        current_world = {}
        current_grid = []
        for line in lines:
            if line.startswith("#WORLD:"):
                current_world["name"] = line[len("#WORLD:"):].strip()
            elif line.strip() == "===":
                if current_world and current_grid:
                    current_world["grid"] = current_grid
                    worlds.append(current_world)
                current_world = {}
                current_grid = []
            else:
                row = [int(x) for x in line.split()]
                current_grid.append(row)
        if current_world and current_grid:
            current_world["grid"] = current_grid
            worlds.append(current_world)
    return worlds

recents = load_custom_worlds()[-5:]  # take the last five custom levels

def create_recent_buttons(recents_list):
    """Create buttons for each recent level."""
    buttons = []
    count = len(recents_list)
    start_x = WIDTH // 2 - (count * 70) // 2
    y = HEIGHT - 100  # position near bottom
    for i in range(count):
        btn = Button(start_x + i * 70, y, pygame.Surface((60, 40)))
        btn.image.fill(GREY)
        btn.text = recents_list[i]["name"]
        btn.font = font_small
        buttons.append(btn)
    return buttons

recent_buttons = create_recent_buttons(recents)

def update_all_worlds_buttons():
    """Update buttons for the All Worlds panel."""
    global all_worlds_edit_buttons, all_worlds_delete_buttons
    all_worlds_edit_buttons = []
    all_worlds_delete_buttons = []
    worlds = load_custom_worlds()
    panel_rect = pygame.Rect(100, 100, WIDTH-200, HEIGHT-200)
    row_height = 50
    for i, w in enumerate(worlds):
        y = panel_rect.y + 10 + i * row_height
        # Edit button rect:
        edit_rect = pygame.Rect(panel_rect.x + 300, y, 40, 40)
        # Delete button rect:
        delete_rect = pygame.Rect(panel_rect.x + 350, y, 40, 40)
        all_worlds_edit_buttons.append((edit_rect, w))
        all_worlds_delete_buttons.append((delete_rect, w))

        play_rect = pygame.Rect(panel_rect.x + 400, y, 50, 40)
        all_worlds_play_buttons.append((play_rect, w))

# -------------------- EDITOR VARIABLES --------------------
# Create a blank grid (default level) as a 2D list of 0's (0 means empty)
grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

# Currently selected tile (default to 1: dirt)
selected_tile = 1

# Block picker panel (toggled with E)
block_picker_visible = False
picker_panel_rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
picker_cols = 6  # number of tile options per row in picker
picker_margin = 10
option_size = TILE_SIZE  # size for each tile option

# Save message display
save_message = ""
save_message_time = 0
save_message_color = GREEN

# -------------------- HELPER FUNCTIONS --------------------

def save_current_world():
    """Save the current grid with the current_world_name.
    If the world already exists, update it and return True.
    If it's a new world, append it and return False."""
    worlds = load_custom_worlds()
    global current_world_name, grid
    found = False
    for w in worlds:
        if w["name"] == current_world_name:
            w["grid"] = grid
            found = True
            break
    if not found:
        worlds.append({"name": current_world_name, "grid": grid})
    with open(CUSTOM_WORLDS_FILE, 'w') as f:
        for w in worlds:
            f.write(f"#WORLD: {w['name']}\n")
            for row in w["grid"]:
                f.write(" ".join(str(x) for x in row) + "\n")
            f.write("===\n")
    return found


def delete_world(world_name):
    """Delete a world by name from the custom worlds file."""
    worlds = load_custom_worlds()
    worlds = [w for w in worlds if w["name"] != world_name]
    with open(CUSTOM_WORLDS_FILE, 'w') as f:
        for w in worlds:
            f.write(f"#WORLD: {w['name']}\n")
            for row in w["grid"]:
                f.write(" ".join(str(x) for x in row) + "\n")
            f.write("===\n")

# -------------------- MAIN LOOP --------------------

running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Global events in EDITOR state
        if current_state == STATE_EDITOR:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    music_muted = not music_muted
                    pygame.mixer.music.set_volume(0.0 if music_muted else 0.5)
                if prompting_name:
                    if event.key == pygame.K_RETURN:
                        if 0 < len(name_input) <= 12:
                            current_world_name = name_input
                            prompting_name = False
                            updated = save_current_world()
                            save_message_color = BLACK
                            chaching_sound.play()
                            save_message = "Saved!"
                            save_message_time = pygame.time.get_ticks()
                            recents = load_custom_worlds()[-5:]
                            recent_buttons = create_recent_buttons(recents)
                        else:
                            err_sound.play()
                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                    else:
                        if len(name_input) < 12:
                            name_input += event.unicode
                else:
                    if event.key == pygame.K_e:
                        block_picker_visible = not block_picker_visible
                    elif event.key == pygame.K_s:
                        if current_world_name == "":
                            prompting_name = True
                            name_input = ""
                        else:
                            #Run save func
                            updated = save_current_world()
                            # Spinner loop for 300ms (fast rotation)
                            spinner_angle = 0
                            start_time = pygame.time.get_ticks()
                            while pygame.time.get_ticks() - start_time < 200:
                                dt = clock.tick(FPS)
                                spinner_angle = (spinner_angle - 8) % 360  # Fast rotation
                                screen.blit(background, (0, 0))
                                rotated_spinner = pygame.transform.rotate(loading_img, spinner_angle)
                                spinner_rect = rotated_spinner.get_rect(center=(WIDTH//2, HEIGHT//2))
                                screen.blit(rotated_spinner, spinner_rect)
                                pygame.display.update()
                            save_message_color = BLACK
                            chaching_sound.play()
                            save_message = "Save Successful!"
                            save_message_time = pygame.time.get_ticks()
                            recents = load_custom_worlds()[-5:]
                            recent_buttons = create_recent_buttons(recents)
                    elif event.key == pygame.K_r:
                        if current_world_name != "":
                            prompting_name = True
                            name_input = current_world_name
                        else:
                            err_sound.play()
                    elif event.key == pygame.K_ESCAPE:
                        current_state = STATE_HOME
        
        # Home screen events
        if current_state == STATE_HOME:
            if all_worlds_panel_visible:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    panel_rect = pygame.Rect(100, 100, WIDTH-200, HEIGHT-200)
                    # Check for close panel button
                    close_panel_rect = pygame.Rect(panel_rect.x + panel_rect.width - 50, panel_rect.y + 10, 40, 30)
                    if close_panel_rect.collidepoint(mouse_x, mouse_y):
                        msclick_sound.play()
                        all_worlds_panel_visible = False
                    # Check edit and delete buttons
                    for edit_rect, world in all_worlds_edit_buttons:
                        if edit_rect.collidepoint(mouse_x, mouse_y):
                            msclick_sound.play()
                            grid = world["grid"]
                            current_world_name = world["name"]
                            current_state = STATE_EDITOR
                            all_worlds_panel_visible = False
                    for delete_rect, world in all_worlds_delete_buttons:
                        if delete_rect.collidepoint(mouse_x, mouse_y):
                            msclick_sound.play()
                        # Spinner loop for 300ms (fast rotation) during deletion
                            spinner_angle = 0
                            start_time = pygame.time.get_ticks()
                            while pygame.time.get_ticks() - start_time < 750:
                                dt = clock.tick(FPS)
                                spinner_angle = (spinner_angle - 8) % 360
                                screen.blit(background, (0, 0))
                                rotated_spinner = pygame.transform.rotate(loading_img, spinner_angle)
                                spinner_rect = rotated_spinner.get_rect(center=(WIDTH//2, HEIGHT//2))
                                screen.blit(rotated_spinner, spinner_rect)
                                pygame.display.update()
                            delete_world(world["name"])
                            update_all_worlds_buttons()
                            recents = load_custom_worlds()[-5:]
                            recent_buttons = create_recent_buttons(recents)

                    for play_rect, world in all_worlds_play_buttons:
                        if play_rect.collidepoint(mouse_x, mouse_y):
                            msclick_sound.play()
                            # Write the level's grid to customPreview.txt
                            with open("customPreview.txt", "w") as f:
                                for row in world["grid"]:
                                    f.write(" ".join(str(x) for x in row) + "\n")
                            # Play confirmation feedback
                            save_message_color = GREEN
                            save_message = "Level sent to game!"
                            save_message_time = pygame.time.get_ticks()
                            print("\nLevel sent to game! Return to SSB2 and click [Play Custom] to play it.\n")

                    
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if create_button.is_clicked(event):
                        # Reset the current world to start a new one
                        current_world_name = ""
                        grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
                        current_state = STATE_EDITOR
                        pygame.event.clear()
                        
                    if all_worlds_button.is_clicked(event):
                        msclick_sound.play()
                        all_worlds_panel_visible = True
                        update_all_worlds_buttons()

                    if exit_button.is_clicked(event):
                        pygame.mixer.music.set_volume(0.0)
                        msclick_sound.play()
                        time.sleep(0.3)
                        print("LevelEdit has been closed.")
                        running = False
                    
                    if switch_button.is_clicked(event):
                        msclick_sound.play()
                        switch_message = "Returning to Super Sussy Boy Part II..."
                        print("\nOpening SSB2 Enhanced - Please Wait...\n")
                        # Clear screen and draw background
                        screen.blit(background, (0, 0))
                        # Render the message with white text for contrast
                        message_surface = font_small.render(switch_message, True, WHITE)
                        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        # Create a semi-transparent overlay with padding around the text
                        padding = 10
                        overlay_rect = message_rect.inflate(padding * 2, padding * 2)
                        overlay = pygame.Surface((overlay_rect.width, overlay_rect.height))
                        overlay.set_alpha(128)  # 50% opaque
                        overlay.fill(BLACK)
                        # Blit the overlay and then the text
                        screen.blit(overlay, overlay_rect.topleft)
                        screen.blit(message_surface, message_rect)
                        spinner_angle = 0
                        start_time = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - start_time < 650:
                            dt = clock.tick(FPS)
                            spinner_angle = (spinner_angle - 8) % 360  # Slow rotation
                            screen.blit(background, (0, 0))
                            # Draw overlay message
                            message_surface = font_small.render(switch_message, True, WHITE)
                            message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                            padding = 10
                            overlay_rect = message_rect.inflate(padding * 2, padding * 2)
                            overlay = pygame.Surface((overlay_rect.width, overlay_rect.height))
                            overlay.set_alpha(128)
                            overlay.fill(BLACK)
                            screen.blit(overlay, overlay_rect.topleft)
                            screen.blit(message_surface, message_rect)
                            # Draw loading spinner under the text
                            rotated_spinner = pygame.transform.rotate(loading_img, spinner_angle)
                            spinner_rect = rotated_spinner.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
                            screen.blit(rotated_spinner, spinner_rect)
                            pygame.display.update()
                        print("Closing LevelEditor...\n")
                        subprocess.Popen(["python3", "playgameV2.py"])
                        pygame.quit()
                        sys.exit()
                    for btn in recent_buttons:
                        if btn.is_clicked(event):
                            # Load the selected recent world
                            worlds = load_custom_worlds()
                            for w in worlds:
                                if w["name"] == btn.text:
                                    grid = w["grid"]
                                    current_world_name = w["name"]
                                    break
                            current_state = STATE_EDITOR
        
        # Editor events: grid interactions and block picker clicks
        if current_state == STATE_EDITOR and not prompting_name:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if not block_picker_visible:
                    # Check if click is within the grid area
                    grid_area = pygame.Rect(0, 0, GRID_COLS * TILE_SIZE, GRID_ROWS * TILE_SIZE)
                    if grid_area.collidepoint(mouse_x, mouse_y):
                        col = mouse_x // TILE_SIZE
                        row = mouse_y // TILE_SIZE
                        if event.button == 1:  # left-click: place selected tile
                            if grid[row][col] != selected_tile:
                                grid[row][col] = selected_tile
                                msclick_sound.play()
                        elif event.button == 3:  # right-click: remove tile (set to 0)
                            if grid[row][col] != 0:
                                grid[row][col] = 0
                                msclick_sound.play()
                else:
                    # If block picker is visible, check for clicks inside it
                    if picker_panel_rect.collidepoint(mouse_x, mouse_y):
                        rel_x = mouse_x - picker_panel_rect.x
                        rel_y = mouse_y - picker_panel_rect.y
                        option_col = rel_x // (option_size + picker_margin)
                        option_row = rel_y // (option_size + picker_margin)
                        index = option_row * picker_cols + option_col
                        if index < len(tile_options):
                            selected_tile = list(tile_options.keys())[index]
                            msclick_sound.play()
    
    # Continuous mouse press handling for click-and-hold actions
    if current_state == STATE_EDITOR and not prompting_name and not block_picker_visible:
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] or mouse_buttons[2]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_area = pygame.Rect(0, 0, GRID_COLS * TILE_SIZE, GRID_ROWS * TILE_SIZE)
            if grid_area.collidepoint(mouse_x, mouse_y):
                col = mouse_x // TILE_SIZE
                row = mouse_y // TILE_SIZE
                # If left mouse button is held, place the selected tile
                if mouse_buttons[0] and grid[row][col] != selected_tile:
                    grid[row][col] = selected_tile
                    msclick_sound.play()
                # If right mouse button is held, remove the tile
                if mouse_buttons[2] and grid[row][col] != 0:
                    grid[row][col] = 0
                    msclick_sound.play()
    
    # -------------------- DRAWING --------------------
    screen.blit(background, (0, 0))
    
    if current_state == STATE_HOME:
        # Draw image and title text
        home_icon_rect = icon.get_rect(center=(WIDTH // 2, 180))
        screen.blit(icon, home_icon_rect)

        title_text = font_title.render("SSB Level Editor", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 250))
        screen.blit(title_text, title_rect)
        
        # Draw the Create button
        create_button.draw(screen)
        
        # Draw All Worlds button if more than 5 worlds exist
        if len(load_custom_worlds()) > 0:
            all_worlds_button.draw(screen)
        
        # Draw "Recents:" label and recent level buttons
        recents_label = font_small.render("Recents:", True, BLACK)
        screen.blit(recents_label, (50, HEIGHT - 90))
        for btn in recent_buttons:
            btn.draw(screen)
        switch_button.draw(screen)
        exit_button.draw(screen)
        
        # Draw All Worlds panel if visible
        if all_worlds_panel_visible:
            panel_rect = pygame.Rect(100, 100, WIDTH-200, HEIGHT-200)
            pygame.draw.rect(screen, GREY, panel_rect)
            # Draw close button
            close_panel_rect = pygame.Rect(panel_rect.x + panel_rect.width - 50, panel_rect.y + 10, 40, 30)
            pygame.draw.rect(screen, BLACK, close_panel_rect)
            close_text = font_small.render("X", True, WHITE)
            screen.blit(close_text, close_panel_rect)
            # List all worlds with edit and delete buttons
            worlds = load_custom_worlds()
            row_height = 50
            for i, w in enumerate(worlds):
                y = panel_rect.y + 10 + i * row_height
                name_text = font_small.render(w["name"], True, WHITE)
                screen.blit(name_text, (panel_rect.x + 10, y))
                # Draw edit button (pencil)
                for edit_rect, world in all_worlds_edit_buttons:
                    if world["name"] == w["name"]:
                        screen.blit(pygame.transform.scale(pencil_img, (40,40)), edit_rect)
                # Draw delete button (trash)
                for delete_rect, world in all_worlds_delete_buttons:
                    if world["name"] == w["name"]:
                        screen.blit(pygame.transform.scale(trash_img, (40,40)), delete_rect)

                for play_rect, world in all_worlds_play_buttons:
                    if world["name"] == w["name"]:
                        pygame.draw.rect(screen, (0, 128, 0), play_rect)  # green button
                        play_text = font_small.render("Send", True, WHITE)
                        screen.blit(play_text, play_rect)
    
    elif current_state == STATE_EDITOR:
        # Draw the grid and placed tiles
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                cell_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if grid[row][col] != 0:
                    if grid[row][col] in tile_options:
                        screen.blit(tile_options[grid[row][col]], cell_rect)
                pygame.draw.rect(screen, WHITE, cell_rect, 1)

        # Draw crosshair on hovered grid cell
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_area = pygame.Rect(0, 0, GRID_COLS * TILE_SIZE, GRID_ROWS * TILE_SIZE)
        if grid_area.collidepoint(mouse_x, mouse_y):
            hover_col = mouse_x // TILE_SIZE
            hover_row = mouse_y // TILE_SIZE
            cell_rect = pygame.Rect(hover_col * TILE_SIZE, hover_row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(crosshair_img, cell_rect)

        # Draw editor tooltips at bottom of grid
        tooltip_text = "[E] Block Picker, [S] Save, [R] Rename, [ESC] Leave, [M] Mute music"
        if current_world_name != "":
            tooltip_text = f"Editing: {current_world_name} | " + tooltip_text
        tooltip = font_small.render(tooltip_text, True, WHITE)
        screen.blit(tooltip, (10, GRID_ROWS * TILE_SIZE + 5))
        
        # If prompting for world name, draw input box
        if prompting_name:
            input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 20, 300, 40)
            pygame.draw.rect(screen, BLACK, input_box, 2)
            prompt_text = font_small.render("Enter world name (max 12 chars): " + name_input, True, BLACK)
            screen.blit(prompt_text, (input_box.x + 5, input_box.y + 5))
        
        # Draw the block picker panel if toggled
        if block_picker_visible:
            panel_bg = pygame.transform.scale(shopbg, (picker_panel_rect.width, picker_panel_rect.height))
            screen.blit(panel_bg, (picker_panel_rect.x, picker_panel_rect.y))
            option_index = 0
            for tile_id, tile_img in tile_options.items():
                option_row = option_index // picker_cols
                option_col = option_index % picker_cols
                x = picker_panel_rect.x + picker_margin + option_col * (option_size + picker_margin)
                y = picker_panel_rect.y + picker_margin + option_row * (option_size + picker_margin)
                option_rect = pygame.Rect(x, y, option_size, option_size)
                screen.blit(tile_img, option_rect)
                # Draw checkmark if this option is selected
                if tile_id == selected_tile:
                    screen.blit(selected_img, option_rect)
                option_index += 1
        
        # Draw a save message if one is active
        if save_message:
            if pygame.time.get_ticks() - save_message_time < 2000:  # display for 2 seconds
                msg = font_small.render(save_message, True, save_message_color)
                msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(msg, msg_rect)
            else:
                save_message = ""
    
    pygame.display.update()

pygame.quit()
sys.exit()