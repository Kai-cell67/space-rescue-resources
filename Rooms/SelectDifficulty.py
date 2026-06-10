from GameFrame import Level, Globals
import pygame
import os


class SelectDifficulty(Level):
    """
    A room that displays a difficulty selection screen.
    The player presses E (Easy), M (Medium), or H (Hard) to choose.
    The image is centred on the screen and updates to reflect the selection.
    """

    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)

        # Image name map
        self.image_map = {
            "easy":   "Select_difficulty_0.png",
            "medium": "Select_difficulty_1.png",
            "hard":   "Select_difficulty_2.png",
        }

        # Load all three images upfront
        self.difficulty_images = {}
        for key, filename in self.image_map.items():
            path = os.path.join("Images", filename)
            img = pygame.image.load(path).convert_alpha()
            self.difficulty_images[key] = img

        # Start with easy previewed
        self._previewed = "easy"
        self._current_image = self.difficulty_images["easy"]

    def _set_difficulty_image(self, difficulty):
        """
        Swaps the displayed image to match the given difficulty.
        """
        self._previewed = difficulty
        self._current_image = self.difficulty_images[difficulty]

    def _confirm_difficulty(self, difficulty):
        """
        Saves the chosen difficulty to Globals and advances to GamePlay.
        """
        Globals.difficulty = difficulty
        Globals.next_level = Globals.levels.index("GamePlay")
        self.running = False

    def catch_events(self, events):
        """
        Listen for E / M / H key presses.
        First press previews (updates image), second press confirms.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self._previewed == "easy":
                        self._confirm_difficulty("easy")
                    else:
                        self._set_difficulty_image("easy")

                elif event.key == pygame.K_m:
                    if self._previewed == "medium":
                        self._confirm_difficulty("medium")
                    else:
                        self._set_difficulty_image("medium")

                elif event.key == pygame.K_h:
                    if self._previewed == "hard":
                        self._confirm_difficulty("hard")
                    else:
                        self._set_difficulty_image("hard")

    def run(self):
        """
        Override run to draw the difficulty image centred on screen each frame.
        """
        self.running = True

        while self.running:
            self._clock.tick(Globals.FRAMES_PER_SECOND)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    Globals.exiting = True

            self.catch_events(events)

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Draw difficulty image centred on screen
            img = self._current_image
            img_w = img.get_width()
            img_h = img.get_height()
            x = (Globals.SCREEN_WIDTH - img_w) // 2
            y = (Globals.SCREEN_HEIGHT - img_h) // 2
            self.screen.blit(img, (x, y))

            pygame.display.update()

        return Globals.exiting