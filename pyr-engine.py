#!/usr/bin/python

"""Engine for PYR"""

import math, random
import json

WALL = "#"
GROUND = '.'
AMMO = "A"
ENERGY = "E"
FOREST = "$"
WATER = "_"

MAXCOORDS=1000

FIREMAXDIST = 4.3
ENERGYMAX = 100
LIVEMAX = 100
AMMOMAX = 100

def Fire(energy, dist):
    """Is robot with energy energy on distantion dist fired?"""
    return (float(energy)/float(ENERGYMAX))*FIREMAXDIST >= random.uniform(FIREMAXDIST/2, FIREMAXDIST*2)






class MMap(dict):
    def __getitem__(self, key):
        if not self.has_key(key):
            return FieldWall(Coordinate(-1,-1),self)
        else:
            return super(MMap, self).__getitem__(key)
    def Print(self):
        for y in range(self.max_y):
            st = ""
            for x in range(self.max_x):
                st+="%s"%self[Coordinate(x,y)]
            print st

    def __repr__(self):
        res =""
        for y in range(self.max_y):
            st = ""
            for x in range(self.max_x):
                st+="%s"%self[Coordinate(x,y)]
            res += st +"\n"
        return res
    ###some work
    def GetFreeCoordinates(self):
        return Coordinate(0,0)

    def LoadFile(self,filename):
        f = open(filename, 'r')
        y = 0
        self.max_x=0
        for line in f:
            x = 0
            for symbol in line.strip('\n'):
                if x> self.max_x:
                    self.max_x = x+1
                coord = Coordinate(x,y)
                if symbol == GROUND:
                    self[coord]=FieldGround(coord, self)
                elif symbol == WALL:
                    self[coord]=FieldWall(coord, self)
                elif symbol == WATER:
                    self[coord]=FieldWater(coord, self)
                elif symbol == FOREST:
                    self[coord]=FieldForest(coord, self)
                elif symbol == ENERGY:
                    self[coord]=FieldEnergy(coord, self)
                elif symbol == AMMO:
                    self[coord]=FieldAmmo(coord, self)
                x += 1
            y += 1
        self.max_y = y


class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        res = "X,Y:(%d,%d)" %(self.x, self.y)
        return res

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __hash__(self):
        #need correct
        return self.x+MAXCOORDS*self.y

    def GetDistToCoordinate(self, coord):
        """Gets distantion to coord, coord must be Coordinate"""
        x = self.x - coord.x
        y = self.y - coord.y
        dist = math.sqrt( (x*x) + (y*y) )
        return dist

    def GetNext(self, position, dist=1):
        """position mustbe position"""
        res = Coordinate(self.x, self.y)
        if position.isEast():
            res.x+=dist
        elif position.isWest():
            res.x-=dist
        elif position.isNorth():
            res.y-=dist
        elif position.isSouth():
            res.y+=dist
        return res


class Field(object):
    """Field of map"""
    crossable = True
    fireable = True
    abbv = "main field type :))"

    def __init__(self, coord, mmap):
        self.__mmap = mmap
        self.coord = coord
        self.isBusy = False

    def __repr__(self):
        if self.isBusy:
            return "%s" % self.robot.position
        else:
            return "%s" % self.abbv

    def Set(self, robot):
        """robot must be Robot object"""
        self.robot = robot
        self.isBusy = True


    def Come(self, robot):
        """robot must be Robot object"""
        self.robot = robot
        self.GetSpecialToRobotStandedOn(robot)
        self.isBusy = True

    def Leave(self):
        self.robot = None
        self.isBusy = False


    def GetSpecialToRobotStandedOn(self, robot):
        """Gets special ability of field to robot object"""
        pass

    def isCrossable(self):
        if self.isBusy:
            return False
        else:
            return self.crossable

    def isFireable(self):
        if self.isBusy:
            return False
        else:
            return self.fireable


class FieldGround(Field):
    """Ground in map"""
    abbv = GROUND
    pass


class FieldWall(Field):
    crossable = False
    fireable = False
    abbv = WALL


class FieldWater(Field):
    crossable = False
    fireable = True
    abbv = WATER

