import os

from symspellpy.symspellpy import SymSpell  # import the module


def main():
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 7
    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)

    # create dictionary using corpus.txt
    if not sym_spell.create_dictionary('D:/ML/QNA_project/corpus.txt'):
        print("Corpus file not found")
        return

    for key, count in sym_spell.words.items():
        print("{} {}".format(key, count))


if __name__ == "__main__":
    main()