from word import Word
from category import Category

import numpy as np
import time
import random
import copy

"""
Algorithm:

1. place a random word on the grid

2. choose a new random word
3. choose direction
4. check constraints (bounds, other chars)
5. place word, else GOTO 2

repeat until time

"""

class Crossword:
    def __init__(self, width, height):
        self.wordlist = []

        self.used_words = []

        self.width = width
        self.height = height

        self.grid = np.empty((height, width), "str")
        self.grid[:] = " "

        self.solution_positions = []

    def set_wordlist(self, wl : [Word]) -> None:
        self.wordlist = copy.deepcopy(wl)

    def get_used_words(self) -> [Word]:
        return self.used_words

    def __check_constraints(self, grid, w : Word, word_pos : (int, int), axis : int, used_words : [Word]) -> bool:
        """ returns true if the word suits,  """
        l_w = len(w)

        # check length
        if axis == 0:
            # horizontal
            if self.width <= word_pos[1] + l_w:
                return False
            elif word_pos[1] < 0:
                return False
        else:
            if self.height <= word_pos[0] + l_w:
                return False
            elif word_pos[0] < 0:
                return False

        # check all words with same axis if they interfere with this position (and their length)
        for w_ in used_words:
            # check if this word is alreay used
            if w_ == w:
                return False

            if w_.axis == axis == 0:
                if w_.pos[0] == word_pos[0] and word_pos[1] + l_w >= w_.pos[1]:
                    return False
            elif w_.axis == axis == 1:
                if w_.pos[1] == word_pos[1] and word_pos[0] + l_w >= w_.pos[0]:
                    return False
            
        # check every character position now
        w_str = str(w)
        to_check = None
        if axis == 0:
            to_check = grid[word_pos[0], word_pos[1] : word_pos[1] + l_w]
        else:
            to_check = grid[word_pos[0] : word_pos[0] + l_w, word_pos[1]]

        for i in range(l_w):
            if to_check[i] == " ":
                continue
            elif to_check[i] == w_str[i]:
                continue
            else:
                return False
        return True

    def __rand_word(self, wordlist) -> int:
        return np.random.randint(len(wordlist))

    def __algo(self, grid, wordlist : [Word], used_words : [Word]):
        # choose a random word
        w_i = self.__rand_word(wordlist)
        w = wordlist[w_i]
        while w in used_words:
            w_i = self.__rand_word(wordlist)
            w = wordlist[w_i]

        pos_found = False
        # choos a random position
        while not pos_found:
            if time.time() - self.starttime > self.maxtime:
                return grid, wordlist, used_words
            
            pos = np.random.randint((0,0), (self.width, self.height), 2)
            axis = np.random.randint(0,2)

            # check if it fits
            if(self.__check_constraints(grid, w, pos, axis, used_words)):
                # place the word
                if axis == 1: # 1 = downwards
                    grid[pos[0] : pos[0] + len(w), pos[1]] = list(w)
                else:
                    grid[pos[0], pos[1] : pos[1] + len(w)] = list(w)
                w.set_axis(axis)
                w.set_pos(pos)

                used_words.append(w)
                wordlist.remove(w)
                pos_found = True

        return self.__algo(grid, wordlist, used_words)

    def create(self, maxtime=2):
        # sort wordlist by size
        wordlist_sorted = sorted(self.wordlist, reverse=True)

        self.starttime = time.time()
        self.maxtime = maxtime

        # run
        g, wl, uw = self.__algo(self.grid[:], wordlist_sorted, [])

        self.used_words = uw
        self.grid = g

    def algo(self, grid, wordlist, used_words, not_used):
        w = wordlist[0]

        # generate a position
        its = 0
        pos_found = False
        while not pos_found and not its == 100:            
            pos = np.random.randint((0,0), (self.width, self.height), 2)
            axis = np.random.randint(0,2)

            if self.__check_constraints(grid, w, pos, axis, used_words):
                if axis == 1: # 1 = downwards
                    grid[pos[0] : pos[0] + len(w), pos[1]] = list(w)
                else:
                    grid[pos[0], pos[1] : pos[1] + len(w)] = list(w)
                w.set_axis(axis)
                w.set_pos(pos)

                used_words.append(w)
                wordlist.remove(w)
                pos_found = True
            
            its += 1
        if not pos_found:
            not_used.append(w)
            wordlist.remove(w)

        if len(wordlist) == 0:
            return grid, wordlist, used_words, not_used
        else:
            return self.algo(grid, wordlist, used_words, not_used)

    def create2(self):
        wordlist_sorted = sorted(self.wordlist, reverse=True)
        wordlist = [x for x in np.random.choice(wordlist_sorted, 100)]

        g, wl, uw, nu = self.algo(self.grid[:], wordlist, [], [])
        self.used_words = uw
        self.grid = g

    def algo2(self, grid, wordlist, used_words, not_used):
        if len(wordlist) == 0:
            return grid, wordlist, used_words, not_used
        w = wordlist[0] # word to use

        # generate a position
        if len(used_words) == 0:
            # initial run
            pos_found = False
            its = 0
        else:
            pos_found = True

        while not pos_found and len(used_words) == 0:
            pos = np.random.randint((0,0), (self.height, self.width), 2)
            axis = np.random.randint(0,2)

            if self.__check_constraints(grid, w, pos, axis, used_words):
                if axis == 1: # 1 = downwards
                    grid[pos[0] : pos[0] + len(w), pos[1]] = list(w)
                else:
                    grid[pos[0], pos[1] : pos[1] + len(w)] = list(w)
                w.set_axis(axis)
                w.set_pos(pos)

                used_words.append(w)
                wordlist.remove(w)
                pos_found = True
                if len(wordlist) == 0:
                    return grid, wordlist, used_words, not_used
                w = wordlist[0] # new word
            else:
                its += 1

            if its == 100:
                # can not place word after many tries, skipping
                not_used.append(w)
                wordlist.remove(w)
                if len(wordlist) == 0:
                    return grid, wordlist, used_words, not_used
                w = wordlist[0]
                its = 0
        

        # iterate over all characters in this word
        found_one = False
        for i,c in enumerate(str(w)):
            for used_w in used_words:
                for j, used_c in enumerate(str(used_w)):
                    if used_c == c:
                        # we found a hit, get axis
                        axis = 1 - used_w.axis # will be 0 or 1
                        # calculate starting point
                        pos0, pos1 = 0, 0
                        if axis == 0:
                            pos0 = used_w.pos[0]
                            pos1 = used_w.pos[1] + j - i
                        else:
                            pos0 = used_w.pos[0] + j - i
                            pos1 = used_w.pos[1]
                        pos = (pos0, pos1)
                        if self.__check_constraints(grid, w, pos, axis, used_words):
                            if axis == 1: # 1 = downwards
                                grid[pos[0] : pos[0] + len(w), pos[1]] = list(w)
                            else:
                                grid[pos[0], pos[1] : pos[1] + len(w)] = list(w)
                            w.set_axis(axis)
                            w.set_pos(pos)

                            used_words.append(w)
                            wordlist.remove(w)

                            found_one = True
                            break
                if found_one:
                    break
            if found_one:
                break

        if not found_one:
            # skip this word because we can not place it
            not_used.append(w)
            wordlist.remove(w)

        return self.algo2(grid, wordlist, used_words, not_used)

    def create3(self):
        random.shuffle(self.wordlist)
        #wordlist_sorted = sorted(self.wordlist, reverse=True)

        g, wl, uw, nu = self.algo2(self.grid[:], self.wordlist, [], [])
        self.used_words = uw
        self.grid = g
    
    def hide_secret(self, loesung) -> bool:
        loesung = loesung.upper().replace("Ü", "UE").replace("Ö", "OE").replace("Ä", "AE")
        self.solution_positions = []
        added_indices = []
        for c in loesung:
            positions = (self.grid == c)

            if(not positions.any()):
                return False
            else:
                positions_all = np.argwhere(positions)
                index = np.random.randint(0, len(positions_all))

                while index in added_indices:
                    if len(positions_all) >= added_indices.count(index):
                        return False
                    index = np.random.randint(0, len(positions_all))
                added_indices.append(index)
                self.solution_positions.append(positions_all[index])
        return True
    
    def fitness(self):
        g = np.zeros((self.height, self.width))
        for w in self.used_words:
            if w.axis == 0:
                g[w.pos[0], w.pos[1] : w.pos[1] + len(w)] += 1.0
            else:
                g[w.pos[0] : w.pos[0] + len(w), w.pos[1]] += 1.0
        return np.linalg.norm(g)

    def get_grid(self):
        return self.grid