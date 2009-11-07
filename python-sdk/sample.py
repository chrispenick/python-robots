#!/usr/bin/python
"""Sample game bot for python-robots"""
import pyr-sdk


class DumbBoot(pyr-sdk.Pobot):
    def main(self):
        """Main cyclic function: :))"""
        for enemyrobot in self.robots:
            if self.GetDistToRobot(enemyrobot)<4:
                self.FireToRobot(enemyrobot)
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
