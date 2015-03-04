# AI Classes

'''
 Initiative: Either I win or I lose, if I win I go second, so I know my
  opponents moves already- otherwise I have to try and predict them
 Move Phase: Number of possible moves per unit depends on speeds and 
  world mechanics. It can easily be 100+ per unit. If we lost the 
  initiative then we need to try and predict the opponents moves first
  as well. 
 Shoot Phase: Given disposition we can logically pick the best move given
  the previous phase. This approach makes sense, but having a fixed 
  disposition at all times does not. If a mech will be destroyed we always
  pick the reckless move, which is start, but more conditions should be
  checked to adjust dispositions for better results. If we are able to run
  turns with enough processing power we can calculate the best
  disposition by doing every one and every turn thereafter


 Dispositions
 Reckless: Ignores Heat, always maximises damage dealt but still favours
           moves with less damage taken
 Aggressive: Aims for dealt/taken ratio 1:2 with shutdown < 30%, avg dam > 2 above
 Neutral: Aims for dealt/taken ratio 1:1 with shutdown < 30%, avg dam > 4 above
 Defensive: Aims for ratio 2:1 with shutdown < 30%, never shoots above
 Cowardly: Never shoots with shutdown > 0%, reverse of reckless

'''

import pickle
from copy import deepcopy 
from random import randint

from player import *
import btlib

# Consider not using a global
global m_types
m_types = ['stationary', 'walk', 'run', 'jump']

# Incomplete
'''
class AI_Calc_Instance(AI_Player):

    def __init__(self, parent, order, turns, game_data):
        self.parent = parent
        self.order = order
        name = parent + '-child-' + str(order)
        super( AI_Calc_Instance, self ).__init__( name, game_data['mechs'], 
               game_data['disposition'], game_data['World'], 
               game_data['MAX_TURN_CALCS'] )
        self.name = name
        self.infer_opponent = game_data['infer']
        self.memory = game_data['memory']
        #self.best_move = calc_turns( turns, 

    def calc_turns(self, move_list, enemy_units):
        # Finds the best move for each specified disposition
        best_move = {}
        for disposition in self.all_disps:
            best_move[disposition]['moves'] = None
            best_move[disposition]['score'] = None

        while len(move_list) > 0:
            # Remove move set from list
            this_move = move_list.pop(0)
            for disp in self.all_disps:
                # Calc expected result from my and opponents shoot phase
                My_Shots, Her_Shots = self.get_shoot_phase( this_move, 
                                                    enemy_units, disp )
                # Evaluate success based on seperate function
                this_score = self.evaluate_turn(My_Shots, Her_Shots)
                # Note: currently we only store 1 turn
                if this_score > best_move[disp]['score']:
                    best_move[disp]['moves'] = this_move
                    best_move[disp]['score'] = this_score
'''


