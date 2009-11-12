#!/usr/bin/python
"""
This module realise programm-player start at local and net
"""


import subprocess,sys

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
        self.progargs = ""

    def connect(self):
        """
        Starts player-programm instance
        """
        self.__proc = self.run_programm(self.progname, self.progargs)
        
        
    def run_programm(self, progname, progargs):
        return subprocess.Popen(executable=progname, args=progargs, stdin=subprocess.PIPE,\
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




class PlayerMultiLang(Player):
    """
    This class run many languages programm, it can even compile it from source
    """
    INTERPRETED = {
        "bash":"/bin/bash", 
        "python":"/usr/bin/python",
        "perl":"/usr/bin/perl", 
        "ruby":"/usr/bin/ruby",

        }
        #many work
    COMPILED = {
        "cpp" : "/usr/bin/gcc",
        }
    def __init__(self, name, progname, progtype):
        """
        name - player name
        progname - where on this machine programm source file
        progtype - name of programming language
        """
        self.progargs = ""
        self.name = name
        if progtype in self.INTERPRETED:
            #sys.chmod(progname, stat.S_IXUS)
            self.progname = self.INTERPRETED[progtype]
            self.progargs = progname
        elif progtype in self.COMPILED:
            self.progname = self.build(progname, progtype)
        else:
            raise AssertionError

    def build(self, progname):
        """
        builds progname and returns name of executable
        """
        ##many work
        compiled_progname=progname

        return compiled_progname




class PlayerMultiLangSSH(PlayerMultiLang):
    """
    This class runs many languages programm by ssh
    """
    SSH_EXEC_PATH="/usr/bin/ssh"
    SCP_EXEC_PATH="/usr/bin/scp"
    TMP_FILENAME="/tmp/programm"
    def __init__(self, name, progname, progtype, ssh_server, ssh_user):
        """
        name - player name
        progname - where on this machine programm source file
        progtype - name of programming language
        ssh server - server to start on
        ssh user - user to start on
        """
        self.ssh_user, self.ssh_server = ssh_user, ssh_server
        os.system("%s %s %s@%s:%s" % (SCP_EXEC_PATH, progname, ssh_user, ssh_server, TMP_FILENAME) )
        progname = TMP_FILENAME
        super(PlayerMultiLangSSH, self).__init__(name, progname, progtype)
    
    def run_programm(self, progname, progargs):
        """
        runs programm on own server
        """
        prog = "%s %s" % (progname, progargs)
        sshargs = '%s@%s "%s"' % (self.ssh_user, self.ssh_server, prog)
        return subprocess.Popen(executable=SSH_EXEC_PATH, args=sshargs, stdin=subprocess.PIPE,\
                        stdout=subprocess.PIPE)


if __name__=="__main__":
    player = PlayerMultiLang(sys.argv[1],sys.argv[2],sys.argv[3])
    player.connect()
    player = Player(sys.argv[1],sys.argv[2])
    player.connect()
