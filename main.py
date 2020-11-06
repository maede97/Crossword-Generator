from loader import DataLoader
from crossword import Crossword
from drawer import draw
import copy

DOWNLOAD_NEW = False
SIZE=18
ITERATIONS = 1000

CREATE_NEW = True
EDIT_OLD = True
loesung = "Weihnachten"

if CREATE_NEW:

    dl = DataLoader()
    if DOWNLOAD_NEW:
        dl.load_data_from_web()
        dl.store_to_file("data.pickle")
    dl.load_from_file("data.pickle")
    cats = dl.get_categories()
    words = []
    for c in cats:
        words.extend(c.get_words())

    best_fit = 0
    best_cw = None
    iters = 0
    while iters < ITERATIONS:
        cw = Crossword(SIZE, SIZE)
        cw.set_wordlist(words)
        cw.create3(shuffle=True)
        print("Created crossword with fitness", cw.fitness())
        if cw.fitness() > best_fit:
            best_fit = cw.fitness()
            best_cw = copy.deepcopy(cw)
            print("New best:", best_fit)
        del cw
        iters += 1
    if best_cw == None:
        print("Error: could not create a single crossword puzzle")
        exit(-1)
    print("Used words:", best_cw.get_used_words())
    print("Grid:")
    print(best_cw.get_grid())
    print("Fitness:", best_fit)

    print("TOTAL WORDS:",len(words))

    #draw(best_cw.get_grid(), best_cw.used_words, best_cw.solution_positions)

    best_cw.store_grid("intermediate_store.txt")

if EDIT_OLD:
    cw = Crossword(SIZE, SIZE)
    cw.set_wordlist(words)
    cw.load_grid("intermediate_store.txt")

    cw.hide_secret(loesung)

    draw(cw.get_grid(), cw.used_words, cw.solution_positions)

else:
    print("Doing nothing...")