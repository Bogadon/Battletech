#
# Battletech Player class
# Written by Kazimierz, Oct 2012
#

"""

"""

#from copy import deepcopy

from btlib import d6


class Player(object):

    def __init__(self, name, mechs):
        self.name = name
        self.units_live = mechs #[]
        self.units_dead = []
        self.units_active = []
        self.initiative = 0
        self.is_ai = False

    def gen_init(self):
        self.initiative = d6(2)
        #return self.initiative

    def get_units_active(self):
        ret = []
        for Unit in self.units_active:
            ret.append(Unit)
        return ret

    def gen_status(self):
        for Unit in self.units_live:
            Unit.init_turn()
        live = []
        act = []
        for Unit in self.units_live:
            if Unit.destroyed:
                self.units_dead.append(Unit)
            else:
                live.append(Unit)
                if not Unit.shutdown and Unit.conscious:
                    act.append(Unit)
        self.units_live = live
        self.units_active = act


    # JUNK Get quick status of mechs
    def get_quick_status(self):
        stat = []
        for mech in self.mechs:
            entry = {}
            entry['name'] = mech.name
            if mech.destroyed:
                entry['destroyed'] = True
            else:
                entry['armour'] = mech.armour
                entry['heat'] = mech.heat
                if not mech.conscious:
                    entry['conscious'] = False
                elif mech.shutdown:
                    entry['shutdown'] = True
                else:
                    entry['weapons'] = mech.weapons
                
            entry['pilot'] = mech.details['pilot']
            entry['health'] = mech.details['health']
            stat.append(entry)
        
        return stat


class Human_Player(Player):

    def __init__(self):
        super(Human_Player, self).__init__()
