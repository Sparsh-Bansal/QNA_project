import pandas as pd
from symspellpy.symspellpy import SymSpell, Verbosity
import os

data1 = pd.read_csv('D:/ML/QNA_project/CSV_files/keywords.csv')
data2 = pd.read_csv('D:/ML/QNA_project/CSV_files/filters.csv')

ques = "I got 584 rank in JEE MAIns examintion"
ques = ques.lower()

max_edit_distance_dictionary = 2
prefix_length = 9
sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
dictionary_path = os.path.join(os.path.dirname(__file__), "dictionary_final.txt")
term_index = 0  # column of the term in the dictionary text file
count_index = 1  # column of the term frequency in the dictionary text file

if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
    print("Dictionary file not found")

max_edit_distance_lookup = 2
suggestion_verbosity = Verbosity.CLOSEST

suggestions = sym_spell.lookup(ques, suggestion_verbosity,max_edit_distance_lookup)
ques = suggestions[0].term

words = []
for i in range(len(data1)):
    str = data1['Keywords'][i]
    str = str.lower()
    if(ques.find(str,0,len(str))!=-1):
        words.append(str)

for i in range(len(data2)):
    str = data2['Filters'][i]
    str = str.lower()
    if(ques.find(str,0,len(str))!=-1):
        words.append(str)

