#
# Map 
#

import math

#import numpy as np

class Map:

    def __init__(self, len_x, len_y):
        #self.grid = np.zeros((len_x, len_y), dtype=str)
        self.grid = [['<>' for x in range(len_x)] for y in range(len_y)]
        self.terrain = [[' ' for x in range(len_x)] for y in range(len_y)]
        #print 'length:: %d   %d' % ( len(self.grid),  len(self.grid[0]) )
        self.len_x = len_x
        self.len_y = len_y
        self.shape = (len_x, len_y)
        #self.grid[:][:] = '.'
        #self.base = self.grid.copy()


    # Print the map with padded coords on edges lining up
    def print_map(self):
        print "The map is now:"
        line = '  '
        for x in range(self.len_x):
            line += ' ' + '%02d' % x
        print line

        for y in range(self.len_y):
            print '  ' + ('---' * self.len_x)
            line = '%02d' % y
            for x in range(self.len_x):
                line += '|' + self.grid[x][y]
            line += '|%02d' % y
            print line

        print '  ' + ('---' * self.len_x)
        line = '  '
        for x in range(self.len_x):
            line += ' ' + '%02d' % x
        print line
		
    # FIX ME SQUARE GRID
    # Returns distance and angle of hit on mech
    def get_dist(self, loc_xy, targ_xy, loc_face, targ_face=None, m_type=None):
        # adjust opposing mech relation
        #face += 180
        hit_ang = 0
        x = targ_xy[0] - loc_xy[0]
        y = targ_xy[1] - loc_xy[1]
        offset_one = 0
        offset_two = 1
        if x < 0 and y < 0:
            offset_two = 1
            offset_one = 180
        elif x < 0:
            offset_two = -1
            offset_one = 0
        elif y < 0:
            offset_one = 90
            offset_two = 1
        #print offset_one, offset_two
        '''
        if x < 0 and y < 0:
            #print 'neg x and y'
            offset_one = 180
            offset_two = 1
            x = abs(x)
            y = abs(y)
        if x < 0 or y < 0:
            #print 'neg x or y'
            offset_one = 180
            offset_two = -1
        '''
        x = abs(x)
        y = abs(y)
        if x == 0 or y == 0:
            dist = x + y
            ang = 0 #loc_face
        else:
            # On a square grid we can just pythagarise. Note: rounded down
            dist = int(math.sqrt(pow(x, 2) + pow(y, 2)) + 0.5)
            ang = math.degrees(math.atan(float(y) / x)) # + loc_face

        #print 'ang is ', ang
        ang = self._angle_correct(ang * offset_two + offset_one)
        #print ang, offset_one, offset_two
        #dist = int(dist + 0.5)
        #if targ_face == 'ang_only':
            #return self._angle_correct((ang - loc_face) * offset_two + offset_one)
        #if targ_face == 'ang_only':
        #    return (ang - loc_face) * offset_two + offset_one
        #ang = self._angle_correct(ang * offset_two + offset_one)
        if targ_face == 'ang_only':
            return ang
        
        #print ang
        if targ_face is not None:
            hit_ang = self._angle_correct(ang + 180 - targ_face)
        ang -= loc_face
        for a in [ang, hit_ang]:
            while a < 0:
                a += 360
            while a >= 360:
                a -= 360
        if targ_face is not None:
            return dist, ang, hit_ang
        else:
            # Get turn required, 1 move per 60 degrees
            turn = ang
            if ang > 180:
                turn = ang - 180
            # Jumping ignores turning
            if m_type == 2:
                turn = 0
            return dist + int(turn / 60), ang

    def _angle_correct(self, ang):
        while ang < 0:
            ang += 360
        while ang >= 360:
            ang -= 360
        return ang



