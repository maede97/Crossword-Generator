from word import Word
# Holds words from a category

class Category:
    def __init__(self, name : str):
        self.words = []
        self.name = name # category name

    def add_word(self, w : Word) -> None:
        """ add a word to this category """
        self.words.append(w)

    def get_words(self) -> [Word]:
        """ returns all words in this category """
        return self.words

    def get_word_by_clue(self, clue : str) -> Word:
        """ returns the word given a clue """
        for w in self.words:
            if w.clue == clue:
                return w
        print("Error: Word not found.")
        return None
    
    def get_word(self, sol : str) -> Word:
        """ returns the word given the solution """
        for w in self.words:
            if str(w) == sol:
                return w
        print("Error: Word not found.")
        return None


    def __str__(self) -> str:
        return self.name

    def __len__(self) -> int:
        return len(self.words)
