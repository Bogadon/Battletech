# Ammo class


class Ammo(object):

    def __init__(self, quant):
        self.name = 'BLANK AMMO'
        self.quantity = 0
        self.damage = 0
        self.weight = 0

    def explode(self):
         dam = self.quantity * self.damage
         self.quantity = 0
         return dam

    def fire(self, num):
        self.quantity -= num
        if self.quantity == 0:
            self.damage = 0
        if self.quantity < 0:
            raise RuntimeError('ammo reduced to below zero')
