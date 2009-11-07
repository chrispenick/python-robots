#!/usr/bin/python
"""Turn. with --start starts new game, with --cont continie"""
import "pyr-engine"

class Game(object):
    def __init__(mapfilename, users):
        self.mmap=pyr-engine.MMap.LoadFile(mapfilename)
        self.users=users
        for user in self.users:
            freecoord = self.mmap.GetFreeCoordinate()
            self.robots[user] = pyr-engine.Robot(freecoord,\
                    self.mmap, self.mmap[freecoord], user)
    def start(self):
        self.StartRobots()
        self.GiveMap()
        self.GiveInfo()


    def turn(self):
        self.ParseOrders()
        self.CheckAlive()
        self.GiveMap()
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
        elif st=="Fire":
            rob.FireToRobot(self.robots[arg])
        else:
            Exit("Invalid command from roboprogramm!")



if __name__ == "__main__":
    game = Game()
    game.start()
    while True:
        game.turn()
