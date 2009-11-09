#!/usr/bin/python
import random
import sys

MESS_NUMBER_DIGITS = "number_digits" #start message
MESS_GUESS = "guess!"
MESS_COWS = "cows:"  #If the matching digits on different positions, they are "cows" 
MESS_BULLS = "bulls:" #If the matching digits are on their right positions, they are "bulls" 
MESS_BULLS_COWS_SPLIT = "|" #Splitter between cows and bulls message



class MooPlayer(object):

    ##technical functions
    def send(self, st):
        sys.stdout.write("%s\n"%st)
        sys.stdout.flush()

    def recieve(self):
        return sys.stdin.readline().strip("\n")
   

    def number_split(self, st):
        num = st.split(' ')
        if num[0]==MESS_NUMBER_DIGITS:
            return int(num[1])
        else:
            exit()

    def answer_split(self, st):
        try:
            bullst, cowst = st.split(MESS_BULLS_COWS_SPLIT)
        except ValueError:
            #sys.stderr.write('------------'+st+'-----------')
            exit()
        bulls, cows = bullst.split(' '), cowst.split(' ')
        if bulls[0]==MESS_BULLS and cows[0]==MESS_COWS:
            return bulls[1], cows[1]
        else:
            exit()

    def main(self):
        self.number = self.number_split(self.recieve())

        while True:
            try:
                self.oldguess = guess
                guess = self.guess(cows=cows, bulls=bulls, firstrun=False)
            except NameError:
                guess = self.guess(firstrun=True)
            self.send(guess)
            answer = self.recieve()
            if answer == MESS_GUESS:
                exit()
            else:
                bulls, cows = self.answer_split(answer)


    ##some functions
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


    def generate_number(self, number):
        """generate number-counted secret"""
        while True:
            result = ""
            for i in range(number):
                result += "%d" % random.randint(0,9)
            if self.is_right_secret(result):
                return result

    ############ Main guess function ###########
    def guess(self, firstrun, bulls=0, cows=0):
        """This is main api function. firstrun means that it is first time run,
        bulls/cows is number of bulls and cows from last time.
        also you have:
            self.number  - number of digits
            self.oldguess - old guess try
        """
        return self.generate_number(self.number)


if __name__ == "__main__":
    mooplayer = MooPlayer()
    mooplayer.main()
