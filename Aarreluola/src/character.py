"""Character is the parent class for both players and enemies"""
import pygame
from map import get_collision_by_coordinate
from map import get_ladder_by_coordinate

# pylint: disable=no-member,c-extension-no-member, too-many-instance-attributes
# Disabloimme too-many-instance-attributes, sillä nämä ovat kaikki tarvittavia attribuutteja.

class Character(pygame.sprite.Sprite):
    """
    Character is the parent class used for either enemies or players. Not to be used as is.
    Attributes:
    spritewidth
    spriteheight
    width (Used for collision)
    height (Used for collision)
    position
    speed (Movement speed)
    gravity
    jump_power
    health
    max_health
    invulnerability_duration in ms, invulnerability is turned on after receiving >= 1 damage
    velocity_y (this value is affected by gravity and knockups, and moves the character up and down)
    """
    def __init__(self, image, width=32, height=32):
        super().__init__()

        # References
        self.projectile_manager = None

        # Visuals
        self.image = image
        self.rect = self.image.get_rect(topleft=(0, 0))

        # Sprite offset
        self.spritewidth = self.rect[2]
        self.spriteheight = self.rect[3]

        # Collision
        self.width = width
        self.height = height
        self.position = pygame.math.Vector2((0, 0))

        # Stats
        self.speed = 0.5
        self.gravity = 0.15
        self.jump_power = 4
        self.health = 1
        self.max_health = 1
        self.invulnerability_duration = 0

        self.last_hit = -9999
        self.velocity_y = 0
        self.direction = pygame.math.Vector2(-1, 0)
        self.dead = False

    def damage(self, amount, knock_up = 0):
        """Damage reduces health, while also starting an invulnerability period"""
        if amount <= 0:
            return False
        if pygame.time.get_ticks() - self.last_hit < self.invulnerability_duration:
            return False

        self.last_hit = pygame.time.get_ticks()
        self.health -= amount
        self.health = max(self.health, 0)

        if knock_up != 0:
            self.knock_up(knock_up)

        if self.health == 0:
            self.die()

        return True

    def die(self):
        """Character dies when they are killed. Who would've known. *Stares in docstring*"""
        self.dead = True

    def heal(self, amount):
        """Heals the character for an amount up till the max health"""
        if amount <= 0:
            return
        self.health += amount
        self.health = min(self.health, self.max_health)

    def knock_up(self, amount):
        """Sends the character flying based on the amount."""
        self.velocity_y = -amount

    def apply_gravity(self):
        """Pulls the character down based on their self.gravity value"""
        if self.can_climb():
            self.velocity_y = 0
            return
        self.velocity_y += self.gravity
        self.velocity_y = min(self.velocity_y, 5)
        self.move(0, self.velocity_y)

    def move(self, dx, dy):
        """Character moves horizontally/vertically, also checks for collision"""
        if not self.collides(dx, 0):
            self.position.x += dx
        if not self.collides(0, dy):
            self.position.y += dy
        else:
            self.velocity_y = 0

        self.rect.center = self.position

    def can_climb(self):
        """Character can climb when they detect a ladder in their position"""
        if get_ladder_by_coordinate(self.position.y, self.position.x):
            return True
        return False

    def move_upwards(self):
        """Attempts to climb if ladder present, or jump if not and floor is right underneath."""
        # Check if ladder present, otherwise attempt to jump
        if self.can_climb():
            self.move(0, -self.speed)
            return

        # Jump
        if not self.feet_on_ground():
            return

        self.velocity_y = -self.jump_power

    def move_downwards(self):
        """Climbs downwards if ladder is present"""
        if self.can_climb():
            self.move(0, self.speed)
            return

    def feet_on_ground(self):
        """Checks whether there is a collision under the character with 3 pixel offset"""
        if get_collision_by_coordinate(self.position.y+3, self.position.x):
            return True
        return False

    def update(self):
        """Applies gravity. Can be used to automate other functions in the future too."""
        self.apply_gravity()

    def draw(self, surface, camera_pos):
        """Draws the character on the given surface based on where the camera is"""
        sprite_x = self.position[0] - self.spritewidth // 2
        sprite_y = self.position[1] - self.spriteheight

        adjusted_x = sprite_x - camera_pos[0]
        adjusted_y = sprite_y - camera_pos[1]

        if self.direction.x > 0:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, (adjusted_x, adjusted_y))
        else:
            surface.blit(self.image, (adjusted_x, adjusted_y))

    def center(self):
        """Returns the position right at the center of the hitbox"""
        return (self.position.x, self.position.y - self.height//2)

    def collides(self, dx, dy):
        """Checks for collisions based on the map and the movement direction."""
        horizontal = 0
        vertical = 0

        if dx < 0:
            horizontal = -self.width//2
        elif dx > 0:
            horizontal = self.width//2
        if dy < 0:
            vertical = -self.height

        new_x = int(self.position[0] + dx + horizontal)
        new_y = int(self.position[1] + dy + vertical)

        if get_collision_by_coordinate(new_y, new_x):
            return True
        return False

    def get_rect(self):
        """Returns hitbox"""
        return pygame.Rect(self.center()[0], self.center()[1], self.width, self.height)
