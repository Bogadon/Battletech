
#import msvcrt
import copy
from random import randint

import player
import ai
import mapgrid
import mech_types
import btlib


print '\n- - - - - - -\nWelcome to the Rats in the Walls AI Battletech Simulator!\n- - - - - -\n'

World = mapgrid.Map(15,15)

Pan = mech_types.M_Panther('Callington', randint(3,5), randint(3,5))
#Pan.location = [0,0]
Spid = mech_types.M_Spider('Hemingway', randint(3,5), randint(3,5))
#Spid.location = [10,10]
Valk = mech_types.M_Valkyrie('Syd', randint(3,5), randint(3,5))
Jen = mech_types.M_Jenner('Jayne', randint(3,5), randint(3,5))
#Valk.location = [12,14]

#World.grid[0][0] = Pan.symbol
#World.grid[10][10] = Spid.symbol

dispositions = ['reckless', 'aggressive', 'neutral', 'defensive', 'cowardly']
disp = dispositions[randint(0,4)]

selection = [Pan, Spid, Valk, Jen]

# Bethany is a human player, but Shodan is an evil AI!
Alpha = player.Player('Bethany', [selection.pop(randint(0, len(selection) - 1))])
Beta = ai.AI_Player('Shodan', [selection.pop(randint(0, len(selection) - 1))], disp)
    
# Position units:
for Unit in Alpha.units_live:
    x, y = randint(0,14), randint(0, 5)
    Unit.location = [x, y]
    World.grid[x][y] = Unit.symbol

for Unit in Beta.units_live:
    x, y = randint(0,14), randint(10, 14)
    Unit.location = [x, y]
    World.grid[x][y] = Unit.symbol

def initiative_phase():
    # In curr imp, AI always wins the init
    Alpha.initiative = 0
    Beta.initiative = 99
    
    '''
    Alpha.gen_init()
    Beta.gen_init()
    while Alpha.initiative == Beta.initiative:
        Alpha.gen_init()
        Beta.gen_init()
    '''
    # Find number of mech moves each player has
    a = ['a'] * len(Alpha.units_active)
    b = ['b'] * len(Beta.units_active)
    # If no one has any active mechs, no moves
    if len(a) == 0 and len(b) == 0:
        return 0
    # If one player has no active mechs, only other has moves
    elif len(a) == 0 or len(b) == 0:
        move_seq = a + b
    else:
        if Alpha.initiative > Beta.initiative:
            move_seq = calc_moves(a, b)
            print 'Player %s wins initiative' %Alpha.name
        else: 
            move_seq = calc_moves(b, a)
            print 'Player %s wins initiative' %Beta.name

    return move_seq

# Find order of player mech moves
def calc_moves(first, second):
    moves = second
    moves.append(first)
    return moves

    # Rest cut from this AI implementation
    moves = [second.pop(0)]
    last = first.pop(0)
    while len(first) > 0 or len(second) > 0:
        if len(first) == 0 or len(second) == 0:
            moves += first + second
        else:
            for x in range(len(second) / len(first)):
                moves.append(second.pop(0))
            moves.append(first.pop(0))
    
    moves.append(last)
    return moves

def mech_choice(_Player, options):
    #print 'Player %s' %_Player.name
    x = 1
    if _Player.is_ai is True:
        choice = 0
        print 'AI chooses ', options[choice].details['name']
        return 0

    print 'Choose available mech: '
    choice = -1
    for mech in options:
        print '%d) %s\tPilot: %s' %(x, options[x-1].details['name'], 
                                    options[x-1].details['pilot'])
    valid = False
    while not valid:
        choice = raw_input()
        print choice
        try:
            choice = int(choice)
            if choice < 1 or choice > len(options):
                print 'Input %d outside of range' %choice
            else:
                valid = True
                choice -= 1 # python indexing
        except ValueError:
            print 'Input must be number'

    return choice