class FieldForest(Field):
    crossable = True
    fireable = False
    abbv = FOREST

class FieldAmmo(Field):
    """Gets ammo to robot"""
    abbv = AMMO
    AMMOONTURN=10
    def GetSpecialToRobotStandedOn(self, robot):
        """Gets special ability of field to robot object"""
        robot.ammo += self.AMMOONTURN

class FieldEnergy(Field):
    """Gets ammo to robot"""
    abbv = ENERGY
    ENERGYONTURN=10
    def GetSpecialToRobotStandedOn(self, robot):
        """Gets special ability of field to robot object"""
        robot.energy += self.ENERGYONTURN



class Position(object):
    _PosDict={\
        "East":">",\
        "West":"<",\
        "North":"^",\
        "South":"\\/",\
        }
    EAST = _PosDict["East"]
    WEST = _PosDict["West"]
    NORTH = _PosDict["North"]
    SOUTH= _PosDict["South"]
    """Which turn of robot"""
    def __init__(self, pos):
        self.__pos = pos

    def __repr__(self):
        return self.__pos

    def isNorth(self):
        if self.__pos == self._PosDict["North"]:
            return True
        else:
            return False

    def isEast(self):
        if self.__pos == self._PosDict["East"]:
            return True
        else:
            return False

    def isWest(self):
        if self.__pos == self._PosDict["West"]:
            return True
        else:
            return False

    def isSouth(self):
        if self.__pos == self._PosDict["South"]:
            return True
        else:
            return False

    def TurnLeft(self):
        if self.__pos==self._PosDict["East"]:
            self.__pos = self._PosDict["North"]
        elif self.__pos==self._PosDict["North"]:
            self.__pos = self._PosDict["West"]
        elif self.__pos==self._PosDict["West"]:
            self.__pos = self._PosDict["South"]
        elif self.__pos==self._PosDict["South"]:
            self.__pos = self._PosDict["East"]

    def TurnRight(self):
        if self.__pos==self._PosDict["East"]:
            self.__pos = self._PosDict["South"]
        elif self.__pos==self._PosDict["North"]:
            self.__pos = self._PosDict["East"]
        elif self.__pos==self._PosDict["West"]:
            self.__pos = self._PosDict["North"]
        elif self.__pos==self._PosDict["South"]:
            self.__pos = self._PosDict["West"]


class Robot(object):

    def __init__(self, coord, mmap, field, name, energy=ENERGYMAX, live=LIVEMAX, ammo=LIVEMAX \
        , position=Position(Position.NORTH)):
        """Position must be position, coord must be Coordinate"""
        self.field = field
        self.field.Set(self)
        self.coord = coord
        self.__mmap = mmap
        self.name = name
        self.energy = energy
        self.live = live
        self.ammo = ammo
        self.position = position

    def __repr__(self):
        res = "Robot \"%s\" L:%d E:%d A:%d P:|%s| cord:%s" % (self.name, self.live, \
                self.energy, self.ammo, self.position, self.coord)
        return res

    def TurnLeft(self):
        self.position.TurnLeft()

    def TurnRight(self):
        self.position.TurnRight()

    def KillYouSelf(self):
        self.live = 0
        self.field.Leave()

    def isWallAhead(self, dist=1):
        newcoord = self.coord.GetNext(self.position, dist)
        return self.__mmap[newcoord].isCrossable()

    def Go (self, dist=1):
        """dist - distantion"""
        newcoord = self.coord.GetNext(self.position, dist)
        if self.__mmap[newcoord].isCrossable():
            self.coord = newcoord
            self.field.Leave()
            self.field = self.__mmap[self.coord]
            self.field.Come(self)

    def GetDistToRobot(self,robot):
        """Gets distantion to enemy robot, robot must be Robot type"""
        return self.coord.GetDistToCoordinate(robot.coord)

    def isDirToRobot(self, robot):
        """If direction to robot, then returns true"""
        return True

    def FireToRobot(self, robot):
        """Fire to robot. Robot must be Robot type"""
        if Fire(self.energy, self.GetDistToRobot(robot)) and self.isDirToRobot(robot):
            print "Fire!!!!"
            robot.live -= 1
        else:
            print "Miss :(("
            pass

    def Json(self):
        return json.dumps(self, sort_keys=True, indent=4, cls=RobotEncoder)


