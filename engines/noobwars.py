#!/usr/bin/python
"""Turn. with --start starts new game, with --cont continie"""
import sys,datetime
import subprocess

sys.path.append('../')

#import engines.engine as engine

import engines.noobwars.noobinternal as pyrengine

MAXTURNS = 450


def Exit(st):
    if METHOD=="screen":
        print st
    game.StopRobots()
    game.WriteDatas()
    exit()


def ExitUsage():
    if METHOD=="screen":
        print "Incorrect arguments! Correct usage:\n  \
            ./pyrturn.py stdio /name/of/mapfile user1:/path/to/user1/programm user2:/path/to/user2/programm"
    exit()



class Game(object):
    def __init__(self, mapfilename, users):
        self.mmap = pyrengine.MMap()
        self.mmap.LoadFile(mapfilename)
        self.users=users
        self.proc={}
        self.robots = {}
        for user in self.users:
            freecoord = self.mmap.GetFreeCoordinate()
            self.robots[user] = pyrengine.Robot(freecoord,\
                    self.mmap, self.mmap[freecoord], user)

        if METHOD=="xml":
            self.xml = ET.Element("game")
            ET.SubElement(self.xml, "date").text=str(datetime.datetime.now())
            players = ET.SubElement(self.xml, "players")
            ##temporary
            for user in self.users:
                player = ET.SubElement(players, "player")
                ET.SubElement(player, "name").text = user
                robots = ET.SubElement(player, "robots")
                ######TEMPORARY:
                robot = ET.SubElement(robots, "robot")
                robot.text = user
                ET.SubElement(player, "time").text = "0"
            self.xml_log = ET.SubElement(self.xml, "log")


    def WriteDatas(self):
        if METHOD=="xml":
            if True:
                def indent(elem, level=0):
                    i = "\n" + level*"  "
                    if len(elem):
                        if not elem.text or not elem.text.strip():
                            elem.text = i + "  "
                        for e in elem:
                            indent(e, level+1)
                            if not e.tail or not e.tail.strip():
                                e.tail = i + "  "
                        if not e.tail or not e.tail.strip():
                            e.tail = i
                    else:
                        if level and (not elem.tail or not elem.tail.strip()):
                            elem.tail = i
                indent(self.xml)
                if XMLFILENAME=="-":
                    f=sys.stdout
                else:
                    f=open(XMLFILENAME,'w')
                ET.ElementTree(self.xml).write(f)
            elif False:
                from xml.dom.minidom import parseString 
                from xml.etree import ElementTree
                def prettyPrint(element):
                    txt = ElementTree.tostring(element)
                    print parseString(txt).toprettyxml()
                prettyPrint(self.xml)
            else:
                ET.ElementTree(self.xml).write(sys.stdout)


    def StopRobots(self):
        for robot in self.robots:
            self.proc[robot].terminate()

    def StartRobots(self):
        for user in self.users:
            prog = self.users[user]
            self.proc[user] = subprocess.Popen(prog, stdin=subprocess.PIPE,\
                        stdout=subprocess.PIPE)
            programsay = self.proc[user].stdout.readline()
            if not (programsay == "CONNECT\n"):
                Exit("Bad game-programm start!")
            if METHOD=="screen":
                pass

                print "Started %s 's programm '%s', it say us '%s' " % (user, self.users[user],\
                        programsay)
                #self.proc[user].wait()


