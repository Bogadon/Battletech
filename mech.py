#
# Battletech mech superclass
#
# Written by John Kazimierz Farey October 2012
#

'''
armour: val 0 = front external, val 1 = internal, (val 2 = rear external)

health: number of hits the pilot for knock out modifier/death

equipment: weapons/ammo are objects, others are strings

weapons/ammo: dict of objects, locations and position(s): eg 'PPC_1': [PPC_1, 'rarm', 1, 2, 3]


NOTES: hip hits need to cause pilot checks for run/jump

'''

from random import randint
import math

import numpy as np

import btlib
d6 = btlib.d6

class Mech(object):

    def __init__(self, details, pilotting, gunnery):
        # unique used if making copies of mech for ai
        self.unique_id = None
        self.details = details
        #{'name': name, 'pilot': pilot, 'tonnage': 0, 
        #                'cost': 0, 'tech': 'Inner Sphere', 'year': 1969}

        self.location = [0, 0] # x, y
        self.symbol = '!!'
        self.face = 0 # 0-360
        self.terrain = ''
        self.defence = 0
        self.turn_gunnery = 0
        self.turn_pilotting = 0

        self.collision = None
        self.col_type = None

        self.armour = {'head': [0,0], 'ct': [0,0,0], 'lt': [0,0,0],
                       'rt': [0,0,0], 'larm': [0,0], 'rarm': [0,0],
                       'lleg': [0,0], 'rleg': [0,0]}
        self.equipment = {'head': ['life_support', 'sensors', 'cockpit', 
                                   'sensors', 'life_support'],
                          'ct' : ['engine', 'engine', 'engine', 'gyro', 
                                   'gyro', 'gyro', 'gyro', 'engine', 
                                   'engine', 'engine'],
                          'lt': [],
                          'rt': [],
                          'larm': ['shoulder', 'up_arm'],
                          'rarm': ['shoulder', 'up_arm'],
                          'lleg': ['hip', 'up_leg', 'low_leg', 'foot'],
                          'rleg': ['hip', 'up_leg', 'low_leg', 'foot']}
        self.weapons = {}
        self.ammo = {}
        self.cased = [] # eg ['rt', 'lt']
        # Modifiers for actuator damage, shooting/melee
        self.limb_mod = {'larm': [0,0], 'rarm': [0,0], 'lleg': 0, 'rleg': 0}

        self.walk = 0
        self.run = 0
        self.jump = 0
        self.jump_check = False # pilotting roll requirement
       
        self.heat_sinks = 0
        self.heat = 0
        self.heat_mod = [0,0] # shooting / move speed
        self.shutdown = False

        self.pilotting = pilotting
        self.gunnery = gunnery
        self.health = 6 # how dead pilot is
        self.conscious = True

        self.engine = 3
        self.gyro = 2
        self.sensors = 2
        self.life_support = True
        self.hips = 2
        self.legs = 2
        self.destroyed = False

        # Per turn variables
        self.turn_walk = self.walk - self.heat_mod[1]
        self.turn_run = self.run - self.heat_mod[1]
        self.turn_jump = self.jump - self.heat_mod[1]
        self.defense = 0
        self.turn_gunnery = self.gunnery + self.heat_mod[0]
        self.turn_pilotting = self.pilotting
        self.collision = None
        self.col_type = None


    
    def init_mech(self):
        for loc in self.equipment.keys():
            for x in range(len(self.equipment[loc])):
                item = self.equipment[loc][x]
                if item.find('WEP') != -1:
                    self.weapons[item].append([loc, x])
                elif item.find('AM') != -1:
                    self.ammo[item].append([loc, x])
        '''
        self.base_vals = {'walk': self.walk, 'run': self.run, 
                          'jump': self.jump, 'gunnery': self.gunnery,
                          'pilotting': self.pilotting}
        '''
        
    def init_turn(self):
        if self.destroyed:
            return
        print self.details['name'], ' Centre Torso Armour: ', self.armour['ct']
        if not self.conscious:
            self._pilot_hit(0)
        #self.speeds = (np.array([self.walk, self.run, self.jump]) - 
        #                                           self.heat_mod[1])
        self.turn_walk = self.walk - self.heat_mod[1]
        self.turn_run = self.run - self.heat_mod[1]
        self.turn_jump = self.jump - self.heat_mod[1]
        if self.turn_walk < 0:
            self.turn_walk = 0
        if self.turn_run < 0:
            self.turn_run = 0
        if self.turn_jump < 0:
            self.turn_jump = 0
        self.defense = 0
        self.turn_gunnery = self.gunnery + self.heat_mod[0]
        self.turn_pilotting = self.pilotting
        self.collision = None
        self.col_type = None


    # movement -1, 0, 1 or 2 for none, walk, run, jump
    def get_move_mods(self, movement, dist, collision=None):
        # At some point remove the int movement arg option
        move_map = {'stationary': -1, 'walk': 0, 'run': 1, 'jump': 2}
        if type(movement) == str:
            movement = move_map[movement]

        if movement == -1:
            return 0
        self.turn_gunnery += movement + 1
        self.defense = (dist - 1) / 2
        self.heat += movement + 1

        # if collison, set mech and type- Death from above or charge dist
        if collision is not None:
            self.collision = collision
            if movement == 2:
                self.col_type = 'DFA'
            else:
                self.col_type = dist
        


    # FIX ME SQUARE GRID
    # Returns distance and angle of hit on mech
    def get_dist(self, xy, face):
        # adjust opposing mech relation
        #face += 180
        x = self.location[0] - xy[0]
        y = self.location[1] - xy[1]
        offset = 0
        if x < 0 or y < 0:
            x = abs(x)
            y = abs(y)
            offset = 180
        if x == 0 or y == 0:
            dist = x + y
            ang = 360 - self.face
        else:
            # On a square grid we can just pythagarise. Note: rounded down
            dist = int(math.sqrt(pow(x, 2) + pow(y, 2)))
            ang = self.face + math.degrees(math.atan(float(y) / x))
        while ang >= 360:
            ang -= 360
        ang = face - ang + offset
        while ang < 0:
            ang += 360
        while ang >= 360:
            ang -= 360

        return dist, ang





    

    # side: 0 for front, 2 for rear
    # critical arg superfluous
    def damage(self, location, amount, side=0, critical=False):
        # Damage redirection
        if self.armour[location][1] <= 0:
            if location in ['larm', 'lleg']:
                location = 'lt'  
            elif location in ['rarm', 'rleg']:
                location = 'rt'
            else:
                location = 'ct'
            
        # internal redirection
        if self.armour[location][side] <= 0:
            side = 1
        
        # Deal damage
        self.armour[location][side] -= amount

        if side == 1 or critical:
            self._critical(location)
        # if external armour lost transfer to internal
        if (self.armour[location][side] < 0) and (side == 0 or side == 2):
            self.armour[location][1] += self.armour[location][side]
            self._critical(location)

        # If internals destroyed, maim
        if self.armour[location][1] <= 0:
            self._maim(location)

    # Only torso damage transfers
    def _ammo_explosion(self, location, dam):
        print 'Ammo Explosion!'
        self.damage(location, dam, side=1)
        self._pilot_hit(2)
        if location in ['lt', 'rt'] and location not in self.cased:
            self.damage('ct', abs(self.armour[location][1]), side=1)

    # Checks whether hes awake. call with hits = 0 just wake up chance
    # Note: if he falls asleep then gets hit again in same round.. he 
    # might wake back up.. I like this idea
    def _pilot_hit(self, hits):
        print 'Pilot hit!'
        self.health -= hits
        if self.health <= 0:
            print 'Pilot Dead!'
            self.conscious = False
            self.destroyed = True
        elif self.health == 1 and d6(2) < 11:
            self.conscious = False
        elif self.health == 2 and d6(2) < 10:
            self.conscious = False
        elif self.health == 3 and d6(2) < 7:
            self.conscious = False
        elif self.health == 4 and d6(2) < 5:
            self.conscious = False
        elif self.health == 5 and d6(2) < 3:
            self.conscious = False
        else:
            self.conscious = True



    def _critical(self, location):
        num_items = len(self.equipment[location])
        limbs = ['larm', 'rarm', 'lleg', 'rleg', 'head']
        # Check there is something to destroy
        if num_items == 0 and location not in limbs:
            return 0
        roll = d6(2)
        hits = 0
        if roll < 8:
            return 0
        elif roll < 10:
            hits = 1
        elif roll < 12:
            hits = 2
        else:
            if location in limbs:
                self._maim(location)
                return 0
            hits = 3

        for h in range(hits):
            item = randint(0, num_items - 1)
            self._destroy_item(location, item)
            num_items -= 1
            if num_items == 0:
                break

    def _destroy_item(self, location, item):
        # If nothing to destroy, return
        if len(self.equipment[location]) is 0:
            return
        # First remove item from equipment list
        item = self.equipment[location].pop(item)
        print 'Critical hit: ', item 
        # Generic mech parts are strings
        #if isinstance(item, str):
        if item == 'cockpit':
            #self.destroyed = True
            self._pilot_hit(99)
        elif item == 'life_support':
            self.life_support = False
        elif item == 'sensors':
            self._sensor_hit()

        elif item == 'engine':
            self._engine_hit()
        elif item == 'gyro':
            self._gyro_hit()
        elif item == 'heat_sink':
            self.heat_sinks -= 1
        elif item == 'jump_jet':
            self.jump -= 1

        elif item == 'shoulder':
            self.limb_mod[location] = [4, 99]
        elif item in ['up_arm', 'low_arm']:
            if self.limb_mod[location][1] < 99:
                self.limb_mod[location][0] += 1
                self.limb_mod[location][1] += 2
        elif item == 'hand':
            self.limb_mod[location][1] += 1

        elif item == 'hip':
            self._hip_hit()
            self.limb_mod[location] = 99
        elif item in ['up_leg', 'low_leg']:
            self.limb_mod[location] += 2
            self.walk -= 1
            self.run = self.walk + self.walk / 2
            self.pilotting += 1
            self.jump_check = True
        elif item == 'foot':
            self.limb_mod[location] += 1
            self.walk -= 1
            self.run = self.walk + self.walk / 2
            self.pilotting += 1
            self.jump_check = True

        #elif isinstance(item, Ammo):
        elif item.find('AM') != -1: 
            self._ammo_explosion(location, self.ammo[item][0].explode())

        elif item.find('WEP') != -1:
            # if it is a weapon, destroy if not already
            if item in self.weapons.keys():
                self.weapons[item][0].destroyed = True
                self.weapons.pop(item)




    def _hip_hit(self):
        self.hips -= 1
        if self.hips == 1 and self.legs == 2:
            # halved speed rounded up
            self.walk = self.walk / 2 + self.walk % 2
            self.run = self.run / 2 + self.run % 2
            self.pilotting += 2
        elif self.hips == 0:
            self.walk = 0
            self.run = 0
            self.pilotting += 2
        elif self.legs == 1:
            self.walk = 1
            self.run = 1
            self.pilotting += 2

    def _gyro_hit(self):
        #print 'Gyro hit!'
        self.gyro -= 1
        if self.gyro == 0:
            print 'Gyro Destroyed!'
            pass
            # FIX ME- mech falls

    def _engine_hit(self):
        #print 'Engine hit!'
        self.engine -= 1
        #self.heat_sinks -= 5
        if self.engine == 0:
            print 'Engine destroyed!'
            self.destroyed = True

    def _sensor_hit(self):
        self.sensors -= 1
        if self.sensors == 1:
            print 'Sensor hit!'
            self.gunnery += 2
        else:
            print 'Sensors destroyed!'
            self.gunnery = 99

    # Amputate a body section 
    def _maim(self, location):
        if location == 'head':
            #self.destroyed = True
            self._pilot_hit(99)
        elif location == 'ct':
            self.destroyed = True
        elif location == 'lt':
            self._maim('larm')
        elif location == 'rt':
            self._maim('rarm')
        elif location in ['lleg', 'rleg']:
            self.legs -= 1
            # FIX ME- mech falls
        elif location in ['larm', 'rarm']:
            self.limb_mod[location] = [99,99]          

        for item in range(len(self.equipment[location])):
            self._destroy_item(location, 0)
        
        print '%s destroyed!' %btlib.loc_full_name[location]


    def heat_phase(self):
        self.heat -= self.heat_sinks
        # Modifications for water and engine hits
        if self.terrain.find('WATER') != -1:
            self.heat -= heat_sinks
        self.heat += (3 - self.engine) * 5
        if self.heat < 0:
            self.heat = 0
        heat = self.heat

        # Shutdown/Wake check
        if heat >= 30:
            self.shutdown = True
        elif heat >= 26:
            if d6(2) < 10:
                self.shutdown = True
            elif self.shutdown is True:
                print '%s wakes up from shutdown' %self.details['name']
                self.shutdown = False
        elif heat >= 22:
            if d6(2) < 8:
                self.shutdown = True
            elif self.shutdown is True:
                print '%s wakes up from shutdown' %self.details['name']
                self.shutdown = False
        elif heat >= 18:
            if d6(2) < 6:
                self.shutdown = True
            elif self.shutdown is True:
                print '%s wakes up from shutdown' %self.details['name']
                self.shutdown = False
        elif heat >= 14:
            if d6(2) < 4:
                self.shutdown = True
            elif self.shutdown is True:
                print '%s wakes up from shutdown' %self.details['name']
                self.shutdown = False
        elif self.shutdown is True:
            print '%s wakes up from shutdown' %self.details['name']
            self.shutdown = False

        # Gunnery modifier
        if heat >= 24:
            self.heat_mod[0] = 4
        elif heat >= 17:
            self.heat_mod[0] = 3
        elif heat >= 13:
            self.heat_mod[0] = 2
        elif heat >= 8:
            self.heat_mod[0] = 1
        else:
            self.heat_mod[0] = 0

        # Movement speed modifier
        self.heat_mod[1] = heat / 5

        # Ammo explosion if carrying + fail roll
        ammo_exp = False
        if len(self.ammo.keys()) > 0:
            if heat >= 28 and d6(2) < 8:
                ammo_exp = True
            elif heat >= 23 and d6(2) < 6:
                ammo_exp = True
            elif heat >= 19 and d6(2) < 4:
                ammo_exp = True
        if ammo_exp:
            am_keys = self.ammo.keys()
            choice = am_keys[0]
            # If more than 1 ammo, check the remaining for most volatile
            if len(am_keys) > 1:
                #exp = self.ammo[choice]
                dam = self.ammo[choice][0].damage
                #dam = self.equipment[exp[0]][exp[1]].damage
                for n in (range(len(am_keys) - 1) + 1):
                    #n_choice = self.ammo[n]
                    #other = self.equipment[nexp[0]][nexp[1]].damage
                    other = self.ammo[n][0].damage
                    if other > dam:
                        choice = n
                        #exp = nexp
                        dam = other
            
            # Remove from ammo list, and destroy
            #bang = self.ammo.pop(choice)
            print self.details['name'] + ' ' + choice + ' Ammo Explosion!'
            self._destroy_item(self.ammo[choice][1][0], self.ammo[choice][1][1]) #bang[0], bang[1])

        print self.details['name'] + ' heat = ' + str(self.heat)
        if self.shutdown is True:
            print "SHUTDOWN!\n"








