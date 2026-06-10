from GameFrame import Level, Globals
import pygame
import os


class GameOver(Level):
    """
    A game-over screen that displays the final score and a background image.
    Press R to return to the title/welcome screen.
    """

    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)

        # Load and scale game over image to slightly smaller than the screen
        border = 40  # pixels of border on each side
        target_w = Globals.SCREEN_WIDTH - (border * 2)
        target_h = Globals.SCREEN_HEIGHT - (border * 2)
        raw_image = pygame.image.load(
            os.path.join("Images", "Gameover.png")
        ).convert_alpha()
        self.gameover_image = pygame.transform.scale(raw_image, (target_w, target_h))
        self.image_x = border
        self.image_y = border

        # Prepare fonts
        pygame.font.init()
        self.font_large = pygame.font.SysFont("Arial Black", 80, bold=True)
        self.font_small = pygame.font.SysFont("Arial Black", 40)

    def run(self):
        """
        Display the game-over screen with the final score at the top.
        Press R to return to the Welcome screen.
        """
        self.running = True

        while self.running:
            self._clock.tick(Globals.FRAMES_PER_SECOND)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    Globals.exiting = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game state for a fresh run
                        Globals.SCORE = 0
                        Globals.LIVES = 3
                        Globals.difficulty = "medium"
                        Globals.next_level = Globals.levels.index("WelcomeScreen")
                        self.running = False

            # --- Draw background ---
            self.screen.fill((0, 0, 0))

            # --- Draw scaled game over image ---
            self.screen.blit(self.gameover_image, (self.image_x, self.image_y))

            # --- Draw final score at the top of the screen ---
            score_text = self.font_large.render(
                f"Score: {Globals.SCORE}", True, (255, 255, 255)
            )
            score_x = (Globals.SCREEN_WIDTH - score_text.get_width()) // 2
            score_y = 20  # near the very top
            self.screen.blit(score_text, (score_x, score_y))

            # --- Draw prompt near the bottom ---
            prompt_text = self.font_small.render(
                "Press R to return to title", True, (200, 200, 200)
            )
            prompt_x = (Globals.SCREEN_WIDTH - prompt_text.get_width()) // 2
            prompt_y = Globals.SCREEN_HEIGHT - 60
            self.screen.blit(prompt_text, (prompt_x, prompt_y))

            pygame.display.update()

        return Globals.exiting