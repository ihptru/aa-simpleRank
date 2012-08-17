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
        index = str(index+1)
        if index[-1] == "1" and index[-2:] != "11":
            return index + "st)"
        elif index[-1] == "2" and index[-2:] != "12":
            return index + "nd)"
        elif index[-1] == "3" and index[-2:] != "13":
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
                temp = []
                for item in matches:
                    temp.append([item.split()[0], item.split()[1]])
                matches = temp[:]
                matches_copy = matches[:]

                winner_raw = []
                for player in matches:
                    if player[1] == winner_name:
                        index = matches.index(player)
                        winner.append(index)
                        winner.append(str(int(player[0])+1))
                        winner.append(winner_name)
                        winner_raw = player
                        #perform shuffling of the original list
                        if winner[1] > matches[index-1][0]:
                            matches_copy.pop(index)
                            for item in matches:
                                if int(item[0]) < int(winner[1]):
                                    insert_index = matches.index(item)
                                    matches_copy.insert(insert_index, winner_raw)
                                    index = matches_copy.index(winner_raw)
                                    winner[0] = index
                                    break
                matches = matches_copy[:]
                if len(winner) == 0:
                    data = "CONSOLE_MESSAGE 0x00ff00"+winner_name+" won their first match!\n"
                    self.flush(data)
                    continue
                for i in range(winner[0]-2, winner[0]):
                    if i < 0:
                        continue
                    try:
                        global_result.append([i, matches[i][0], matches[i][1]])
                    except:
                        pass
                global_result.append(winner)
                for i in range(winner[0]+1, winner[0]+3):
                    try:
                        global_result.append([i, matches[i][0], matches[i][1]])
                    except:
                        pass
                self.flush("CONSOLE_MESSAGE 0x00ff00Won Matches:\n")
                for value in global_result:
                    if value == winner:
                        color = "0xff0000"
                    else:
                        color = "0xffff99"
                    index = self.index(value[0])
                    self.flush("CONSOLE_MESSAGE "+color+"    "+index+" "+value[1]+"  "+value[2]+"\n")

if __name__ == "__main__":
    rank = Rank(path_to_cmds, path_to_won_matches)
    rank.rank()
