#
# Mech subclasses
#

"""
Currently the syntax needs to entered exactly- equip must match weps/ammo/heatsinks

mechs should be prepended with 'M_' to avoid confusion

"""

from mech import *
from weapon_types import *
from ammo_types import *

class M_Jenner(Mech):

    def __init__(self, pilot, pilotting, gunnery):
        details = {}
        details['name'] = 'Jenner'
        details['code'] = 'JR7-D'
        details['tonnage'] = 35
        details['year'] = 2784
        details['cost'] = 3198376
        details['tech'] = 'Inner Sphere'
        details['pilot'] = pilot
        super(M_Jenner, self).__init__(details, pilotting, gunnery)

        self.symbol = 'JE'

        self.walk = 7
        self.run = 11
        self.jump = 5
        self.heat_sinks = 10
        
        # [Front, internal, rear]
        self.armour['head'] = [7, 3]
        self.armour['ct'] = [10, 11, 3]
        self.armour['lt'] = [8, 8, 4]
        self.armour['rt'] = [8, 8, 4]
        self.armour['larm'] = [4, 6]
        self.armour['rarm'] = [4, 6]
        self.armour['lleg'] = [4, 8]
        self.armour['rleg'] = [4, 8]

        self.weapons['WEP_SRM4_1'] = [W_SRM(4, 'ct')]
        self.weapons['WEP_M_LAS_1'] = [W_M_LAS('rarm')]
        self.weapons['WEP_M_LAS_2'] = [W_M_LAS('rarm')]
        self.weapons['WEP_M_LAS_3'] = [W_M_LAS('larm')]
        self.weapons['WEP_M_LAS_4'] = [W_M_LAS('larm')]

        self.ammo['AM_SRM_1'] = [A_SRM(100)]

        self.equipment['ct'] += ['jump_jet']
        self.equipment['lt'] += 2 * ['jump_jet']
        self.equipment['rt'] += 2 * ['jump_jet'] + ['AM_SRM_1']
        self.equipment['larm'] += ['WEP_M_LAS_3'] + ['WEP_M_LAS_4']
        self.equipment['rarm'] += ['WEP_M_LAS_1'] + ['WEP_M_LAS_2']
        self.equipment['lleg'] += []
        self.equipment['rleg'] += []

        self.init_mech()

   
class M_Valkyrie(Mech):

    def __init__(self, pilot, pilotting, gunnery):
        details = {}
        details['name'] = 'Valkyrie'
        details['code'] = 'VLK-QA'
        details['tonnage'] = 30
        details['year'] = 2787
        details['cost'] = 2205320
        details['tech'] = 'Inner Sphere'
        details['pilot'] = pilot
        super(M_Valkyrie, self).__init__(details, pilotting, gunnery)

        self.symbol = 'VA'

        self.walk = 5
        self.run = 8
        self.jump = 5
        self.heat_sinks = 11

        self.armour['head'] = [9, 3]
        self.armour['ct'] = [16, 7, 4]
        self.armour['lt'] = [10, 5, 2]
        self.armour['rt'] = [10, 5, 2]
        self.armour['larm'] = [10, 6]
        self.armour['rarm'] = [10, 6]
        self.armour['lleg'] = [12, 8]
        self.armour['rleg'] = [12, 8]

        self.weapons['WEP_LRM10_1'] = [W_LRM(10, 'lt')]
        self.weapons['WEP_M_LAS_1'] = [W_M_LAS('rarm')]

        self.ammo['AM_LRM_1'] = [A_LRM(120)]

        self.equipment['ct'] += ['jump_jet'] + ['heat_sink']
        self.equipment['lt'] += 2 * ['heat_sink'] + 2 * ['WEP_LRM10_1']
        self.equipment['rt'] += 2 * ['heat_sink'] + ['AM_LRM_1']
        self.equipment['larm'] += ['low_arm', 'hand']
        self.equipment['rarm'] += ['low_arm'] + ['WEP_M_LAS_1']
        self.equipment['lleg'] += 2 * ['jump_jet']
        self.equipment['rleg'] += 2 * ['jump_jet']

        self.init_mech()

    
class M_Panther(Mech):

    def __init__(self, pilot, pilotting, gunnery):
        details = {}
        details['name'] = 'Panther'
        details['code'] = 'PNT-9R'
        details['tonnage'] = 35
        details['year'] = 2739
        details['cost'] = 2485711
        details['tech'] = 'Inner Sphere'
        details['pilot'] = pilot
        super(M_Panther, self).__init__(details, pilotting, gunnery)

        self.symbol = 'PA'

        self.walk = 4
        self.run = 6
        self.jump = 4
        self.heat_sinks = 18

        # Front, Internal, (Rear)
        self.armour['head'] = [8, 3]
        self.armour['ct'] = [14, 11, 4]
        self.armour['lt'] = [12, 7, 2]
        self.armour['rt'] = [12, 7, 2]
        self.armour['larm'] = [7, 5]
        self.armour['rarm'] = [7, 5]
        self.armour['lleg'] = [12, 7]
        self.armour['rleg'] = [12, 7]

        self.weapons['WEP_PPC_1'] = [W_PPC('rarm')]
        self.weapons['WEP_SRM4_1'] = [W_SRM(4, 'ct')]

        self.ammo['AM_SRM_1'] = [A_SRM(100)]

        self.equipment['ct'] += ['WEP_SRM4_1']
        self.equipment['lt'] += 4 * ['heat_sink'] + ['AM_SRM_1']
        self.equipment['rt'] += 4 * ['heat_sink']
        self.equipment['larm'] += ['low_arm', 'hand']
        self.equipment['rarm'] += ['low_arm', 'hand'] + 3 * ['WEP_PPC_1']
        self.equipment['lleg'] += 2 * ['jump_jet']
        self.equipment['rleg'] += 2 * ['jump_jet']

        self.init_mech()

    
class M_Spider(Mech):

    def __init__(self, pilot, pilotting, gunnery):
        details = {}
        details['name'] = 'Spider'
        details['code'] = 'SDR-5V'
        details['tonnage'] = 30
        details['year'] = 2650
        details['cost'] = 2984540
        details['tech'] = 'Inner Sphere'
        details['pilot'] = pilot
        super(M_Spider, self).__init__(details, pilotting, gunnery)

        self.symbol = 'SP'

        self.walk = 8
        self.run = 12
        self.jump = 8
        self.heat_sinks = 10

        self.armour['head'] = [6, 3]
        self.armour['ct'] = [8, 10, 4]
        self.armour['lt'] = [6, 7, 2]
        self.armour['rt'] = [6, 7, 2]
        self.armour['larm'] = [5, 5]
        self.armour['rarm'] = [5, 5]
        self.armour['lleg'] = [6, 7]
        self.armour['rleg'] = [6, 7]

        self.weapons['WEP_M_LAS_1'] = [W_M_LAS('ct')]
        self.weapons['WEP_M_LAS_2'] = [W_M_LAS('ct')]

        self.equipment['ct'] +=  ['WEP_M_LAS_1', 'WEP_M_LAS_2']
        self.equipment['lt'] += 4 * ['jump_jet']
        self.equipment['rt'] += 4 * ['jump_jet']
        self.equipment['larm'] += ['low_arm', 'hand']
        self.equipment['rarm'] += ['low_arm', 'hand']

        self.init_mech()

