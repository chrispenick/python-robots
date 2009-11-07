#!/usr/bin/python
"""Turn. with --start starts new game, with --cont continie"""
import subprocess

import "pyr-engine"

def Exit(st):
    print st
    exit()


class Game(object):
    def __init__(mapfilename, users):
        self.mmap=pyr-engine.MMap.LoadFile(mapfilename)
        self.users=users
        self.proc={}
        for user in self.users:
            freecoord = self.mmap.GetFreeCoordinate()
            self.robots[user] = pyr-engine.Robot(freecoord,\
                    self.mmap, self.mmap[freecoord], user)



    def StartRobots(self):
        for user in self.users:
            prog = self.users[user]["prog_filename"]
            self.proc[user] = subprocess.Popen(prog, stdin=subprocess.PIPE,\
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def GiveInfo(self):
        for user in self.users:
            st = "%s"%self.mmap
            st += self.robots[user].Json()
            self.proc[user].communicate(st)


    def CheckAlive(self)
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

    def ParseOrders()
       for user in self.users:
            order = self.proc[user].communicate(st)
            self.__order(user, order)

    def start(self):
        self.StartRobots()
        self.GiveInfo()


    def turn(self):
        self.ParseOrders()
        self.CheckAlive()
        self.GiveInfo()


    def __order(self, user, stringorder):
        (st, arg) = stringorder.split(' ')
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
    game = Game()
    game.start()
    while True:
        game.turn()
