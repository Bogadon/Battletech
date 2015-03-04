#
# Weapon types
# 

"""
Weapons should be prepended with 'W_' to avoid confusion

"""

from weapon import *

# # # # # # # # # #
# Energy Weapons  #
# # # # # # # # # #

class W_PPC(Weapon):
    def __init__(self, loc, rear=False):
        super(W_PPC, self).__init__(loc, rear)
        self.name = 'PPC'
        self.damage = 10
        self.heat = 10
        self.weight = 7
        self.size = 3
        self.r_min = 3
        self.r_short = 6 
        self.r_med = 12
        self.r_max = 18

class W_S_LAS(Weapon):
    def __init__(self, loc, rear=False):
        super(W_S_LAS, self).__init__(loc, rear)
        self.name = 'Small Laser'
        self.damage = 3
        self.heat = 1
        self.weight = 0.5
        self.size = 1
        self.r_min = 0
        self.r_short = 1
        self.r_med = 2
        self.r_max = 3

class W_M_LAS(Weapon):
    def __init__(self, loc, rear=False):
        super(W_M_LAS, self).__init__(loc, rear)
        self.name = 'Medium Laser'
        self.damage = 5
        self.heat = 3
        self.weight = 1
        self.size = 1
        self.r_min = 0
        self.r_short = 3 
        self.r_med = 6
        self.r_max = 9

class W_L_LAS(Weapon):
    def __init__(self, loc, rear=False):
        super(W_L_LAS, self).__init__(loc, rear)
        self.name = 'Large Laser'
        self.damage = 8
        self.heat = 8
        self.weight = 5
        self.size = 2
        self.r_min = 0
        self.r_short = 5
        self.r_med = 10
        self.r_max = 15

# # # # # # # # # # #
# Ballistic Weapons #
# # # # # # # # # # #

class W_AC_2(Weapon):
    def __init__(self, loc, rear=False):
        super(W_AC_2, self).__init__(loc, rear)
        self.name = 'Autocannon/2'
        self.damage = 2
        self.heat = 1
        self.weight = 6
        self.size = 1
        self.ammo = 'AM_AC_2'
        self.r_min = 4
        self.r_short = 8
        self.r_med = 16
        self.r_max = 24


class W_AC_5(Weapon):
    def __init__(self, loc, rear=False):
        super(W_AC_5, self).__init__(loc, rear)
        self.name = 'Autocannon/5'
        self.damage = 5
        self.heat = 1
        self.weight = 8
        self.size = 4
        self.ammo = 'AM_AC_5'
        self.r_min = 3
        self.r_short = 6
        self.r_med = 12
        self.r_max = 18

class W_AC_10(Weapon):
    def __init__(self, loc, rear=False):
        super(W_AC_10, self).__init__(loc, rear)
        self.name = 'Autocannon/10'
        self.damage = 10
        self.heat = 3
        self.weight = 12
        self.size = 7
        self.ammo = 'AM_AC_10'
        self.r_min = 0
        self.r_short = 5
        self.r_med = 10
        self.r_max = 15

class W_AC_20(Weapon):
    def __init__(self, loc, rear=False):
        super(W_AC_20, self).__init__(loc, rear)
        self.name = 'Autocannon/10'
        self.damage = 20
        self.heat = 7
        self.weight = 14
        self.size = 10
        self.ammo = 'AM_AC_20'
        self.r_min = 0
        self.r_short = 3
        self.r_med = 6
        self.r_max = 9

# # # # # # #
# Missiles  #
# # # # # # #

class W_SRM(Weapon):
    def __init__(self, racks, loc, rear=False):
        super(W_SRM, self).__init__(loc, rear)
        self.name = 'SRM_%d' %racks
        self.damage = 2
        self.heat = 1 + racks / 2
        self.weight = racks / 2
        self.size = racks / 3
        self.rof = racks
        self.ammo = 'AM_SRM'
        self.r_min = 0
        self.r_short = 3 
        self.r_med = 6
        self.r_max = 9
        
class W_LRM(Weapon):
    def __init__(self, racks, loc, rear=False):
        super(W_LRM, self).__init__(loc, rear)
        self.name = 'LRM_%d' %racks
        self.damage = 1
        self.heat = racks / 3
        if racks <= 10:
            self.heat += 1
        self.weight = racks / 2
        self.size = racks / 3
        self.rof = racks
        self.ammo = 'AM_LRM'
        self.r_min = 6
        self.r_short = 7 
        self.r_med = 14
        self.r_max = 21

        


