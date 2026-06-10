from GameFrame import RoomObject, Globals
import random


class Asteroid(RoomObject):
    """
    A class for Zork's dangerous obstacles
    """

    def __init__(self, room, x, y):
        """
        Initialise the Asteroid object
        """
        RoomObject.__init__(self, room, x, y)

        # set image
        image = self.load_image("asteroid.png")
        self.set_image(image, 50, 49)

        # set travel direction
        angle = random.randint(135, 225)
        self.set_direction(angle, 10)

        # register events
        self.register_collision_object("Ship")

    def step(self):
        """
        Determines what happens to the asteroid on each tick of the game clock
        """
        self.keep_in_room()
        self.outside_of_room()

    def keep_in_room(self):
        """
        Keeps the asteroid inside the top and bottom room limits
        """
        if self.y < 0:
            self.y = 0
            self.y_speed *= -1
        elif self.y > Globals.SCREEN_HEIGHT - self.height:
            self.y = Globals.SCREEN_HEIGHT - self.height
            self.y_speed *= -1

    def outside_of_room(self):
        """
        Removes asteroids that have exited the room
        """
        if self.x + self.width < 0:
            self.room.delete_object(self)

    def handle_collision(self, other, other_type):
        """
        Handles the collision events for the Asteroid
        """
        if other_type == "Ship":
            self.room.delete_object(self)
            self.room.asteroid_collision.play()
            Globals.LIVES -= 1

            if Globals.LIVES > 0:
                # Still alive — update the lives display
                self.room.lives.update_image()
            else:
                # No lives left — go to game over screen
                Globals.next_level = Globals.levels.index("GameOver")
                self.room.running = False