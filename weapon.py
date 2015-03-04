# Weapon class

class Weapon(object):

    def __init__(self, loc, rear=False):
        self.name = 'BLANK WEAPON'
        self.destroyed = False
        self.ammo = None # Does it need ammo
        self.location = loc
        self.rear = rear

        self.damage = 0
        self.rof = 1 # eg PPC = 1, LRM20 = 20
        self.heat = 0
        self.weight = 0
        self.size = 1

        self.r_min = 0
        self.r_short = 0
        self.r_med = 0
        self.r_max = 0 # long

    def range_mod(self, dist, ang):
        if not self.angle_check(ang):
            return 99
        elif dist > self.r_max:
            return 99
        elif dist > self.r_med:
            return 4
        elif dist > self.r_short:
            return 2
        elif dist <= self.r_min:
            return 1 + self.r_min - dist
        else:
            return 0

    def angle_check(self, ang):
        if self.rear and (135 <= ang <= 225):
            return True
        elif self.location == 'larm' and (ang <= 45 or ang >= 225):
            return True
        elif self.location == 'rarm' and (ang <= 135 or ang >= 315):
            return True
        # Front mounted
        elif ang <= 60 or ang >= 300:
            return True
        else:
            return False



