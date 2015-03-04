#
# Ammo types
#

"""
class names should be prepended with 'A_' to avoid confusion

damage is for volatility in ammo explosion

"""

from ammo import *

class A_SRM(Ammo):
    def __init__(self, quant=100):
        super(A_SRM, self).__init__(self)
        self.name = 'AM_SRM'
        self.quantity = quant
        self.damage = 2
        self.weight = quant / 100.

class A_LRM(Ammo):
    def __init__(self, quant=120):
        super(A_LRM, self).__init__(self)
        self.name = 'AM_LRM'
        self.quantity = quant
        self.damage = 1
        self.weight = quant / 120.


class A_AC_2(Ammo):
    def __init__(self, quant=45):
        super(A_AC_2, self).__init__(self)
        self.name = 'AM_AC_2'
        self.quantity = quant
        self.damage = 2
        self.weight = quant / 45.

class A_AC_5(Ammo):
    def __init__(self, quant=20):
        super(A_AC_5, self).__init__(self)
        self.name = 'AM_AC_5'
        self.quantity = quant
        self.damage = 5
        self.weight = quant / 20.

class A_AC_10(Ammo):
    def __init__(self, quant=10):
        super(A_AC_10, self).__init__(self)
        self.name = 'AM_AC_10'
        self.quantity = quant
        self.damage = 10
        self.weight = quant / 10.

class A_AC_20(Ammo):
    def __init__(self, quant=5):
        super(A_AC_20, self).__init__(self)
        self.name = 'AM_AC_20'
        self.quantity = quant
        self.damage = 20
        self.weight = quant / 5.


