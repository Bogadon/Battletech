
#import msvcrt
#import copy

import player
import mapgrid
import mech_types
import btlib


print '\n- - - - - - -\nWelcome to Battletech\n- - - - - -\n'

world = mapgrid.Map(15,15)

Pan = mech_types.M_Panther('Callington', 4, 5)
Pan.location = [0,0]
Spid = mech_types.M_Spider('Hemingway', 5, 4)
Spid.location = [10,10]

world.grid[0][0] = Pan.symbol
world.grid[10][10] = Spid.symbol

Alpha = player.Player('Jimbo', [Pan])
Beta = player.Player('Bogadon', [Spid])
    


def initiative_phase():
    Alpha.gen_init()
    Beta.gen_init()
    while Alpha.initiative == Beta.initiative:
        Alpha.gen_init()
        Beta.gen_init()
    Alpha.gen_status()
    Beta.gen_status()
    # Find number of mech moves each player has
    a = ['a'] * len(Alpha.units_live)
    b = ['b'] * len(Beta.units_live)
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
    moves = [second.pop(0)]
    last = first.pop(0)
    while len(first) > 0 or len(second) > 0:
        if len(first) == 0 or len(second) == 0:
            moves += a + b
        else:
            for x in range(len(second) / len(first)):
                moves.append(second.pop(0))
            moves.append(first.pop(0))
    
    moves.append(last)
    return moves

def mech_choice(_Player, options):
    print 'Player %s' %_Player.name
    x = 1
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
    for m in seq:
        world.print_map()
        if m == 'a':
            print 'Player %s move\n- - - -' %Alpha.name
            mech = a_moves.pop(mech_choice(Alpha, a_moves))
            print mech, Alpha.units_active
            #mech = Alpha.units_active[Alpha.units_active.index(mech)]
            enemies = Beta.units_live
            #mv = Alpha
            #mechs = a_moves
        else:
            print 'Player %s move\n- - - -' %Beta.name
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
    
        speeds = mech.speeds #np.array([mech.walk, mech.run, mech.jump]) - mech.heat_mod[1]
        valid = False
        m_type = -1
        while not valid:
            print '\n', mech.details['name'], ' location: ', mech.location, ' facing: ', mech.face
            print 'Walk: %d, Run: %d, Jump: %d | Heat: %d' %(speeds[0], speeds[1], speeds[2], mech.heat)
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
                        x, y = raw_input('Enter X, Y move location: ').split(',')
                        x, y = int(x), int(y)
                        if (x + 1, y + 1) > world.shape or x < 0 or y < 0:
                            print ('Location outside of map, X and Y must be in ' + 
                                   'range 0,0 to %d,%d' %(world.shape[0], 
                                                        world.shape[1]))
                        else:
                            dist, angle = world.get_dist(mech.location, [x,y], mech.face, m_type=m_type)
                            if dist > speeds[m_type]:
                                print 'Distance %d too great' %dist
                            else:
                                # Clear old map space
                                world.grid[mech.location[0]][mech.location[1]] = '<>'
                                mech.location = [x, y]
                                mech.terrain = world.terrain[x][y]
                                # Move mech pos in grid
                                world.grid[x][y] = mech.symbol
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
            mech = a_moves.pop(mech_choice(Alpha, a_moves))
            enemies = Beta.units_live
            #mech = Alpha.units_active[Alpha.units_active.index(mech)]
            print 'Player %s move\n- - - -' %Alpha.name
        else:
            mech = b_moves.pop(mech_choice(Beta, b_moves))
            enemies = Alpha.units_live
            #mech = Beta.units_active[Beta.units_active.index(mech)]
            print 'Player %s move\n- - - -' %Beta.name
        print 'Angles to enemy mechs:'
        for e in enemies:
            ang = world.get_dist(mech.location, e.location, mech.face, 'ang_only')
            print 'Mech: %s, Pilot: %s = %d' %(e.details['name'], e.details['pilot'], ang)

        valid = False
        while not valid:
            print '\n%s is facing %d' %(mech.details['name'], mech.face)
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
    a_moves = Alpha.get_units_active()
    b_moves = Beta.get_units_active()
    for m in seq:
        world.print_map()
        if m == 'a':
            print 'Player %s move\n- - - -' %Alpha.name
            mech = a_moves.pop(mech_choice(Alpha, a_moves))
            #mech = Alpha.units_active[Alpha.units_active.index(mech)]
            enemies = Beta.units_live
            #mv = Alpha
            #mechs = a_moves
        else:
            print 'Player %s move\n- - - -' %Beta.name
            mech = b_moves.pop(mech_choice(Beta, b_moves))
            #mech = Beta.units_active[Beta.units_active.index(mech)]
            enemies = Alpha.units_live
        weps = mech.weapons.keys()
        while len(weps) > 0:
            print 'Choose Target: '
            for e in range(len(enemies)):
                print '%d) %s, location: %s' %(e + 1, enemies[e].details['name'], enemies[e].location)
            print '0) End move'
            target = raw_input('Enter target: ')
            try:
                target = int(target)
                if target == 0:
                    break
                target = enemies[target - 1]
                dist, ang, hit_ang = world.get_dist(mech.location, target.location, mech.face, target.face)
                print '\nDistance: %d, Angle of shot: %d, Angle of hit: %d\n' %(dist, ang, hit_ang)
                for w in range(len(weps)):
                    gun = mech.weapons[weps[w]][0]
                    hit_req = mech.turn_gunnery + gun.range_mod(dist, ang)
                    hit_chance = btlib.hit_chance(hit_req)
                    shots = ''
                    if gun.rof > 1:
                        shots = 'Missiles: %d, ' %gun.rof
                    print '%d) %s\nHit Chance: %s Damage:  %d, %sHeat: %d' %(
                     w + 1, gun.name, hit_chance, gun.damage, shots, gun.heat)
                print '0) Back'
                choice = int(raw_input('Enter choice: '))
                if choice == 0:
                    pass
                else:
                    shoot(mech, mech.weapons[weps.pop(choice - 1)][0], target, hit_req, hit_ang)

            except (ValueError, IndexError):
                print 'invalid input, must be number in available range'

def shoot(mech, gun, target, hit_req, hit_ang):
    mech.heat += gun.heat
    if btlib.d6(2) < hit_req:
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
    for _player in Alpha, Beta:
        for mech in _player.units_live:
            mech.heat_phase()

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
    print 'Bogadon wins!'
else:
    print 'Jimbo wins!'