class RobotEncoder(json.JSONEncoder):
     ''' a custom JSON encoder for Robot objects '''
     def default(self, robot):
         if not isinstance (robot, Robot):
             print 'You cannot use the JSON custom MyClassEncoder for a non-Robot object.'
             return
         return {'name':robot.name, 'live':robot.live, 'energy':robot.energy,\
                'ammo':robot.ammo, 'coord':(robot.coord.x,robot.coord.y),\
                'position':"%s"%robot.position
             }

class RobotDecoder(json.JSONDecoder):
    def __init__(self, **kw):
        self.mmap=kw['mmap']

    def decode (self, json_string):
        my_class_dict = json.loads(json_string)
        return Robot(name=my_class_dict['name'], live=my_class_dict['live'], \
                      energy=my_class_dict['energy'], ammo=my_class_dict['ammo'],\
                      mmap=self.mmap, field=self.mmap[Coordinate(my_class_dict['coord'][0],my_class_dict['coord'][1])], \
                      coord=Coordinate(my_class_dict['coord'][0],my_class_dict['coord'][1]),\
                      position=Position(my_class_dict['position']))

if __name__=="__main__":
    def PRINT():
        mmap.Print()
        print robot.GetDistToRobot(enemyrobot)
        print robot
        print enemyrobot

    """pos = Position(">")
    pos.TurnLeft()
    print pos
    pos.TurnLeft()
    print pos
    pos.TurnLeft()
    print pos
    pos.TurnLeft()
    print pos
    pos.TurnLeft()
    print pos
    print "another"

    pos.TurnRight()
    print pos
    pos.TurnRight()
    print pos
    pos.TurnRight()
    print pos
    pos.TurnRight()
    print pos
    pos.TurnRight()
    print pos"""
    mmap = MMap()
    mmap.LoadFile('testmap')
    #print mmap
    mmap.Print()
    robot = Robot(coord=Coordinate(4,4),mmap=mmap,field=mmap[Coordinate(4,4)],
            name="Darvi", energy=100, ammo=92, live=94, position=Position(Position.NORTH))
    enemyrobot = Robot(coord=Coordinate(6,6),mmap=mmap,field=mmap[Coordinate(6,6)],
            name="P_r_i_m_a", energy=100, ammo=92, live=94, position=Position(Position.NORTH))
    robot.Go()
    PRINT()
    robot.TurnRight()
    PRINT()
    robot.Go()
    PRINT()
    robot.TurnLeft()
    PRINT()
    robot.Go()
    robot.FireToRobot(enemyrobot)
    PRINT()
    enemyrobot.TurnLeft()
    robot.FireToRobot(enemyrobot)
    PRINT()
    enemyrobot.Go()
    robot.FireToRobot(enemyrobot)
    PRINT()
    enemyrobot.Go()
    robot.FireToRobot(enemyrobot)
    PRINT()
    enemyrobot.Go()
    robot.FireToRobot(enemyrobot)
    PRINT()
    enemyrobot.Go()
    robot.FireToRobot(enemyrobot)
    PRINT()
    enemyrobot.Go()
    robot.FireToRobot(enemyrobot)
    PRINT()
    enemyrobot.Go()
    robot.FireToRobot(enemyrobot)
    PRINT()
    enemyrobot.Go()
    robot.FireToRobot(enemyrobot)
    PRINT()
    enemyrobot.Go()
    robot.FireToRobot(enemyrobot)
    PRINT()
    robot.TurnRight()
    robot.Go()
    robot.Go()
    PRINT()
    robot.TurnLeft()
    robot.Go()
    robot.Go()
    robot.Go()
    robot.Go()
    robot.Go()
    robot.Go()
    robot.Go()
    robot.Go()
    robot.Go()
    PRINT()

    print robot.Json()
    print enemyrobot.Json()

    jsonsavedrobot = enemyrobot.Json()
    newrobot = json.loads(jsonsavedrobot, cls=RobotDecoder, mmap=mmap)
    print newrobot
