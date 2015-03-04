#
# Library of common functions


import random


hit_table = {'centre': ['ct', 'rarm', 'rarm', 'rleg', 'rt', 'ct', 'lt',
                        'lleg', 'larm', 'larm'],
             'left': ['lt', 'lleg', 'larm', 'larm', 'lleg', 'lt', 'ct',
                      'rt', 'rarm', 'rleg'],
             'right': ['rt', 'rleg', 'rarm', 'rarm', 'rleg', 'rt', 'ct', 
                       'lt', 'larm', 'lleg']}

# 11+ is always all
missile_table = {2:  [1, 1, 1, 1, 1,   1, 2, 2, 2], 
                 4:  [1, 2, 2, 2, 2,   3, 3, 3, 3],
                 5:  [1, 2, 2, 3, 3,   3, 3, 4, 4],
                 6:  [2, 2, 3, 3, 4,   4, 4, 5, 5],
                 10: [3, 3, 4, 6, 6,   6, 6, 8, 8],
                 15: [5, 5, 6, 9, 9,   9, 9, 12, 12],
                 20: [6, 6, 9, 12, 12, 12, 12, 16, 16]}

loc_full_name = {'head': 'head', 'ct': 'centre torso', 'lt': 'left torso',
                 'rt': 'right torso', 'larm': 'left arm', 'rarm': 'right arm',
                 'lleg': 'left leg', 'rleg': 'right leg'}

def d6(x):
    val = 0
    for d in range(x):
        val += random.randint(1,6)
    return val

def powerset(elements):
    if len(elements) > 0:
        head = elements[0]
        for tail in powerset(elements[1:]):
           yield [head] + tail
           yield tail
    else:
        yield []

def get_subset(full_set):
    ret = powerset(full_set)
    #ret.pop(ret.index([]))

    return ret

# return probability of scoring a hit via 2d6 roll
def hit_chance(x, ai=False):
    prob = []
    chance = 0
    for n in range(1,7):
        for m in range(1,7):
            prob.append(n + m)
    for a in range(x, 13):
        chance += prob.count(a) / 36.
    
    if ai is True:
        # 0 - 1.0
        return chance
    else:
        # percentage without decimal point
        chance = int(chance * 100 + 0.5)
        return str(chance) + '%'

def shutdown_chance(heat):
    if heat < 14:
        return 0
    # 4+
    if heat < 18:
        return 8.33
    # 6+
    if heat < 22:
        return 27.77
    # 8+
    if heat < 26:
        return 58.33
    # 10+
    if heat < 30:
        return 83.33
    # 30+ heat
    return 100


def shot_location(ang):
    roll = d6(2)
    critical = False
    # Critical hit
    if roll == 2:
        critical = True
    if roll == 12:
        return 'head', 0, critical
    if (90 <= ang < 150):
        side = 'right'
    elif (210 <= ang < 270):
        side = 'left'
    else:
        side = 'centre'
    loc = hit_table[side][roll - 2]
    # Rear torso hit
    if loc in ['ct', 'lt', 'rt'] and (150 <= ang < 210):
        return loc, 2, critical
    else:
        return loc, 0, critical

def missile_hits(num):
    roll = d6(2)
    if roll > 10:
        return num
    else:
        return missile_table[num][roll - 2]
        

    