# Memory is list of previous turns contained in dicts:
# { 'dmg_dealt': int, 'dmg_taken': int, 'opponent heats': [int, int..] }
# infer_opponent is the disposition prediction based on memory
class AI_Player(Player):

    def __init__(self, name, mechs, disposition): #, World, MAX_TURN_CALCS):
        super(AI_Player, self).__init__(name, mechs)
        unique_id = 0
        self.unique_ids = {}
        for unit in self.units_live:
            unit.unique_id = unique_id
            self.unique_ids[unique_id] = unit
            unique_id += 1
        self.is_ai = True
        self.disposition = disposition
        self.all_disps = [ 'reckless', 'aggressive', 'neutral', 'defensive',
                           'cowardly' ]
        self.World = None
        self.infer_opponent = 'neutral'
        self.memory = []
        self._all_turn_movements = []
        self.my_turn = None


        # Per Instance
        #self.MAX_TURN_CALCS = MAX_TURN_CALC
        #self.filename = 'ai-' + name

    def get_turn(self, Opponent, World):
        self.World = World
        Move_Phase = AI_Move_Phase( self.units_live, Opponent.units_live, World )
        poss_moves = Move_Phase.moves
        move_list = self.get_all_moves_as_list(poss_moves)
        # This is a huge list of all possible unique moves for entire 
        # set of units. List of lists of dicts {move info}
        self._all_turn_movements = [] # clear some place else
        self.recurse_get_moves( [], move_list )
        
        turn_calcs = 0
        best_move = self.calc_turns(self._all_turn_movements, Opponent.units_live)
        # Dynamic disposition not yet implemented
        self.my_turn = best_move[self.disposition]
        self.my_turn['moves'] = self.my_turn['moves'][0]
        # Shooting uses duplicates for calcing, we need to remap
        '''
        print self.my_turn
        for Unit in self.my_turn['moves'].keys():
            for Unique in self.units_live:
                if Unit.ai_id == Unique.ai_id:
                    self.my_turn['moves'][Unique] = ( 
                                   self.my_turn['moves'].pop(Unit) )
        '''
        '''
        while len(self._all_turn_movements) > MAX_TURN_CALCS:

        while ( len(self._all_turn_movements) > 0 and 
                turn_calcs < self.MAX_TURN_CALCS ):

            turn_calcs += 1
            # choose any random turn option left in list
            choice = randint( 0, len(self._all_turn_movements) - 1 )
            moves = move_list.pop(choice)

            My_Shoot_Phase, Opponent_Shoot_Phase = get_shoot_phase()
        '''
        

    def calc_turns(self, move_list, enemy_units):
        # Finds the best move for each specified disposition
        best_move = {}
        for disposition in self.all_disps:
            best_move[disposition] = {}
            best_move[disposition]['moves'] = None
            best_move[disposition]['score'] = None

        while len(move_list) > 0:
            # Remove move set from list
            this_move = move_list.pop(0)
            for disp in self.all_disps:
                # Calc expected result from my and opponents shoot phase
                My_Shots, Her_Shots = self.get_shoot_phase( this_move, 
                                                    enemy_units, disp )
                # Evaluate success based on seperate function
                this_score = self.evaluate_turn(My_Shots, Her_Shots)
                # Note: currently we only store 1 turn
                if this_score > best_move[disp]['score']:
                    best_move[disp]['moves'] = this_move
                    best_move[disp]['score'] = this_score
                    best_move[disp]['shooting'] = My_Shots

        return best_move

    # This function is currently entirely rudimentary, but is a placeholder
    # for future development. The turn_score is the returned rating.
    def evaluate_turn(self, My_Shoot_Phase, Opponent_Shoot_Phase):
        net_damage = ( My_Shoot_Phase.total_dam_dealt - 
                       Opponent_Shoot_Phase.total_dam_dealt )

        turn_score = net_damage

        return turn_score

    # moves is a 1-entry list of dicts of single unit positions
    def get_shoot_phase(self, moves, enemy_units, disposition):
        my_units = [] #deepcopy(self.units_live)
        # the keys are objects, this may cause you problems- look at hashing


        #if len(moves) != 1:
        #    print "Error! bad move type for unit: ", moves
        #    raise ValueError
        # Only 1 entry now, from previous giant list
        moves = moves[0]
        for unit in moves.keys():
            # Error Check
            m_type = moves[unit].keys()[0]
            #if len(moves[unit][m_type]) != 1:
            #    print "Error! bad move coord for unit: ", moves[unit][m_type]
            #    raise ValueError
            new_loc = moves[unit][m_type] #[0]
            # Hopefully this is the obj, hence caps
            This_Unit = deepcopy(unit) #my_units[unit]
            # Note: calcing dist again here is repetition. Fix sometime.
            dist, ang = self.World.get_dist( This_Unit.location, new_loc, 
                                             This_Unit.face )
            This_Unit.location = new_loc
            # This adjusts the unit's status (heat/accuracy/defense..)
            This_Unit.get_move_mods(m_type, dist)
            my_units.append(This_Unit)

        My_Shoot_Phase = AI_Shoot_Phase( self, my_units, enemy_units, 
                                         disposition )
        Opponent_Shoot_Phase = AI_Shoot_Phase( None, enemy_units, my_units, 
                                               self.infer_opponent )

        return My_Shoot_Phase, Opponent_Shoot_Phase




    def get_all_moves_as_list(self, moves):
        #m_types = ['stationary', 'walk', 'run', 'jump']
        all_ind_moves = {}
        for unit in moves.keys():
            all_ind_moves[unit] = []
            for m_type in m_types:
                for m in range(len(moves[unit][m_type])):
                    all_ind_moves[unit].append(
                                         {m_type: moves[unit][m_type][m]} )

        return all_ind_moves

    def recurse_get_moves(self, curr_move, move_list):
        # Recursion Escape when no more units to check
        if len(move_list.keys()) is 0:
            self._all_turn_movements.append(curr_move)
            return

        # You should stop redefining th
        #m_types = ['stationary', 'walk', 'run', 'jump']
        unit = move_list.keys()[0]
        unit_moves = move_list[unit]
        del move_list[unit]
        for move in unit_moves:

            this_move = deepcopy(curr_move)
            this_move.append({unit: move})
            self.recurse_get_moves(this_move, move_list)


    





