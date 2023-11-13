from projectile import Projectile


class ProjectileManager():
    def __init__(self, player, enemies):
        self.projectiles = []
        self.enemies = enemies
        self.player = player

    def create_projectile(self, pos, direction, source):
        new_projectile = Projectile(pos, direction, source)
        self.projectiles.append(new_projectile)
        return new_projectile

    def update(self):
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.check_collision() or self.check_entity_collision(projectile):
                self.projectiles.remove(projectile)

    def draw(self, surface, camera_pos):
        for proj in self.projectiles:
            proj.draw(surface, camera_pos)

    def check_entity_collision(self, projectile):
        if projectile.source == "player":
            for enemy in self.enemies:
                if enemy.rect.colliderect(projectile.rect):
                    enemy.damage(projectile.damage)
                    enemy.knock_up(projectile.knock_power)
                    return True
        elif projectile.source == "enemy":
            if self.player.rect.colliderect(projectile.rect):
                self.player.damage(projectile.damage)
                return True

        return False
