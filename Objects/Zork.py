from GameFrame import RoomObject, Globals
from Objects.Asteroid import Asteroid
from Objects.Astronaut import Astronaut
import random


class Zork(RoomObject):
    """
    A class for the game's antagonist.
    Spawn rates for asteroids and astronauts are scaled by difficulty.

    Easy:
      - Asteroids spawn slowly  (every 60-110 ticks)
      - Astronauts spawn often  (every 30-45 ticks)

    Medium:
      - Asteroids spawn steadily (every 30-60 ticks)
      - Astronauts spawn steadily (every 40-60 ticks)

    Hard:
      - Asteroids spawn rapidly  (every 10-25 ticks)
      - Astronauts spawn rarely  (every 60-200 ticks)
    """

    DIFFICULTY_SETTINGS = {
        #           ast_min  ast_max  aut_min  aut_max
        "easy":   (   60,    110,      30,      45  ),
        "medium": (   30,     60,      40,      60  ),
        "hard":   (    10,     25,      60,     200  ),
    }

    def __init__(self, room, x, y):
        """
        Initialise the Zork object
        """
        RoomObject.__init__(self, room, x, y)

        # set image
        image = self.load_image("Zork.png")
        self.set_image(image, 135, 165)

        # set initial movement
        self.y_speed = random.choice([-10, 10])

        # read difficulty chosen on the select screen (default to medium)
        difficulty = getattr(Globals, "difficulty", "medium")
        settings = self.DIFFICULTY_SETTINGS.get(difficulty,
                                                self.DIFFICULTY_SETTINGS["medium"])
        self._ast_min, self._ast_max = settings[0], settings[1]
        self._aut_min, self._aut_max = settings[2], settings[3]

        # start asteroid timer
        self.set_timer(random.randint(self._ast_min, self._ast_max), self.spawn_asteroid)

        # start astronaut timer
        self.set_timer(random.randint(self._aut_min, self._aut_max), self.spawn_astronaut)

    def keep_in_room(self):
        """
        Keeps the Zork inside the top and bottom room limits
        """
        if self.y < 0 or self.y > Globals.SCREEN_HEIGHT - self.height:
            self.y_speed *= -1

    def step(self):
        """
        Determine what happens to Zork on each tick of the game clock
        """
        self.keep_in_room()

    def spawn_asteroid(self):
        """
        Spawns a new Asteroid then resets the timer based on difficulty
        """
        new_asteroid = Asteroid(self.room, self.x, self.y + self.height / 2)
        self.room.add_room_object(new_asteroid)
        self.set_timer(random.randint(self._ast_min, self._ast_max), self.spawn_asteroid)

    def spawn_astronaut(self):
        """
        Spawns a new Astronaut then resets the timer based on difficulty
        """
        new_astronaut = Astronaut(self.room, self.x, self.y + self.height / 2)
        self.room.add_room_object(new_astronaut)
        self.set_timer(random.randint(self._aut_min, self._aut_max), self.spawn_astronaut)