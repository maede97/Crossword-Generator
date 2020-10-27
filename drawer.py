import matplotlib.pyplot as plt
from word import Word
import numpy as np

def draw(grid, used_words : [Word], loesung_pos) -> None:
    minx, miny, maxx, maxy = 100, 100, 0, 0
    for w in used_words:
        minx = min(minx, w.pos[1])
        maxx = max(maxx, w.pos[1] + len(w) * (1-w.axis))
        miny = min(miny, w.pos[0])
        maxy = max(maxy, w.pos[0] + len(w) * (w.axis))
    x = maxx
    y = maxy

    fig_sol = plt.figure(0, figsize=(maxx-minx, maxy-miny))
    ax = fig_sol.add_subplot(111)
    ax.set_aspect('equal')

    ax.set_xlim(minx, maxx)
    ax.set_ylim(maxy, miny)
    ax.set_xticks([],[])
    ax.set_yticks([],[])
    ax.set_axis_off()

    for x_ in range(minx,maxx+1):
        ax.plot([x_, x_], [miny, maxy], color="k", lw=1)
    for y_ in range(miny, maxy+1):
        ax.plot([minx, maxx], [y_, y_], color="k", lw=1)

    for w in used_words:
        s = str(w)
        p0,p1 = w.pos

        # create a fat line at the beginning and the end of this word
        if w.axis == 0:
            ax.plot([p1, p1], [p0, p0 + 1], color="k", lw=3)
            ax.plot([p1 + len(w), p1 + len(w)], [p0, p0 + 1], color="k", lw=3)
        else:
            ax.plot([p1, p1 + 1 ], [p0, p0], color="k", lw=3)
            ax.plot([p1, p1 + 1 ], [p0 + len(w), p0 + len(w)], color="k", lw=3)

        for i,c in enumerate(s):
            ax.annotate(c, (p1 + (1-w.axis) * i + 0.35, p0 + w.axis * i + 0.6), fontsize="xx-large")
    
    #fig_sol.tight_layout()
    plt.savefig("solution.png",bbox_inches='tight',dpi=100)

    # create challenge figure

    fig_challenge = plt.figure(1, figsize=(maxx-minx, maxy-miny))
    ax = fig_challenge.add_subplot(111)
    ax.set_aspect('equal')

    ax.set_xlim(minx, maxx)
    ax.set_ylim(maxy, miny)
    ax.set_xticks([],[])
    ax.set_yticks([],[])
    ax.set_axis_off()

    for x_ in range(minx,maxx+1):
        ax.plot([x_, x_], [miny, maxy], color="k", lw=1)
    for y_ in range(miny, maxy+1):
        ax.plot([minx, maxx], [y_, y_], color="k", lw=1)

    # store all positions
    pos_numbers = {}

    vertical = []
    horizontal = []

    for w in used_words:
        s = str(w)
        p0,p1 = w.pos
        key = p0 * x + p1
        if key in pos_numbers:
            pos_numbers[key].append(w)
        else:
            pos_numbers[key] = []
            pos_numbers[key].append(w)

        # create a fat line at the beginning and the end of this word
        if w.axis == 0:
            ax.plot([p1, p1], [p0, p0 + 1], color="k", lw=3)
            ax.plot([p1 + len(w), p1 + len(w)], [p0, p0 + 1], color="k", lw=3)
        else:
            ax.plot([p1, p1 + 1 ], [p0, p0], color="k", lw=3)
            ax.plot([p1, p1 + 1 ], [p0 + len(w), p0 + len(w)], color="k", lw=3)

    delim = ": "

    for i,k in enumerate(sorted(pos_numbers.keys())):
        ax.annotate(str(i+1), (pos_numbers[k][0].pos[1] + 0.35, pos_numbers[k][0].pos[0] + 0.6),fontsize="xx-large")

        for w in pos_numbers[k]:
            if w.axis == 0:
                horizontal.append(str(i+1) + delim + w.clue)
            else:
                vertical.append(str(i+1) + delim + w.clue)
    for c in loesung_pos:
        ax.plot(c[1] + 0.5, c[0] + 0.5, 'o', ms=40, mec='b', mfc='none', mew=2)
    with open("clues.txt", "w") as wr:
        wr.write("Waagrecht:\n" + "\n".join(horizontal)+"\n\nSenkrecht:\n" + "\n".join(vertical)+"\n\nDas Lösungswort ist in den markierten Feldern und muss noch in die Richtige Reihenfolge gebracht werden.")

    plt.savefig("challenge.png",bbox_inches='tight',dpi=100)