def move_phase(seq):
    print '- - - - - - - -\nMovement Phase\n- - - - - - - -'
    a_moves = Alpha.get_units_active() #copy.deepcopy(Alpha.units_active)
    b_moves = Beta.get_units_active() #copy.deepcopy(Beta.units_active)
    ai_move = False
    for m in seq:
        World.print_map()
        if m == 'a':
            print 'Player %s move\n- - - -' %Alpha.name
            mech = a_moves.pop(mech_choice(Alpha, a_moves))
            #print mech, Alpha.units_active
            #mech = Alpha.units_active[Alpha.units_active.index(mech)]
            enemies = Beta.units_live
            #mv = Alpha
            #mechs = a_moves
        else:
            print 'AI %s calculating moves\n- - - -' %Beta.name
            Beta.get_turn(Alpha, World)
            ai_move = True
            mech = b_moves.pop(mech_choice(Beta, b_moves))
            #mech = Alpha.units_active[Alpha.units_active.index(mech)]
            enemies = Alpha.units_live
            #mv = Beta
            #mechs = b_moves
        '''
        print 'Player %s' %mv.name
        x = 1
        print 'Choose available mech: '
        choice = -1
        for mech in mechs:
            print '%d) %s\tPilot: %s' %(x, mechs[x-1].details['name'], 
                                        mechs[x-1].details['pilot'])
        valid = False
        while not valid:
            choice = raw_input()
            print choice
            try:
                choice = int(choice)
            except ValueError:
                print 'Input must be number'
            if choice < 1 or choice > len(mechs):
                print 'Input %d outside of range' %choice
            else:
                valid = True
                choice -= 1 # python indexing
        '''
    
        speeds = [mech.turn_walk, mech.turn_run, mech.turn_jump] #np.array([mech.walk, mech.run, mech.jump]) - mech.heat_mod[1]
        valid = False
        m_type = -1
        while not valid:
            print '\n', mech.details['name'], ' location: ', mech.location, ' facing: ', mech.face
            print 'Walk: %d, Run: %d, Jump: %d | Heat: %d' %(speeds[0], speeds[1], speeds[2], mech.heat)
            if ai_move is True:
                #print Beta.my_turn #['moves']
                ai_move_type = Beta.my_turn['moves'][mech].keys()[0]
                m_type = ['stationary', 'walk', 'run', 'jump'].index(ai_move_type)
                if m_type is 0:
                    print "No movement for ", mech.details['name']
            else:
                print '1) Walk \n2) Run \n3) Jump\n0) No Movement'
                m_type = raw_input()
            try:
                m_type = int(m_type) - 1
                if m_type < -1 or m_type > 2:
                    print 'input %d out of range' %m_type
                elif m_type == -1:
                    valid = True
                else:
                    try:
                        if ai_move is True:
                            xy = Beta.my_turn['moves'][mech][ai_move_type]
                            x, y = xy[0], xy[1]
                        else:
                            x, y = raw_input('Enter X, Y move location: ').split(',')
                            x, y = int(x), int(y)
                        if (x + 1, y + 1) > World.shape or x < 0 or y < 0:
                            print ('Location outside of map, X and Y must be in ' + 
                                   'range 0,0 to %d,%d' %(World.shape[0], 
                                                        World.shape[1]))
                        else:
                            dist, angle = World.get_dist(mech.location, [x,y], mech.face, m_type=m_type)
                            if dist > speeds[m_type]:
                                if ai_move is True:
                                    print "Error! AI tried to %d %s %d" %(m_type, ai_move_type, dist)
                                    raise ValueError
                                print 'Distance %d too great' %dist
                            else:
                                # Clear old map space
                                World.grid[mech.location[0]][mech.location[1]] = '<>'
                                if ai_move is True:
                                    print '%s %ss %s to %d, %d' %(Beta.name,
                                     ai_move_type.lower(), mech.details['name'], x, y)
                                mech.location = [x, y]
                                mech.terrain = World.terrain[x][y]
                                # Move mech pos in grid
                                World.grid[x][y] = mech.symbol
                                mech.facing = angle
                                # Calculate hit modifiers and collision
                                collision = None # FIX ME- multi collisions
                                for e in enemies:
                                    if e.location == [x, y]:
                                        collision = e
                                mech.get_move_mods(m_type, dist, collision)
                                valid = True
                    except ValueError:
                        print 'Invalid input, enter integers "X, Y"'
            except ValueError:
                print 'input must be number'

    # Torso twists
    a_moves = Alpha.get_units_active()
    b_moves = Beta.get_units_active()
    print '\n- - - - - - -\nTorso twist phase\n'
    for m in seq:
        if m == 'a':
            ai_move = False
            mech = a_moves.pop(mech_choice(Alpha, a_moves))
            enemies = Beta.units_live
            #mech = Alpha.units_active[Alpha.units_active.index(mech)]
            print 'Player %s move\n- - - -' %Alpha.name
        else:
            ai_move = True
            mech = b_moves.pop(mech_choice(Beta, b_moves))
            enemies = Alpha.units_live
            print 'Player %s move\n- - - -' %Beta.name
        print 'Angles to enemy mechs:'
        for e in enemies:
            ang = World.get_dist(mech.location, e.location, mech.face, 'ang_only')
            print 'Mech: %s, Pilot: %s = %d' %(e.details['name'], e.details['pilot'], ang)

        valid = False
        while not valid:
            print '\n%s is facing %d' %(mech.details['name'], mech.face)
            if ai_move is True:
                facing = ang
            else:
                facing = raw_input('Enter new facing: ')
            try:
                facing = int(facing)
                if facing < 0 or facing > 360:
                    print 'Invalid input, facing must be degrees 0-360'
                else:
                    mech.face = facing
                    valid = True
            except ValueError:
                print 'Invalid input, must be number of degrees'



