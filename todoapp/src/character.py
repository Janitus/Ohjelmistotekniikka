import pygame, map

class Character(pygame.sprite.Sprite):
    def __init__(self, image, pos, width=32, height=32):
        super().__init__()

        # Visuals
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

        # Sprite offset
        self.spritewidth = self.rect[2]
        self.spriteheight = self.rect[3]

        # Collision
        self.width = width
        self.height = height
        self.position = pygame.math.Vector2(pos)

        # Stats
        self.speed = 2
        self.gravity = 0.15
        self.jumpPower = 4
        self.hp = 10

        self.velocity_y = 0


    def apply_gravity(self):
        if(self.canClimb()):
            self.velocity_y = 0
            return
        self.velocity_y += self.gravity
        self.move(0, self.velocity_y)

    def move(self, dx, dy):
        # This function has an issue. The issue is that if the character moves towards the collideable target too fast, there may be a gap between the character and the collideable.
        # This could be fixed by snapping the character as close to the collision as possible, but we'll leave it for later.

        if not self.collides(dx, 0): self.position.x += dx

        if not self.collides(0, dy) and not self.onPlatform(): self.position.y += dy
        else: self.velocity_y = 0


        self.rect.center = self.position

    def canClimb(self):
        if(map.get_ladder_by_coordinate(self.position.y,self.position.x)): return True
        return False
    
    def onPlatform(self):
        if(map.get_platform_by_coordinate(self.position.y+(map.tile_size-3),self.position.x)): return True
        return False

    def moveUpwards(self):
        # Check if ladder present, otherwise attempt to jump
        if(self.canClimb()):
            self.move(0,-self.speed)
            return

        # Jump
        #if(self.velocity_y < 0): return
        if(not self.feet_on_ground()): return # or not self.onPlatform()

        print("jump!",self.velocity_y)

        self.velocity_y = -self.jumpPower

    def moveDownwards(self):
        if(self.canClimb()):
            self.move(0,self.speed)
            return

    def feet_on_ground(self):
        if(map.get_collision_by_coordinate(self.position.y+3,self.position.x)): return True
        return False

    def update(self):
        self.apply_gravity()

    def draw(self, surface, camera_pos):
        sprite_x = self.position[0] - self.spritewidth // 2
        sprite_y = self.position[1] - self.spriteheight

        adjusted_x = sprite_x - camera_pos[0]
        adjusted_y = sprite_y - camera_pos[1]

        surface.blit(self.image, (adjusted_x, adjusted_y))

    def center(self):   return (self.position.x, self.position.y - self.height//2)

    def collides(self, dx, dy):
        # Horizontal and vertical are added towards the direction the character is moving towards. This way we can apply width and height to check for collisions!
        # Note to self, there is probably a bug if the width/height are larger than the tilewidth, as we're not checking the closest tile. Check later.
        # Also it would only be checking for one tile and not multiple as we may want to!

        horizontal = 0
        vertical = 0

        if(dx < 0): horizontal = -self.width//2
        elif(dx > 0): horizontal = self.width//2
        if(dy < 0): vertical = -self.height

        new_x = int(self.position.x + dx + horizontal)
        new_y = int(self.position.y + dy + vertical)

        print(vertical)
        
        #print("pos",self.position," dest",tile, horizontal, vertical)

        if map.get_collision_by_coordinate(new_y,new_x): return True
        return False