# Contains all valid move phases for a set of mechs against an opponent
# Moves = dict of dicts of lists: Mech -> Move types -> coords
# { Mech: { 'stationary': [x,y], 'walk'/'run'/'jump': [[x,y], [x,y]..] } }
class AI_Move_Phase:

    def __init__(self, units, enemy_units, World):
        self.moves = {}
        for Unit in units:
            self.moves[Unit] = self.find_moves(Unit, enemy_units, World)


    # Unit is some mech of mine, enemy is theirs, World is the map
    # Returns all valid moves for unit in a dict
    def find_moves(self, Unit, enemy_units, World):
        stationary = [Unit.location]
        walk_moves = []
        run_moves = []
        jump_moves = []
        # find limit of x/y unit movement on map 
        min_x = Unit.location[0] - Unit.turn_run
        max_x = Unit.location[0] + Unit.turn_run
        min_y = Unit.location[1] - Unit.turn_run
        max_y = Unit.location[1] + Unit.turn_run
        if min_x < 0:
            min_x = 0
        if max_x >= World.len_x:
            max_x = World.len_x - 1
        if min_y < 0:
            min_y = 0
        if max_y >= World.len_y:
            max_y = World.len_y - 1

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                # find distance according to world, and whether this is 
                # possible via walking or running
                dist, ang = World.get_dist(Unit.location, [x,y], Unit.face)
                if dist <= Unit.turn_walk:
                    walk_moves.append([x,y])
                elif dist <= Unit.turn_run:
                    run_moves.append([x,y])
                # Some mechs can jump, which has alternate game mechanics
                if Unit.jump > 0:
                    jump_dist, ang = World.get_dist( Unit.location, [x,y], 
                                                Unit.face, None, 2 )
                    if jump_dist <= Unit.turn_jump:
                        jump_moves.append([x,y])

        return { 'stationary': stationary, 'walk': walk_moves, 
                 'run': run_moves, 'jump': jump_moves }

