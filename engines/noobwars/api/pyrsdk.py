#!/usr/bin/python

"""Python SDK for PYR"""

import json,sys,math

WALL = "#"
GROUND = '.'
AMMO = "A"
ENERGY = "E"
FOREST = "$"
WATER = "_"

MAXCOORDS=1000



def ReadUntil(untilstr):
        line = ""
        name = ""
        while line.strip('\n')!=untilstr:
            name += line
            line = sys.stdin.readline()
        return name


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

    def LoadStdin(self):
        y = 0
        self.max_x=0
        line =""
        while line!="EOM":
            line=sys.stdin.readline().strip('\n')
            x = 0
            for symbol in line.strip('\n'):
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
                if x> self.max_x:
                    self.max_x = x
            y += 1
        self.max_y = y-1


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
        self.mmap = mmap
        self.coord = coord
        self.isBusy = False

    def __repr__(self):
        if self.isBusy:
            return "%s" % self.robot.position
        else:
            return "%s" % self.abbv


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

    def __init__(self, coord, mmap, field, name, energy, live, ammo \
        , position=Position(Position.NORTH)):
        """Position must be position, coord must be Coordinate"""
        self.field = field
        self.coord = coord
        self.mmap = mmap
        self.name = name
        self.energy = energy
        self.live = live
        self.ammo = ammo
        self.position = position
        self.isIam = False

    def __repr__(self):
        res = "Robot \"%s\" L:%d E:%d A:%d P:|%s| cord:%s" % (self.name, self.live, \
                self.energy, self.ammo, self.position, self.coord)
        return res

    def WriteLn(self, st):
        sys.stdout.write("%s\n"%st)
        sys.stdout.flush()

    def Left(self):
        self.WriteLn("Left")


    def Right(self):
        self.WriteLn("Right")

    def Idle(self):
        self.WriteLn("Idle")

    def KillMe(self):
        self.WriteLn("KillMe")

    def Go (self):
        self.WriteLn("Go")

    def FireToRobot(self, robot):
        """Fire to robot. Robot must be Robot type"""
        self.WriteLn("Fire %s" % robot.name)

    def isWallAhead(self, dist=1):
        newcoord = self.coord.GetNext(self.position, dist)
        return not self.mmap[newcoord].isCrossable()

    def GetDistToRobot(self,robot):
        """Gets distantion to enemy robot, robot must be Robot type"""
        return self.coord.GetDistToCoordinate(robot.coord)


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



class Pobot(Robot):
    """Main Sdk class"""



    def __init__(self):
        self.myoldusername=""
        self.turnnumber = 1
        self.start()

        self.WriteLn("CONNECT")
        self.reloading(True)


    def __repr__(self):
        return "My name '%s', myself:|%s| \n -- map -- \n%s\n%dX%d\n =robots=\n%s" %\
            (self.name, super(Pobot, self).__repr__(), \
            self.mmap, self.mmap.max_x, self.mmap.max_y, self.robots)


    def reloading(self, newsession=False):
        self.name = ReadUntil('EON').strip('\n')
        if self.myoldusername=="":
            self.myoldusername=self.name
        self.mmap = MMap()
        self.mmap.LoadStdin()
        self.robots = []
        robostring ="}\n"+ReadUntil('EOR').strip('\n')+"\n{"
        robostrings = robostring.split("}\n{")
        for st in robostrings:
            if len(st)<5:
                robostrings.remove(st)
        #sys.stderr.write("%s"%robostrings)
        for st in robostrings:
            #print "!!!!!!"+st+"!!!!!!"
            self.robots.append( json.loads("{"+st+"}", cls=RobotDecoder, mmap=self.mmap))


        for robot in self.robots:
            if robot.name==self.name:
                robot.isIam = True
                myself = robot
        self.live = myself.live
        self.energy = myself.energy
        self.ammo = myself.ammo
        self.coord = myself.coord
        self.field = myself.field
        self.position = myself.position

        #go to main loop!
        self.main()

    def main(self):
        self.Idle()
        self.turnnumber += 1
        self.reloading()
    def start(self):
        pass


if __name__=="__main__":
    pob = Pobot()
    print '%s' % pob
    #newrobot = json.loads(jsonsavedrobot, cls=RobotDecoder, mmap=mmap)
    #print newrobot
