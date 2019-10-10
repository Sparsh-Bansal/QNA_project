import pandas as pd
import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import os
from symspellpy.symspellpy import SymSpell, Verbosity
from gensim.models import KeyedVectors
import time
from scipy import spatial

text = "Why upsee is making compulsory for the students to get admission in allotted college if they want to take part in fifth round counselling.."

t1 = time.time()
def remove_duplicates(my_list):
    return list(set(my_list))

stop_words = set(stopwords.words('english'))
def remove_stopwords(words):
    wx = [w for w in words if not w in stop_words]  ## Removing Stopwords
    return wx

def spell_correction(words):
    s = ""
    print(words)
    for i in words:
        suggestions = sym_spell.lookup(i, suggestion_verbosity,max_edit_distance_lookup)
        try:
            # print('hello')
            # print(suggestions[0].term)
            s = s + suggestions[0].term + " "
        except:
            # print('vhjyfhfy')
            s = s + i + " "
    s = s[:-1]
    print(s)
    w = s.split(' ')
    w = list(set(w))
    return w


def word_segmentation(words):
    print('started')
    final = words
    for i in words:
        input_term = i
        try:
            result = sym_spell.word_segmentation(input_term)
            w = (result.corrected_string).split(' ')

            print(w)
            w = w + final

        except:
            print('fail')
            pass
    try:
        w = list(set(w))
    except:
        print('YOYO')
        w = words
    print(w)
    return w

def preprocessing(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # get rid of URLs
    text = re.sub('[0-9]', "", text)
    text = re.sub(r'[{}@_*>()\\#%+=\[\]\-]',' ', text)
    text = re.sub('\(|\)|\[|\]',' ', text)
    text = re.sub('a0','', text)
    text = re.sub('\.','. ', text)
    text = re.sub('\!','! ', text)
    text = re.sub('\?','? ', text)
    text = re.sub(' +',' ', text)
    return text


def vectors(words):

    w = []
    for i in words:
        try:
            vector = model[i]
        except:
            vector = np.zeros(300)
            vector = vector.tolist()
        # print(vector.shape)
        w.append(vector)

    return w


def average_vector(vectors):
    v = np.zeros(300)
    x = np.zeros(300)
    n = len(vectors)
    for i in vectors:
        i = np.array(i)
        if (i==x).all():
            n = n - 1
        else:
            v = v + i
    v = v/n
    v = v.tolist()

    return v

text = preprocessing(text)

tokenizer = RegexpTokenizer(r'\w+')
words = tokenizer.tokenize(text)

words = remove_duplicates(words)

words = remove_stopwords(words)

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

words = spell_correction(words)



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

words = word_segmentation(words)



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

words = spell_correction(words)

words = remove_stopwords(words)


t1 =time.time()
model = KeyedVectors.load_word2vec_format('D:/ML/QNA_project/model/GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin', binary=True)
t2 = time.time()
print('model loaded in {} seconds'.format(t2-t1))
vs = vectors(words)


avg_v = average_vector(vs)

data = pd.read_csv('D:/ML/QNA_project/CSV_files/average_vectors.csv')
print('sparsh')




def match(s):
    s = re.sub('\[|\]|\,|\'', '', s)
    words = s.split(' ')
    vec1 = []
    for i in words:
        vec1.append(float(i))

    result = 1 - spatial.distance.cosine(vec1,avg_v)
    # print(result)
    return result

data['Similarity'] = data['Average_vector'].apply(match)
print(data.nlargest(5,['Similarity']))

dummy = data.nlargest(50,['Similarity'])
print(dummy['Question'].head(5))
print(time.time()-t1)

id = dummy.iloc[0]['ID']
id = int(id)

data_a = pd.read_csv('D:/ML/QNA_project/CSV_files/answers.csv')

req = data_a.loc[data_a['question_id']==id]

print(req.iloc[0]['Answers'])


# for i in range(len(dummy)):