# Contains best shoot phase for a player based on disposition
class AI_Shoot_Phase:
    
    
    def __init__(self, Turn_Player, My_Units, enemy_units, disposition):
        self.enemy_units = enemy_units
        #self.best_move = {'move': 0, 'use_weps': [], 'heat': 0, 'dmg_dealt': 0, 'dmg_taken': 0}
        self.disposition = disposition
        self.moves = {}
        self.total_dam_dealt = 0
        self.Turn_Player = Turn_Player

        # Disposition setup
        if disposition is 'reckless':
            self._sd_thresh = 100
            self._min_dam = 0
            self._dam_ratio = 0
        elif disposition is 'aggressive':
            self._sd_thresh = 30
            self._min_dam = 3
            self._dam_ratio = 0.5
        elif disposition is 'neutral':
            self._sd_thresh = 30
            self._min_dam = 6
            self._dam_ratio = 1
        elif disposition is 'defensive':
            self._sd_thresh = 10
            self._min_dam = 6
            self._dam_ratio = 2
        elif disposition is 'cowardly':
            self._sd_thresh = 0
            self._min_dam = 0
            self._dam_ratio = 0
        else:
            print "Error! AI init with invalid disposition: ", disposition
            raise ValueError
        
        # Setup the moves
        for Unit in My_Units:
            # Map mech copies to uniques if this is our turn not prediction
            if Turn_Player is not None:
                Mapped_Unit = Turn_Player.unique_ids[Unit.unique_id]
                #self.moves[Turn_Player.unique_ids[Unit.unique_id]] = self.find_move(Unit)
            else:
                Mapped_Unit = Unit

            self.moves[Mapped_Unit] = self.find_move(Unit)
                
            self.total_dam_dealt += self.moves[Mapped_Unit]['move']['damage']

        

    # finds the best move for a unit against all possible targets
    # returns a list of dicts
    def find_move(self, Unit):
        targets = []
        for Target in self.enemy_units:
            move = self._pick_weapon_choice(Unit, Target)
            targets.append({'target': Target, 'move': move})
        # At some point other factors should be added
        best_move = targets.pop(0)
        while len(targets) > 0:
            this_move = targets.pop(0)
            if this_move['move']['damage'] > best_move['move']['damage']:
                best_move = this_move
        
        return best_move

        
    
    # Unit = MyMech, Target = Enemy Mech, returns avg dam as float
    def _calc_average_damage(self, Unit, Target, Weapon):
        #Unit = self.My_Unit
        avg_dmg = 0
        #angle = 0 # not implemented???
        dist, ang = Unit.get_dist(Target.location, Unit.face)
        hit_difficulty = Unit.turn_gunnery + Weapon.range_mod(dist, ang)
        hit_chance = btlib.hit_chance(hit_difficulty, True)
        avg_dmg += Weapon.damage * hit_chance

        return avg_dmg

    # Returns a list of dictionaries containing all uniquely viable weapon
    # choices. The mech status and AI disposition will decide on which later
    def _calc_weapon_choices(self, Unit, Target):
        #Unit = self.My_Unit
        unit_heat = Unit.heat
        poss_weps = []
        poss_combos = []
        weps = Unit.weapons.keys()
        # find all weapons with potential damage
        for w in weps:
            #weapon = Unit.weapons[weps[w]][0]
            #Weapon = Unit.weapons[w][0]
            if self.Turn_Player is not None:
                Unique = self.Turn_Player.unique_ids[Unit.unique_id]
                Weapon = Unique.weapons[w][0]
            else:
                Weapon = Unit.weapons[w][0]
            avg_dmg = self._calc_average_damage( Unit, Target, Weapon )
            if avg_dmg > 0:
                poss_weps.append(Weapon)
        
        poss_combos = btlib.get_subset(poss_weps)
        scored_combos = []
        for poss in poss_combos:
            combo = {'weps': poss, 'heat': 0, 'damage': 0}
            combo['heat'] += unit_heat
            for wep in poss:
                combo['heat'] += wep.heat
                combo['damage'] += wep.damage
            scored_combos.append(combo)
        
        remove = []

        # Check each entry against remaining entries, remove any wholly 
        # or duplicate options
        for choice in range(len(scored_combos)):
            this = scored_combos[choice]
            # We remove irrelevant other entries- self and preremoved
            others = range(len(scored_combos))
            others.pop(others.index(choice))
            # Compare value
            for compare in others:
                if compare not in remove:
                    that = scored_combos[compare]
                    if ( this['damage'] <= that['damage'] and 
                        this['heat'] >= that['heat'] ):
                        remove.append(choice)
                #for rem in remove:
                #    others.pop(others.index(rem))
                #    remove.pop(remove.index(rem))
        # Now we clear out the bad choices from list
        #for rem in remove:
        #    scored_combos.pop(scored_combos.index(rem))
        
        best_combos = []
        for combo in scored_combos:
            if scored_combos.index(combo) not in remove:
                best_combos.append(combo)

        return best_combos

    # Decide which weapon combo is best choice based on status/disposition
    # and predicted damage taken from opponent
    def _pick_weapon_choice(self, Unit, Target):
        
        #Unit = self.My_Unit
        choices = self._calc_weapon_choices( Unit, Target )
        choice = {'weps': [], 'heat': 0, 'damage': 0}
        for option in choices:
            if option['damage'] > choice['damage']:
                # Damage is applied at end of turn- hence a unit that will
                # be destroyed has nothing to lose by firing everything
                if self.disposition is 'reckless' or Unit.destroyed is True:
                    choice = option
                # If shutdown chance is over disposition threshold, pass
                elif ( btlib.shutdown_chance(option['heat']) > self._sd_thresh 
                       and option['damage'] < self._min_dam ):
                    pass
                else:
                    choice = option

        return choice
        

        



    