def shooting_phase(seq):
    print '- - - - - - - -\nShooting Phase\n- - - - - - - -'
    World.print_map()
    a_moves = Alpha.get_units_active()
    b_moves = Beta.get_units_active()
    ai_move = False
    for m in seq:
        if m == 'a':
            ai_move = False
            print '\nPlayer %s move\n- - - -' %Alpha.name
            mech = a_moves.pop(mech_choice(Alpha, a_moves))
            #mech = Alpha.units_active[Alpha.units_active.index(mech)]
            enemies = Beta.units_live
            #mv = Alpha
            #mechs = a_moves
        else:
            ai_move = True
            print '\nPlayer %s move\n- - - -' %Beta.name
            mech = b_moves.pop(mech_choice(Beta, b_moves))
            #mech = Beta.units_active[Beta.units_active.index(mech)]
            enemies = Alpha.units_live
        weps = mech.weapons.keys()
        while len(weps) > 0:
            if ai_move is True:
                #print "this side: ", mech, mech.weapons
                #print "Target: ", Beta.my_turn['shooting'].moves #[mech]['target']
                Target = Beta.my_turn['shooting'].moves[mech]['target']
                #print "%s: %s is targetting %s" %(Beta.name, mech.details['name'], Target.details['name'])
                #Target = enemies[enemies.index(Target)]
            else:
                print '\nChoose Target: '
                for e in range(len(enemies)):
                    print '%d) %s, location: %s' %(e + 1, enemies[e].details['name'], enemies[e].location)
                print '0) End move'
                target = raw_input('Enter target: ')
            try:
                if ai_move is True:
                    target = Target
                else:
                    target = int(target)
                    if target == 0:
                        break
                    target = enemies[target - 1]
                #print "ai_move, mech and target airound 297.. : ", ai_move, mech, target
                dist, ang, hit_ang = World.get_dist(mech.location, target.location, mech.face, target.face)
                if ai_move is False:
                    print '\nDistance: %d, Angle of shot: %d, Angle of hit: %d\n' %(dist, ang, hit_ang)
                for w in range(len(weps)):
                    gun = mech.weapons[weps[w]][0]
                    hit_req = mech.turn_gunnery + gun.range_mod(dist, ang)
                    hit_chance = btlib.hit_chance(hit_req)
                    shots = ''
                    if gun.rof > 1:
                        shots = 'Missiles: %d, ' %gun.rof
                    if ai_move is False:
                        print '%d) %s\nHit Chance: %s Damage:  %d, %sHeat: %d' %(
                           w + 1, gun.name, hit_chance, gun.damage, shots, gun.heat)
                if ai_move is False:
                    print '0) Back'
                if ai_move is True:
                    #print "moves[mech] = ", Beta.my_turn['shooting'].moves[mech].keys()
                    if len(Beta.my_turn['shooting'].moves[mech]['move']['weps']) is 0:
                        break #pass
                    else:
                        Wep = Beta.my_turn['shooting'].moves[mech]['move']['weps'].pop(0)
                        print "%s: firing %s at %s" %(Beta.name, Wep.name, target.details['name'])
                        shoot(mech, Wep, target, hit_req, hit_ang)
                else:
                    choice = int(raw_input('Enter choice: '))
                    if choice == 0:
                        break #pass
                    else:
                        shoot(mech, mech.weapons[weps.pop(choice - 1)][0], target, hit_req, hit_ang)

            except (ValueError, IndexError):
                print 'invalid input, must be number in available range'

