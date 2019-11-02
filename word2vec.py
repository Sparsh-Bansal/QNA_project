import pandas as pd
import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import os
from symspellpy.symspellpy import SymSpell, Verbosity
from gensim.models import KeyedVectors
import time

data = pd.read_csv('D:/ML/QNA_project/CSV_files/questions.csv')

def standardize_text(df, text_field):
    df[text_field] = df[text_field].str.lower()
    df[text_field] = df[text_field].apply(lambda elem: re.sub(r"http\S+", "", str(elem)))  # get rid of URLs
    df[text_field] = df[text_field].apply(lambda elem: re.sub('[0-9]', "", str(elem)))
    df[text_field] = df[text_field].apply(lambda elem: re.sub(r'[{}@_*>()\\#%+=\[\]\-]',' ', str(elem)))
    df[text_field] = df[text_field].apply(lambda elem: re.sub('\(|\)|\[|\]',' ', str(elem)))
    df[text_field] = df[text_field].apply(lambda elem: re.sub('a0','', str(elem)))
    df[text_field] = df[text_field].apply(lambda elem: re.sub('\.','. ', str(elem)))
    df[text_field] = df[text_field].apply(lambda elem: re.sub('\!','! ', str(elem)))
    df[text_field] = df[text_field].apply(lambda elem: re.sub('\?','? ', str(elem)))
    df[text_field] = df[text_field].apply(lambda elem: re.sub(' +',' ', str(elem)))
    return df


def remove_duplicates(my_list):
    return list(set(my_list))


def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
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

if __name__ == '__main__':
    clean_questions = standardize_text(data.head(), "Question")


    tokenizer = RegexpTokenizer(r'\w+')
    clean_questions["tokens"] = clean_questions["Question"].apply(tokenizer.tokenize)


    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_duplicates)      # Removing Duplicates


    stop_words = set(stopwords.words('english'))
    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_stopwords)


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
    clean_questions['tokens'] = clean_questions['tokens'].apply(spell_correction)

    # clean_questions.to_csv('D:/ML/QNA_project/CSV_files/main_spell1.csv')
    print('spell1 done')
    # clean_questions = pd.read_csv('D:/ML/QNA_project/CSV_files/main_spell1.csv')
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
    clean_questions['tokens'] = clean_questions['tokens'].apply(word_segmentation)
    # clean_questions.to_csv('D:/ML/QNA_project/CSV_files/main_word_seg.csv')
    print('wordseg done')

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
    clean_questions['tokens'] = clean_questions['tokens'].apply(spell_correction)


    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_stopwords)
    clean_questions['processed_words'] = clean_questions['tokens']
    # clean_questions.to_csv('D:/ML/QNA_project/CSV_files/main_spell2.csv')

    t1 =time.time()
    model = KeyedVectors.load_word2vec_format('D:/ML/QNA_project/model/GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin', binary=True)
    t2 = time.time()
    print('model loaded in {} seconds'.format(t2-t1))
    clean_questions['vectors'] = clean_questions['tokens'].apply(vectors)
    # clean_questions.to_csv('D:/ML/QNA_project/CSV_files/main_vectors.csv')


    clean_questions['Average_vector'] = clean_questions['vectors'].apply(average_vector)

    clean_questions = clean_questions.drop(['vectors','tokens'],axis=1)
    clean_questions.to_csv('D:/ML/QNA_project/CSV_files/main_average.csv')

    print(clean_questions['tokens'])
    print(type(clean_questions['tokens'][0]))

    print(clean_questions.head())


