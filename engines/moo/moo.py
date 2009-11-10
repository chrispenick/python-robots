#!/usr/bin/python
import random
import time, sys

import engine

MESS_NUMBER_DIGITS = "number_digits" #start message
MESS_GUESS = "guess!"
MESS_COWS = "cows:"  #If the matching digits on different positions, they are "cows" 
MESS_BULLS = "bulls:" #If the matching digits are on their right positions, they are "bulls" 
MESS_BULLS_COWS_SPLIT = "|" #Splitter between cows and bulls message
MAX_TURN_NUMBER = 1000



class MooPlayer(engine.Player):
    def __init__(self, name, progname):
        super(MooPlayer, self).__init__(name,progname)
        self.turns = 0
        self.time = -1


class MooEngine(engine.Engine):
    def __init__(self, players_prognames, opts, output, output_file=sys.stdout): 
        super(MooEngine, self).__init__(players_prognames=players_prognames, opts=opts, \
                        output=output, output_file=output_file, player_type=MooPlayer)
        self.number = int(opts["number_digits"])
        if self.number > 10:
            exit()
        self.secret = self.make_secret(self.number)

        self.screenln( ">>>> I think: %s" % self.secret)


    def is_right_secret(self, secret):
        """check all digits are different"""
        dct = []
        for digit in secret:
            if digit in dct:
                return 0
            else:
                dct.append(digit)
        return True

    def make_secret(self, number):
        """generate number-counted secret"""
        while True:
            result = ''.join([ str(random.randint(0,9)) for x in range(number) ]) 
            if self.is_right_secret(result):
                return result

    def count_bulls_cows(self, number, secret):
        """count bulls and cows in number/secret"""
        cows, bulls = 0, 0
        dct = {}
        for i in range(len(secret)):
            if secret[i]==number[i]:
                bulls += 1
            else:
                dct[secret[i]] = True
                try:
                    if dct[number[i]]:
                        cows += 1
                except KeyError:
                    pass
        self.screenln( ">>>> bulls:%d cows:%d" % (bulls, cows))
        return bulls, cows


    def main(self):
        for playername in self.players:
            player = self.players[playername]
            player.connect()
            player.send("%s %d" % (MESS_NUMBER_DIGITS, self.number))
            self.screenln("%s %d" % (MESS_NUMBER_DIGITS, self.number))
            starttime = time.time() 
            while True:
                if player.turns > MAX_TURN_NUMBER:
                    self.screenln( ">>>> Player '%s' turns timeout" % player.name)
                    player.disconnect()
                    break
                answer = player.recieve()
                self.screenln(">>>> Answer is %s" % answer)
                if len(self.secret)!=len(answer):
                    self.stop_game("wrong number")
                bulls, cows = self.count_bulls_cows(answer, self.secret)
                if bulls==self.number:
                    player.time = time.time() - starttime
                    player.send("%s" % MESS_GUESS)
                    player.disconnect()
                    self.screenln(">>>> Player disconected")
                    break
                else:
                    player.turns += 1
                    player.send("%s %d%s%s %d" % (MESS_BULLS, bulls,\
                            MESS_BULLS_COWS_SPLIT, MESS_COWS, cows))
                    self.screenln(">>>> %s %d%s%s %d" % (MESS_BULLS, bulls,\
                            MESS_BULLS_COWS_SPLIT, MESS_COWS, cows) )

        '''winner = self.players[0]
        for player in self.players:
            if player.turns<winner.turns:
                winner = player'''
#        self.screenln(">>>> Winner name: %s" % winner.name)
    




if __name__ == "__main__":
    mooengine = MooEngine.ParseArgs(sys.argv[1:])
    mooengine.main()
