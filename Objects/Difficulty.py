from GameFrame import RoomObject, Globals


class Difficulty(RoomObject):
    """
    A class to store and provide difficulty settings for the game.
    Difficulty is set from the SelectDifficulty room and read by Zork
    when spawning asteroids and astronauts.
    """

    def __init__(self, room, x, y):
        """
        Initialise the Difficulty object
        """
        RoomObject.__init__(self, room, x, y)

        # Spawn timer ranges per difficulty: (asteroid_min, asteroid_max, astronaut_min, astronaut_max)
        self.settings = {
            "easy":   (60, 110, 30, 45),   # fewer asteroids, more astronauts
            "medium": (30, 60, 40, 60),  # balanced (same as original Zork defaults)
            "hard":   (10,  25, 60, 200),  # more asteroids, fewer astronauts
        }

         # set image
        image = self.load_image("Select_difficulty_0.png")
        self.set_image(image,400,600)

        # set image
        image = self.load_image("Select_difficulty_1.png")
        self.set_image(image,8400,600)

        # set image
        image = self.load_image("Select_difficulty_2.png")
        self.set_image(image,400,600)

    def get_asteroid_range(self):
        """
        Returns (min, max) spawn timer range for asteroids based on current difficulty
        """
        diff = getattr(Globals, "difficulty", "medium")
        return self.settings.get(diff, self.settings["medium"])[:2]

    def get_astronaut_range(self):
        """
        Returns (min, max) spawn timer range for astronauts based on current difficulty
        """
        diff = getattr(Globals, "difficulty", "medium")
        return self.settings.get(diff, self.settings["medium"])[2:]