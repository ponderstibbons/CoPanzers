import math, pygame

from pytanks import GameObject
import pytanks.weapon as weapon
import pytanks.target as target

class Turret (GameObject):

    def __init__ (self, hp, cannon, *args, **kw):
        """
        hp     -- int, hitpoints for the turret
        cannon -- pytanks.weapon.Weapon, the cannon for this turret
        """

        self.cannon = cannon
        self.target = None

        GameObject.__init__ (self, *args, **kw)
        target.init (self, hp)

    def step (self, others, dt):

        self.cannon.step (dt)
        target.step (self, others, dt)

        if not self.target:
            try:
                self.target = next (filter (lambda x: hasattr (x, "health"), others))
            except StopIteration:
                return 

        if self.target.health.hp <= 0:
            self.target = None
            return

        if self.cannon.reloaded > 0:
            return # our weapon is not ready to fire

        mpos = self.position
        tpos = self.target.position
        dx = tpos [0] - mpos [0]
        dy = tpos [1] - mpos [1]
        angle = math.acos (dx / math.sqrt (dx ** 2 + dy ** 2))

        bullet = self.cannon.shoot (angle, mpos)
        others.append (bullet)

    def draw (self, surface):

        GameObject.draw (self, surface)
        self.cannon.draw (surface, self.position)
        target.draw (self, surface)

        if self.target:
            pygame.draw.circle (surface, (255, 0, 0), tuple (map (int, self.target.position)), 20, 1)

class ExampleTurret (Turret):

    def __init__ (self, *args, **kw):

        s = pygame.Surface ((30, 30))
        s.set_colorkey ( (0, 0, 0) )
        pygame.draw.polygon (s, (0, 155, 0), ((0, 15), (15, 0), (30, 15), (15, 30)))
        pygame.draw.polygon (s, (0, 0, 0), ((0, 15), (15, 0), (30, 15), (15, 30)), 1)
        Turret.__init__ (self, 80, weapon.ExampleWeapon (), s, *args, **kw)