##BAD fat BUG!!!!!!!!!!

    def GiveInfo(self):
        for robot in self.robots:
            sendstring = ""
            sendstring += robot
            sendstring += "\nEON\n"
            sendstring += "%s"%repr(self.mmap)
            sendstring += "EOM\n"
            for robotnameinrobotslist in self.robots:
                sendstring += self.robots[robotnameinrobotslist].Json()+'\n'
            sendstring += "EOR\n"

            if METHOD=="screen":
                print sendstring
            self.proc[robot].stdin.write(sendstring)
            if METHOD=="screen":
                print "Sended to %s 's programm '%s'" % (robot, self.users[robot])


    def CheckAlive(self):
        mustbedeleted = []
        for robot in self.robots:
            if self.robots[robot].live<=0:
                self.proc[robot].terminate()
                self.robots[robot].KillYouSelf()
                self.proc[robot].wait()
                mustbedeleted.append(robot)

        for robot in mustbedeleted:
                del self.proc[robot]
                del self.robots[robot]
        
        if len (self.robots)==1:
            winners =""
            for robot in self.robots:
                winners += self.robots[robot].name+" "
            if METHOD=="xml":
                ET.SubElement(self.xml_log, "winner").text = winners
            Exit("Winner: "+winners)
        elif len(self.robots)==0:
            if METHOD=="xml":
                ET.SubElement(self.xml_log, "winner").text = "NOWINNERS"
            Exit("Winner: "+"NOBODY")

    def ParseOrders(self):

        for robot in self.robots:
            order = self.proc[robot].stdout.readline().strip('\n')
            self.robots[robot].order=order
            if METHOD=="screen":
                print "##################-%s-##########################"%order
            self.__order(robot, order)

    def start(self):
        self.StartRobots()
        self.GiveInfo()
        global Turn
        Turn = -1


    def turn(self):
        global Turn
        Turn += 1
        if METHOD=="screen":
            print "/////////////////////T U R N  %d ////////////////////////"%Turn
        elif METHOD=="xml":
            turn = ET.SubElement(self.xml_log, "turn")
            ET.SubElement(turn, "number").text = "%d" % Turn
            ET.SubElement(turn, "map").text = "%s"%self.mmap
            
            robots = ET.SubElement(turn, "robots")
            for rob in self.robots:
                robot = ET.SubElement(robots, "robot")
                ET.SubElement(robot, "name").text = self.robots[rob].name
                ET.SubElement(robot, "position").text = self.robots[rob].position.asName()
                ET.SubElement(robot, "energy").text = "%d" % self.robots[rob].energy
                ET.SubElement(robot, "ammo").text = "%d" % self.robots[rob].ammo
                ET.SubElement(robot, "live").text = "%d" % self.robots[rob].live
                try:
                    order = self.robots[rob].order
                except AttributeError:
                    order = "EMPTY"

                ET.SubElement(robot, "order").text = order
                coord = ET.SubElement(robot, "coord")
                ET.SubElement(coord, "x").text = "%d" % self.robots[rob].coord.x
                ET.SubElement(coord, "y").text = "%d" % self.robots[rob].coord.y

        self.ParseOrders()
        self.CheckAlive()
        self.GiveInfo()

        if Turn>=MAXTURNS:
            if METHOD=="xml":
                ET.SubElement(self.xml_log, "winner").text = "TIMEOUT"
            Exit('Nobody wins, too many (%d) turns!'%Turn)


    def __order(self, user, stringorder):
        rob = self.robots[user]
        rob.Turn() #robot one turn
        try:
            st, arg = stringorder.split(' ')
        except ValueError:
            st = stringorder
        if st=="Left":
            rob.TurnLeft()
        elif st=="Right":
            rob.TurnRight()
        elif st=="Idle":
            pass
        elif st=="Go":
            rob.Go()
        elif st=="KillMe":
            rob.KillYouSelf()
        elif st=="Fire":
            try:
                rob.FireToRobot(self.robots[arg])
            except KeyError:
                pass
        else:
            Exit("Invalid command from roboprogramm!")



if __name__ == "__main__":
    args = sys.argv
    if len (args) > 3:
        global METHOD,Turn
        METHOD = args[1]
        if METHOD == "xml":
            #import elementtree.ElementTree as ET
            #import cElementTree as ElementTree
            import xml.etree.ElementTree as ET
            global XMLFILENAME
            XMLFILENAME = args[2]
            mapfilename = args[3]
            argsuser = args[4:]
        else:
            mapfilename = args[2]
            argsuser = args[3:]
        users = {} 
        for st in argsuser:
            splited = st.split(':')
            users[splited[0]]=splited[1]
        game = Game(mapfilename, users)
        game.start()
        while True:
            game.turn()
    else:
        ExitUsage()
