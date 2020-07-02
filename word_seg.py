import os

from symspellpy.symspellpy import SymSpell  # import the module


def main():
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 0
    prefix_length = 7
    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__),"dictionary_final.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return

    # a sentence without any spaces
    input_term = "bangalore"
    # input_term = "thequickbrownfoxjumpsoverthelazydog"
    # input_term =  'universitycollegesbangalore'
    result = sym_spell.word_segmentation(input_term)
    x = result.corrected_string.split(' ')
    # display suggestion term, term frequency, and edit distance
    print(x)
    print("{}, {}, {}".format(result.corrected_string, result.distance_sum,
                              result.log_prob_sum))


if __name__ == "__main__":
    main()