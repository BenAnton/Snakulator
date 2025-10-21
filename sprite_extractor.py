import pygame
import sys
import json
import os

# Initialize Pygame
pygame.init()

# Configuration
SPRITESHEET_PATH = 'Graphics/SnakeSprites.png'  # Change this to your file path
OUTPUT_DIR = 'extracted_sprites'
SPRITE_DATA_FILE = 'sprite_data.json'

# Alternative: Use absolute path if relative doesn't work
# SPRITESHEET_PATH = '/Users/benanton/PycharmProjects/Snakulator/Graphics/SnakeSprites.png'
SCALE = 3  # Scale factor for easier viewing
GRID_SIZE = 16  # Snap to grid (16 or 32 pixels typically)
SNAP_TO_GRID = True

# Colors
BG_COLOR = (40, 40, 40)
GRID_COLOR = (60, 60, 60)
SELECTION_COLOR = (255, 255, 0)
SAVED_COLOR = (0, 255, 0)
CURRENT_COLOR = (255, 0, 0)


class SpriteExtractor:
    def __init__(self):
        # Load spritesheet (before convert_alpha, we just need to load it)
        try:
            # Try to resolve the path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(script_dir, SPRITESHEET_PATH)

            print(f"Looking for spritesheet at: {full_path}")

            if os.path.exists(full_path):
                self.spritesheet = pygame.image.load(full_path)
                print(f"Successfully loaded: {full_path}")
            elif os.path.exists(SPRITESHEET_PATH):
                self.spritesheet = pygame.image.load(SPRITESHEET_PATH)
                print(f"Successfully loaded: {SPRITESHEET_PATH}")
            else:
                print(f"Error: Could not find file at:")
                print(f"  - {full_path}")
                print(f"  - {SPRITESHEET_PATH}")
                print(f"\nCurrent working directory: {os.getcwd()}")
                print(f"Script directory: {script_dir}")
                sys.exit(1)
        except Exception as e:
            print(f"Error loading spritesheet: {e}")
            sys.exit(1)

        # Setup display first
        self.screen_width = self.spritesheet.get_width() * SCALE + 400
        self.screen_height = max(self.spritesheet.get_height() * SCALE + 100, 600)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Spritesheet Extractor - Click and drag to select sprites')

        # Now convert_alpha after display is set
        self.spritesheet = self.spritesheet.convert_alpha()

        # Scale up for display
        self.scaled_sheet = pygame.transform.scale(
            self.spritesheet,
            (self.spritesheet.get_width() * SCALE,
             self.spritesheet.get_height() * SCALE)
        )

        # State
        self.start_pos = None
        self.current_pos = None
        self.sprites = []
        self.selected_sprite = None
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        # Load existing sprite data if available
        self.load_sprite_data()

        # Create output directory
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    def snap_to_grid(self, value):
        """Snap a value to the grid"""
        if SNAP_TO_GRID:
            return (value // GRID_SIZE) * GRID_SIZE
        return value

    def screen_to_sheet_coords(self, pos):
        """Convert screen coordinates to spritesheet coordinates"""
        x = pos[0] // SCALE
        y = pos[1] // SCALE
        return (x, y)

    def sheet_to_screen_coords(self, pos):
        """Convert spritesheet coordinates to screen coordinates"""
        return (pos[0] * SCALE, pos[1] * SCALE)

    def load_sprite_data(self):
        """Load previously saved sprite data"""
        if os.path.exists(SPRITE_DATA_FILE):
            try:
                with open(SPRITE_DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.sprites = [(s['name'], s['x'], s['y'], s['w'], s['h'])
                                    for s in data]
                print(f"Loaded {len(self.sprites)} sprites from {SPRITE_DATA_FILE}")
            except Exception as e:
                print(f"Could not load sprite data: {e}")

    def save_sprite_data(self):
        """Save sprite data to JSON file"""
        data = [{'name': name, 'x': x, 'y': y, 'w': w, 'h': h}
                for name, x, y, w, h in self.sprites]
        with open(SPRITE_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(self.sprites)} sprites to {SPRITE_DATA_FILE}")

    def extract_sprite(self, x, y, w, h, name):
        """Extract and save a sprite"""
        if w <= 0 or h <= 0:
            return

        sprite_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite_surface.blit(self.spritesheet, (0, 0), (x, y, w, h))

        filename = f"{name}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        pygame.image.save(sprite_surface, filepath)
        print(f"Saved: {filepath} ({w}x{h})")

    def draw_grid(self):
        """Draw grid overlay"""
        for x in range(0, self.scaled_sheet.get_width(), GRID_SIZE * SCALE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0),
                             (x, self.scaled_sheet.get_height()), 1)
        for y in range(0, self.scaled_sheet.get_height(), GRID_SIZE * SCALE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y),
                             (self.scaled_sheet.get_width(), y), 1)

    def draw_ui(self):
        """Draw UI elements"""
        ui_x = self.scaled_sheet.get_width() + 20
        y = 20

        # Instructions
        instructions = [
            "CONTROLS:",
            "- Click & drag: Select sprite",
            "- Enter: Save selected sprite",
            "- D: Delete selected sprite",
            "- S: Save all data to JSON",
            "- G: Toggle grid snap",
            "- C: Clear all sprites",
            "- ESC: Quit",
            "",
            f"Grid Snap: {'ON' if SNAP_TO_GRID else 'OFF'}",
            f"Grid Size: {GRID_SIZE}px",
            f"Total Sprites: {len(self.sprites)}",
        ]

        for line in instructions:
            text = self.small_font.render(line, True, (200, 200, 200))
            self.screen.blit(text, (ui_x, y))
            y += 25

        # Current selection info
        if self.current_pos and self.start_pos:
            y += 20
            x1, y1 = self.screen_to_sheet_coords(self.start_pos)
            x2, y2 = self.screen_to_sheet_coords(self.current_pos)
            x, y_pos = min(x1, x2), min(y1, y2)
            w, h = abs(x2 - x1), abs(y2 - y1)

            text = self.font.render("CURRENT SELECTION:", True, (255, 255, 0))
            self.screen.blit(text, (ui_x, y))
            y += 30

            info = [
                f"Position: ({x}, {y_pos})",
                f"Size: {w}x{h}",
                f"",
                "Press ENTER to save"
            ]
            for line in info:
                text = self.small_font.render(line, True, (200, 200, 200))
                self.screen.blit(text, (ui_x, y))
                y += 25

        # List of saved sprites
        if self.sprites:
            y = self.screen_height - 300
            text = self.font.render("SAVED SPRITES:", True, (0, 255, 0))
            self.screen.blit(text, (ui_x, y))
            y += 30

            # Show last 10 sprites
            for i, (name, x, y_pos, w, h) in enumerate(self.sprites[-10:]):
                sprite_text = f"{name}: ({x},{y_pos}) {w}x{h}"
                text = self.small_font.render(sprite_text, True, (150, 150, 150))
                self.screen.blit(text, (ui_x, y))
                y += 20

    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                elif event.key == pygame.K_RETURN and self.start_pos and self.current_pos:
                    # Save current selection
                    x1, y1 = self.screen_to_sheet_coords(self.start_pos)
                    x2, y2 = self.screen_to_sheet_coords(self.current_pos)
                    x, y = min(x1, x2), min(y1, y2)
                    w, h = abs(x2 - x1), abs(y2 - y1)

                    name = f"sprite_{len(self.sprites):03d}"
                    self.sprites.append((name, x, y, w, h))
                    self.extract_sprite(x, y, w, h, name)

                    self.start_pos = None
                    self.current_pos = None

                elif event.key == pygame.K_s:
                    # Save sprite data
                    self.save_sprite_data()

                elif event.key == pygame.K_g:
                    # Toggle grid snap
                    global SNAP_TO_GRID
                    SNAP_TO_GRID = not SNAP_TO_GRID
                    print(f"Grid snap: {'ON' if SNAP_TO_GRID else 'OFF'}")

                elif event.key == pygame.K_c:
                    # Clear all sprites
                    if self.sprites:
                        confirm = input("Clear all sprites? (y/n): ")
                        if confirm.lower() == 'y':
                            self.sprites = []
                            print("Cleared all sprites")

                elif event.key == pygame.K_d:
                    # Delete last sprite
                    if self.sprites:
                        removed = self.sprites.pop()
                        print(f"Removed: {removed[0]}")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] < self.scaled_sheet.get_width():
                    x, y = self.screen_to_sheet_coords(event.pos)
                    x = self.snap_to_grid(x)
                    y = self.snap_to_grid(y)
                    self.start_pos = self.sheet_to_screen_coords((x, y))

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.start_pos:
                    self.current_pos = event.pos

            elif event.type == pygame.MOUSEMOTION:
                if self.start_pos:
                    x, y = self.screen_to_sheet_coords(event.pos)
                    x = self.snap_to_grid(x)
                    y = self.snap_to_grid(y)
                    self.current_pos = self.sheet_to_screen_coords((x, y))

        return True

    def draw(self):
        """Draw everything"""
        self.screen.fill(BG_COLOR)

        # Draw spritesheet
        self.screen.blit(self.scaled_sheet, (0, 0))

        # Draw grid
        self.draw_grid()

        # Draw saved sprites
        for name, x, y, w, h in self.sprites:
            screen_rect = pygame.Rect(x * SCALE, y * SCALE, w * SCALE, h * SCALE)
            pygame.draw.rect(self.screen, SAVED_COLOR, screen_rect, 2)

        # Draw current selection
        if self.start_pos and self.current_pos:
            x = min(self.start_pos[0], self.current_pos[0])
            y = min(self.start_pos[1], self.current_pos[1])
            w = abs(self.current_pos[0] - self.start_pos[0])
            h = abs(self.current_pos[1] - self.start_pos[1])
            pygame.draw.rect(self.screen, CURRENT_COLOR, (x, y, w, h), 3)

        # Draw UI
        self.draw_ui()

        pygame.display.flip()

    def run(self):
        """Main loop"""
        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.handle_events()
            self.draw()
            clock.tick(60)

        # Save on exit
        if self.sprites:
            self.save_sprite_data()

        pygame.quit()
        print(f"\nExtracted {len(self.sprites)} sprites to '{OUTPUT_DIR}' directory")
        print(f"Sprite data saved to '{SPRITE_DATA_FILE}'")


if __name__ == '__main__':
    extractor = SpriteExtractor()
    extractor.run()