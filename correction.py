import os
import pandas as pd
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

def main():
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 9
    data = pd.read_csv('D:/ML/QNA_project/CSV_files/final_words_total_rd2.csv')

    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__),"frequency_dictionary_en_82_765.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return
    # lookup suggestions for single-word input strings

    # input_term = "agricultr"  # misspelling of "members"
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_edit_distance_dictionary)
    max_edit_distance_lookup = 2

    suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
    s = ""
    print('original')
    # print(len(words))
    for i in range(len(data)):
        # print(i)
        if i==0 or i==51124 or i==65070:
            continue
        input_term = data['Final_words'][i]
        suggestions = sym_spell.lookup(input_term, suggestion_verbosity,
                                   max_edit_distance_lookup)
        print(i)
        try:
            s = s + str(suggestions[0].term)+" "
        except:
            s = s+ input_term

    s = s[:-1]
    words = s.split(' ')
    # print(len(words))
    print('After')
    print(len(words))
    # for suggestion in suggestions:
    #     print("{}, {}, {}".format(suggestion.term, suggestion.distance,
    #                               suggestion.count))

    # lookup suggestions for multi-word input strings (supports compound
    # splitting & merging)
    # input_term = ("whereis th elove hehad dated forImuch of thepast who "
    #               "couqdn'tread in sixtgrade and ins pired him")
    # # input_term = 'he lives in bngalre'
    # max_edit_distance_lookup = 2
    # suggestions = sym_spell.lookup_compound(input_term,
    #                                         max_edit_distance_lookup)
    # for suggestion in suggestions:
    #     print("{}, {}, {}".format(suggestion.term, suggestion.distance,
    #                               suggestion.count))
if __name__ == "__main__":
    main()