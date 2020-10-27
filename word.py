from functools import total_ordering

@total_ordering
class Word:
    def __init__(self, clue, solution):
        self.clue = clue
        self.solution = solution.upper().replace("Ü", "UE").replace("Ö", "OE").replace("Ä", "AE")

        self.pos = (-1, -1)
        self.axis = -1

    def set_pos(self, p):
        self.pos = p

    def set_axis(self, a):
        self.axis = a
    
    def __len__(self) -> int:
        return len(self.solution)

    def __str__(self) -> str:
        return self.solution

    def __repr__(self) -> str:
        return "Word('" + self.clue + "','" + self.solution + "', " + str(self.pos) + ", " + str(self.axis) + ")"

    def __eq__(self, other) -> bool:
        return self.clue == other.clue and self.solution == other.solution
    
    def __lt__(self, other) -> bool:
        return len(self) < len(other)

    def __iter__(self):
        for elem in list(self.solution):
            yield elem