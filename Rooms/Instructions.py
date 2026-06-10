from GameFrame import Level, Globals
import pygame


class Instructions(Level):
    """
    Displays the game instructions before the difficulty select screen.
    Press ENTER to skip.
    """

    def __init__(self, screen, joysticks):
        Level.__init__(self, screen, joysticks)

        pygame.font.init()

        # Fonts
        self.font_title   = pygame.font.SysFont("Arial Black", 64, bold=True)
        self.font_heading = pygame.font.SysFont("Arial Black", 36, bold=True)
        self.font_body    = pygame.font.SysFont("Arial", 30)
        self.font_skip    = pygame.font.SysFont("Arial", 28)

        # Colours
        self.COL_TITLE   = (0, 220, 255)   # cyan
        self.COL_HEADING = (255, 220, 0)   # yellow
        self.COL_BODY    = (255, 255, 255) # white
        self.COL_SKIP    = (160, 160, 160) # grey
        self.COL_BG      = (10, 10, 30)    # dark navy

        # Pre-render all text surfaces so they are not rebuilt every frame
        self._build_surfaces()

    def _build_surfaces(self):
        """Pre-render every text surface once."""

        self.surf_title = self.font_title.render(
            "How to Play", True, self.COL_TITLE)

        self.surf_controls_heading = self.font_heading.render(
            "Controls", True, self.COL_HEADING)

        self.surf_objective_heading = self.font_heading.render(
            "Objective", True, self.COL_HEADING)

        controls = [
            "W          —   Move Up",
            "S           —   Move Down",
            "SPACE  —   Shoot Laser",
        ]
        self.surf_controls = [
            self.font_body.render(line, True, self.COL_BODY)
            for line in controls
        ]

        objective_lines = [
            "Destroy asteroids and collect astronauts",
            "to earn as many points as possible.",
            "Watch your lives — each asteroid hit costs one!",
        ]
        self.surf_objective = [
            self.font_body.render(line, True, self.COL_BODY)
            for line in objective_lines
        ]

        self.surf_skip = self.font_skip.render(
            "Press ENTER to skip", True, self.COL_SKIP)

    def run(self):
        # Not the first play — jump straight to SelectDifficulty
        if not Globals.first_play:
            Globals.next_level = Globals.levels.index("SelectDifficulty")
            return Globals.exiting

        # Mark as seen so it won't show again this session
        Globals.first_play = False

        self.running = True

        while self.running:
            self._clock.tick(Globals.FRAMES_PER_SECOND)

            # --- Events ---
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    Globals.exiting = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Skip straight to difficulty select
                        Globals.next_level = Globals.levels.index("SelectDifficulty")
                        self.running = False

            # --- Draw background ---
            self.screen.fill(self.COL_BG)

            cx = Globals.SCREEN_WIDTH // 2  # horizontal centre
            y = 60                           # vertical drawing cursor

            # --- Title ---
            self.screen.blit(self.surf_title,
                             (cx - self.surf_title.get_width() // 2, y))
            y += self.surf_title.get_height() + 40

            # --- Divider ---
            pygame.draw.line(self.screen, self.COL_TITLE,
                             (100, y), (Globals.SCREEN_WIDTH - 100, y), 2)
            y += 30

            # --- Controls heading ---
            self.screen.blit(self.surf_controls_heading,
                             (cx - self.surf_controls_heading.get_width() // 2, y))
            y += self.surf_controls_heading.get_height() + 16

            # --- Control lines ---
            for surf in self.surf_controls:
                self.screen.blit(surf, (cx - surf.get_width() // 2, y))
                y += surf.get_height() + 10
            y += 30

            # --- Divider ---
            pygame.draw.line(self.screen, self.COL_HEADING,
                             (100, y), (Globals.SCREEN_WIDTH - 100, y), 2)
            y += 30

            # --- Objective heading ---
            self.screen.blit(self.surf_objective_heading,
                             (cx - self.surf_objective_heading.get_width() // 2, y))
            y += self.surf_objective_heading.get_height() + 16

            # --- Objective lines ---
            for surf in self.surf_objective:
                self.screen.blit(surf, (cx - surf.get_width() // 2, y))
                y += surf.get_height() + 10

            # --- Skip prompt pinned to bottom ---
            skip_x = cx - self.surf_skip.get_width() // 2
            skip_y = Globals.SCREEN_HEIGHT - self.surf_skip.get_height() - 30
            self.screen.blit(self.surf_skip, (skip_x, skip_y))

            pygame.display.update()

        return Globals.exiting