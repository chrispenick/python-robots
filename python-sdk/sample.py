#!/usr/bin/python
"""Sample game bot for python-robots"""
import pyrsdk


class DumbBoot(pyrsdk.Pobot):
    def main(self):
        """Main cyclic function: :))"""
        fired = False
        for enemyrobot in self.robots:
            if self.GetDistToRobot(enemyrobot)<4:
                self.FireToRobot(enemyrobot)
                fired=True
        if not fired:
            if self.energy<50:
                self.KillYouSelf()
            if not self.isWallAhead():
                self.Go()
            else:
                self.Left()

        ###########common part
        self.reloading()
        
    def start(self):
        """some code which run once"""
        pass

if __name__=="__main__":
    darvin_small_metal_guy = DumbBoot()
