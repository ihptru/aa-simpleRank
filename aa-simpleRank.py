#!/usr/bin/env python

path_to_cmds = ""
path_to_won_matches = ""

import sys

class Rank:
    def __init__(self, path_to_cmds, path_to_won_matches):
        self.cmds = path_to_cmds
        self.won_matches = path_to_won_matches
    
    def flush(self, data):
        file = open(self.cmds, 'a')
        file.write(data)
        file.close()

    def index(self, index):
        if index == "1":
            return index + "st)"
        elif index == "2":
            return index + "nd)"
        elif index == "3":
            return index + "rd)"
        else:
            return index + "th)"

    def rank(self):
        while 1:
            line = sys.stdin.readline()
            line = line.rstrip()
            line_args = line.split(' ')
            if line_args[0] == 'MATCH_WINNER':
                global_result = []
                winner = []
                winner_name = line_args[2]
                
                matches = open(self.won_matches, 'r').readlines()
                winner_raw = ""
                for player in matches:
                    player_data = player.split()
                    if player_data[1] == winner_name:
                        index = str(matches.index(player))
                        index = self.index(index)
                        winner.append("0xff0000    "+index)
                        winner.append(player_data[0])
                        winner.append(winner_name)
                        winner_raw = player
                if len(winner) == 0:
                    data = "CONSOLE_MESSAGE 0x00ff00"+winner_name+" won their first match!"
                    self.flush(data)
                    continue
                winner_index = matches.index(winner_raw)
                for i in range(winner_index-2, winner_index):
                    try:
                        index = self.index(str(i))
                        global_result.append(["0xffff99    "+index, matches[i].split()[0], matches[i].split()[1]])
                    except:
                        pass
                global_result.append(winner)
                for i in range(winner_index+1, winner_index+3):
                    try:
                        index = self.index(str(i))
                        global_result.append(["0xffff99    "+index, matches[i].split()[0], matches[i].split()[1]])
                    except:
                        pass
                self.flush("CONSOLE_MESSAGE 0x00ff00Won Matches:\n")
                for value in global_result:
                    self.flush("CONSOLE_MESSAGE "+value[0]+" "+value[1]+"  "+value[2]+"\n")

if __name__ == "__main__":
    rank = Rank(path_to_cmds, path_to_won_matches)
    rank.rank()
