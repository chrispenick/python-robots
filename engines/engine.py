#!/usr/bin/python
"""
Parent module for all game-engines
"""

import sys,subprocess

class Player(object):
    """
    Class to communicate with players-programs
    """
    def __init__(self, name, progname):
        """
        name - name of player
        progname - path to programm
        """
        self.name = name
        self.progname = progname

    def connect(self):
        """
        Starts player-programm instance
        """
        self.__proc = subprocess.Popen(self.progname, stdin=subprocess.PIPE,\
                        stdout=subprocess.PIPE)

    def send(self, sendstring):
        """
        Sends line to program
        """
        self.__proc.stdin.write(sendstring+'\n')

    def recieve(self):
        """
        Reads line from programm output, stripes \\n
        """
        return self.__proc.stdout.readline().strip('\n')

    def disconnect(self):
        """
        Terminates programm
        """
        self.__proc.terminate()


class Engine(object):
    """
    Parent class for engines class's
    """
    OUTPUT_SCREEN = "screen"
    OUTPUT_XML = "xml"
    OUTPUT_TYPES = [OUTPUT_XML, OUTPUT_SCREEN]
    OUTPUT_FILENAME_STDOUT = "-"

    def __init__(self, players_prognames, opts, output, output_file=sys.stdout, player_type=Player):
        """
        players_prognames - dict of playersname:path to programs
        opts - some custom options to engine, dict
        output - type of output, see Engine.OUTPUT_TYPES
        output_file - file object to write to
        player_type - class for Players instance
        """
        self.opts, self.output, self.output_file = opts, output, output_file

        self.players = {}
        for playername in players_prognames:
            self.players[playername] = player_type(playername, players_prognames[playername])

    @classmethod
    def ParseArgs(cls, argst):
        """
        Parses argst string and returns Engine object
        """
        from optparse import OptionParser
        usage = "usage: %prog [options] PlayerName1:/usr/bin/player-prog1 PlayerName2:/home/play2/prog2"
        parser = OptionParser(usage=usage)
        parser.add_option('-o','--output', choices=cls.OUTPUT_TYPES, type='choice'\
			, dest='output', default=cls.OUTPUT_SCREEN \
			,help='output type ('+', '.join(cls.OUTPUT_TYPES)+') [default: %default]')
        parser.add_option("-f", "--file-output", dest="output_filename",
                  help="write game log to FILE, may be regular filename or '%s' for STDOUT" % \
                        cls.OUTPUT_FILENAME_STDOUT + '[default: %default]', \
                        default=cls.OUTPUT_FILENAME_STDOUT, metavar="FILE")
        parser.add_option("-a", "--args", dest="options",
                  help="common-separated list of custom options", metavar="o1=v1,o2=v2")
        (options, args) = parser.parse_args(args=argst)

        opts = {}
        if options.options:
            opts = options.options.split(',')
            opts = dict([ opt.split('=') for opt in opts ])

        if not args:
            raise AssertionError
        else:
            players_progs =  dict([ arg.split(':') for arg in args ])

        output = options.output
        if options.output_filename==cls.OUTPUT_FILENAME_STDOUT:
            output_file = sys.stdout
        else:
            output_file = open(options.output_filename, 'w')
        return cls(players_prognames=players_progs, opts=opts, output=output, output_file=output_file)


    def writeln(self,st):
        """
        Writes string to output file
        """
        self.output_file.write(st+'\n')

    def screenln(self,st):
        """
        Writes string to output file, only if output is to screen
        """
        if self.output==self.OUTPUT_SCREEN:
            self.writeln(st)

    def stop_game(self, st):
        """
        Stops all players-games and exit programms
        st - string to say
        """
        for player in self.players:
            player.disconnect()
        if self.screen():
            self.writeln(">>>> Game stopped: %s" % st)
        exit()

    def main(self):
        """
        main loop
        """
        pass



if __name__=="__main__":
    sampleengine = Engine.ParseArgs(sys.argv[1:])
    sampleengine.writeln('Dumbengine')
    sampleengine.main()
    import pprint
    pprint.pprint (sampleengine.__dict__)