def shoot(mech, gun, target, hit_req, hit_ang):
    mech.heat += gun.heat
    roll = btlib.d6(2)
    if roll < hit_req:
        print 'Miss!' 
    else:
        hits = [1]
        if gun.rof > 1:
            hits = [btlib.missile_hits(gun.rof)]
            print '%d missiles on target' %hits[0]
            while hits[0] > 5:
                hits[0] -= 5
                hits.append(5)
        for h in hits:
            loc, side, crit = btlib.shot_location(hit_ang)
            target.damage(loc, gun.damage, side, crit)
            if crit:
                print 'Critical hit to %s!' %btlib.loc_full_name[loc]
            else:
                print 'Hit %s!' %btlib.loc_full_name[loc]

def get_melee_reach(loc, facing):
            reach = [loc]
            if facing <= 90:
                reach.append([loc[0] + 1, loc[1] + 1])
            if 45 <= facing < 135:
                reach.append([loc[0] + 1, loc[1]])
            if 90 <= facing < 180:
                reach.append([loc[0] + 1, loc[1] - 1])
            if 135 <= facing < 225:
                reach.append([loc[0], loc[1] - 1])
            if 180 <= facing < 270:
                reach.append([loc[0] - 1, loc[1] - 1])
            if 225 <= facing < 315:
                reach.append([loc[0] - 1, loc[1]])
            if 270 <= facing < 360:
                reach.append([loc[0] - 1, loc[1] + 1])
            if 315 <= facing or facing < 45:
                reach.append([loc[0], loc[1] + 1])

            return reach

# Finds possible targets for a mech
def get_melee_targets(_Player, Enemy):
        moves = {}
        for unit in _Player.get_units_active:
            moves[unit] = []
            reach = get_melee_reach(unit.location, unit.face)
            for enemy in Enemy.units_live:
                if enemy.location in reach:
                    moves[unit].append(enemy)
        # Remove empty entries
        for mv in moves.keys():
            if len(moves[mv]) == 0:
                del moves[mv]
        
        return moves

def melee_phase(sequence):
    print '- - - - - - - -\nMelee Phase\n- - - - - - - -'
    a_moves = get_melee_targets(Alpha, Beta)
    b_moves = get_melee_targets(Beta, Alpha)

    for m in seq:
        if m == 'a':
            print 'Player %s move\n- - - -' %Alpha.name
            mech = a_moves.pop(mech_choice(Alpha, a_moves))
            enemies = Beta.units_live
        else:
            print 'Player %s move\n- - - -' %Beta.name
            mech = b_moves.pop(mech_choice(Beta, b_moves))
            enemies = Alpha.units_live


def heat_phase():
    print '\nHeat Phase:'
    for _player in Alpha, Beta:
        for mech in _player.units_live:
            mech.heat_phase()
'''
for Plyr in [Alpha, Beta]:
    for Unit in Plyr.units_live:
        Unit.init_turn()
'''

Alpha.gen_status()
Beta.gen_status()

while len(Alpha.units_live) > 0 and len(Beta.units_live) > 0:
    
    raw_input('Press any key to start this turn')

    sequence = initiative_phase()
    move_phase(sequence)
    shooting_phase(sequence)

    heat_phase()
    print '- - - -\n'
    Alpha.gen_status()
    Beta.gen_status()
    #for Plyr in [Alpha, Beta]:
    #    for Unit in Plyr.units_live:
    #        Unit.init_turn()

if len(Alpha.units_live) is 0 and len(Beta.units_live) is 0:
    print '\nDraw!'
elif len(Alpha.units_live) is 0:
        print '\nYou lose! Better luck next time'
elif len(Beta.units_live) is 0:
    print '\nYou win!'


print '\nThanks for playing\n'

'''
while not Pan.destroyed and not Spid.destroyed:
    Pan.init_turn()
    Spid.init_turn()
    sequence = initiative_phase()
    move_phase(sequence)
    shooting_phase(sequence)

    heat_phase()


if Pan.destroyed and Spid.destroyed:
    print '\nDraw!'
elif Pan.destroyed:
    print ' wins!'
else:
    print 'Jimbo wins!'
'''





