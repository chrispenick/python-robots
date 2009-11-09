#!/usr/bin/python
import random
import time, sys
import subprocess

MESS_NUMBER_DIGITS = "number_digits" #start message
MESS_GUESS = "guess!"
MESS_COWS = "cows:"  #If the matching digits on different positions, they are "cows" 
MESS_BULLS = "bulls:" #If the matching digits are on their right positions, they are "bulls" 
MESS_BULLS_COWS_SPLIT = "|" #Splitter between cows and bulls message
MAX_TURN_NUMBER = 1000



class Player(object):
    def __init__(self, name, progname):
        self.name = name
        self.turns = 0
        self.time = -1
        self.progname = progname

    def connect(self):
        self.__proc = subprocess.Popen(self.progname, stdin=subprocess.PIPE,\
                        stdout=subprocess.PIPE)
    
    def send(self, sendstring):
        self.__proc.stdin.write(sendstring+'\n')

    def recieve(self):
        return self.__proc.stdout.readline().strip('\n') 

    def disconnect(self):
        self.__proc.terminate()


class Game(object):
    def __init__(self, number, players_progs):
        if number > 10:
            exit()
        self.number = number
        self.secret = self.make_secret(self.number)

        print ">>>> I think: %s" % self.secret
        self.players = []

        for playername in players_progs:
            self.players.append(Player(playername, players_progs[playername]))

        self.main()

    def is_right_secret(self, secret):
        """check all digits are different"""
        dct = {}
        for digit in secret:
            try:
                if dct[digit]:
                    return False
            except KeyError:
                dct[digit] = True
        return True

    def make_secret(self, number):
        """generate number-counted secret"""
        while True:
            result = ""
            for i in range(number):
                result += "%d" % random.randint(0,9)
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
        print ">>>> bulls:%d cows:%d" % (bulls, cows)
        return bulls, cows


    def main(self):
        for player in self.players:
            player.connect()
            player.send("%s %d" % (MESS_NUMBER_DIGITS, self.number))
            print ("%s %d" % (MESS_NUMBER_DIGITS, self.number))
            starttime = time.time() 
            while True:
                if player.turns > MAX_TURN_NUMBER:
                    print ">>>> Player '%s' turns timeout" % player.name
                    player.disconnect()
                    break
                answer = player.recieve()
                print ">>>> Answer is %s" % answer
                if len(self.secret)!=len(answer):
                    self.stop_game("wrong number")
                bulls, cows = self.count_bulls_cows(answer, self.secret)
                if bulls==self.number:
                    player.time = time.time() - starttime
                    player.send("%s" % MESS_GUESS)
                    player.disconnect()
                    print ">>>> Player disconected"
                    break
                else:
                    player.turns += 1
                    player.send("%s %d%s%s %d" % (MESS_BULLS, bulls,\
                            MESS_BULLS_COWS_SPLIT, MESS_COWS, cows))
                    print(">>>> %s %d%s%s %d" % (MESS_BULLS, bulls,\
                            MESS_BULLS_COWS_SPLIT, MESS_COWS, cows) )

        winner = self.players[0]
        for player in self.players:
            if player.turns<winner.turns:
                winner = player
        print ">>>> Winner name: %s" % winner.name
    
    def stop_game(self, st):
        for player in self.players:
            player.disconnect()
        print ">>>> Game stopped: %s" % st
        exit()




if __name__ == "__main__":
    game = Game(2, {'Player1':"api/mooapi.py", 'Player2':"api/mooapi.py", 'HabraMan':"api/mooapi.py" })


