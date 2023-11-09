import pygame
from character import Character

class Player(Character):
    def __init__(self, image, pos, width=16, height=24):
        super().__init__(image, pos, width, height)
        self.money = 0
        self.life = 3
        self.ammo = 4
        self.max_ammo = 4
        self.keys = set()
        self.invulnerability_duration = 1000
        self.last_shot = -9999
        self.shot_cooldown = 1000

    def update(self, keys):
        super().update()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.moveUpwards()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.moveDownwards()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move(-self.speed, 0)
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move(self.speed, 0)
            self.direction.x = 1
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            self.shoot()

    def shoot(self):
        if(self.ammo <= 0): return False
        if (pygame.time.get_ticks() - self.last_shot < self.shot_cooldown): return False

        self.last_shot = pygame.time.get_ticks()
        self.ammo -= 1
        print("shoot")
        return True

    def receive_key (self, key_name):
        self.keys.add(key_name)
        print(key_name)

    def receive_ammo(self, amount):
        if(amount <= 0): return
        self.ammo += amount
        self.ammo = min(self.ammo,self.max_ammo)

    def receive_life(self, amount):
        self.life += amount

    def receive_money(self, amount):
        self.money += amount

    def purchase_item (self, price):
        if(price > self.money): return False
        self.money -= price
        return True

    def draw(self, surface, camera_pos):
        super().draw(surface, camera_pos)

        #surface.blit(self.image, (self.rect.x - camera_pos[0], self.rect.y - camera_pos[1]))
        #surface.blit(self.image, self.rect)
