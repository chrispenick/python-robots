#!/usr/bin/python
"""Turn. with --start starts new game, with --cont continie"""
import sys
import subprocess
import pyrengine

def Exit(st):
    print st
    exit()


def ExitUsage():
    print "Incorrect arguments! Correct usage:\n  \
    ./pyrturn.py stdio /name/of/mapfile user1:/path/to/user1/programm user2:/path/to/user2/programm"



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
        print self.users
        for user in self.users:


            sendstring = ""
            sendstring += user
            sendstring += "\nEON\n"
            sendstring += "%s"%repr(self.mmap)
            sendstring += "EOM\n"
            for robotname in self.robots:
                sendstring += self.robots[robotname].Json()+'\n'
            sendstring += "EOR\n"

            if METHOD=="screen":
                print sendstring
            self.proc[user].stdin.write(sendstring)
            if METHOD=="screen":
                print "Sended to %s 's programm '%s'" % (user, self.users[user])


    def CheckAlive(self):
        for user in self.users:
            if self.robots[user].live<=0:
                self.proc[user].terminate()
                self.robots[user].KillYouSelf()
                del self.robots[user]
        if len (self.robots)<=1:
            winners =""
            for robot in self.robots:
                winners += self.robot[user].name+" "
            Exit("Winner: "+winners)

    def ParseOrders(self):

        for user in self.users:
            order = self.proc[user].stdout.readline().strip('\n')
            print "##################-%s-##########################"%order
            self.__order(user, order)

    def start(self):
        self.StartRobots()
        self.GiveInfo()


    def turn(self):
        self.ParseOrders()
        self.CheckAlive()
        self.GiveInfo()


    def __order(self, user, stringorder):
        print "--string order---"+stringorder
        try:
            st, arg = stringorder.split(' ')
        except ValueError:
            st = stringorder
        rob = self.robots[user]
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
            rob.FireToRobot(self.robots[arg])
        else:
            Exit("Invalid command from roboprogramm!")



if __name__ == "__main__":
    args = sys.argv
    if len (args) > 3:
        global METHOD
        METHOD = args[1]
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
