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
from datetime import datetime

import sys

print(sys.stdout.encoding)
print(u"Stöcker".encode(sys.stdout.encoding, errors='replace'))
print(u"Стоескер".encode(sys.stdout.encoding, errors='replace'))

model = KeyedVectors.load_word2vec_format('D:/ML/QNA_project/model/GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin', binary=True)
print('Model Loaded')
keyword_data = pd.read_csv('D:/ML/QNA_project/CSV_files/keywords.csv')
filter_data = pd.read_csv('D:/ML/QNA_project/CSV_files/filters.csv')
keys_data = pd.read_csv('D:/ML/QNA_project/CSV_files/final_words_keys2.csv')
answer_data = pd.read_csv('D:/ML/QNA_project/CSV_files/answers.csv')
vector_data = pd.read_csv('D:/ML/QNA_project/CSV_files/final_question_vector.csv')
print('All CSV Files readed')


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
        suggestions = sym_spell.lookup(i, suggestion_verbosity, max_edit_distance_lookup)
        try:
            s = s + suggestions[0].term + " "
        except:
            s = s + i + " "
    s = s[:-1]
    print(s)
    w = s.split(' ')
    w = list(set(w))
    return w


def word_segmentation(words):
    final = []
    for i in words:
        input_term = i
        try:
            result = sym_spell.word_segmentation(input_term)
            w = (result.corrected_string).split(' ')
            final = final + w
        except:
            pass
    final = list(set(final))
    print('Segmented')
    print(final)
    return final


def preprocessing(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # get rid of URLs
    text = re.sub('[0-9]', "", text)
    text = re.sub(r'[{}@_*>()\\#%+=\[\]\-]', ' ', text)
    text = re.sub('\(|\)|\[|\]', ' ', text)
    text = re.sub('a0', '', text)
    text = re.sub('\.', '. ', text)
    text = re.sub('\!', '! ', text)
    text = re.sub('\?', '? ', text)
    text = re.sub(' +', ' ', text)
    return text


def vectors(words):
    w = []
    for i in words:
        try:
            vector = model[i]
        except:
            vector = np.zeros(300)
            vector = vector.tolist()
        w.append(vector)
    return w


def average_vector(vectors):
    v = np.zeros(300)
    x = np.zeros(300)
    n = len(vectors)
    for i in vectors:
        i = np.array(i)
        if (i == x).all():
            n = n - 1
        else:
            v = v + i
    v = v / n
    v = v.tolist()
    return v


def match(s):
    s = re.sub('\[|\]|\,|\'', '', s)
    words = s.split(' ')
    vec1 = []
    for i in words:
        vec1.append(float(i))

    result = 1 - spatial.distance.cosine(vec1, avg_v)
    return result

def common_keywords(text_q):
    print(w_in_ques)
    # text_q = text_q.lower()
    # w = text_q.split(' ')
    #
    # max_edit_distance_dictionary = 2
    # prefix_length = 9
    # sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    # dictionary_path = os.path.join(os.path.dirname(__file__), "dictionary_final.txt")
    # term_index = 0  # column of the term in the dictionary text file
    # count_index = 1  # column of the term frequency in the dictionary text file
    #
    # if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
    #     print("Dictionary file not found")
    #
    # max_edit_distance_lookup = 2
    # suggestion_verbosity = Verbosity.CLOSEST
    #
    # ques = ""
    # for input in w:
    #     suggestions = sym_spell.lookup(input, max_edit_distance_lookup)
    #     try:
    #         ques = ques + suggestions[0].term + " "
    #     except:
    #         ques = ques + input + " "
    # ques = ques + text_q
    # print(ques)

    # input_ques = text_cw
    # input_ques = input_ques.lower()
    # words_input = input_ques.split(' ')
    #
    # in_ques = ''
    # for input in words_input:
    #     suggestions = sym_spell.lookup(input, max_edit_distance_lookup)
    #     try:
    #         in_ques = in_ques + suggestions[0].term + " "
    #     except:
    #         in_ques = in_ques + input + " "
    # in_ques = in_ques + input_ques
    # print(in_ques)

    text_q = preprocessing(text_q)

    tokenizer = RegexpTokenizer(r'\w+')
    words_cw = tokenizer.tokenize(text_q)

    words_cw = remove_duplicates(words_cw)

    words_cw = remove_stopwords(words_cw)

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

    words_cw = spell_correction(words_cw)

    max_edit_distance_dictionary = 0
    prefix_length = 7
    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__), "dictionary_final.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")

    words_cw = word_segmentation(words_cw)

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

    words_cw = spell_correction(words_cw)

    words_cw = remove_stopwords(words_cw)

    w_ques = words_cw
    print(w_ques)
    w1 = []
    w2 = []
    # for i in range(len(keyword_data)):
    #     str = keyword_data['Keywords'][i]
    #     str = str.lower()
    #     if (ques.find(str, 0, len(str)) != -1):
    #         w1.append(str)
    #     if (in_ques.find(str, 0, len(str)) != -1):
    #         w2.append(str)
    #
    # for i in range(len(filter_data)):
    #     str = filter_data['Filters'][i]
    #     str = str.lower()
    #     if (ques.find(str, 0, len(str)) != -1):
    #         w1.append(str)
    #     if (in_ques.find(str, 0, len(str)) != -1):
    #         w2.append(str)

    for i in range(len(keys_data)):
        ss = keys_data['Final_filters'][i]
        # print(i)
        ss = str(ss)
        ss = ss.lower()
        # w_ques = ques.split()
        # w_ques = list(set(w_ques))
        # w_in_ques = in_ques.split()
        # w_in_ques = list(set(w_in_ques))
        if ss in w_ques:
            w1.append(ss)
        if ss in w_in_ques:
            w2.append(ss)


    common = w2 + w1
    common_d = list(set(common))
    x = len(common) - len(common_d)
    print(common)
    print(common_d)
    print(x)
    return x


def common_keyword_new(s):
    s = re.sub('\[|\]|\,|\'', '', s)
    w_ques = s.split(' ')
    print(w_ques)
    print(w_in_ques)
    w1=[]
    w2=[]
    for i in range(len(keys_data)):
        ss = keys_data['Final_filters'][i]
        # print(i)
        ss = str(ss)
        ss = ss.lower()
        if ss in w_ques:
            w1.append(ss)
        if ss in w_in_ques:
            w2.append(ss)


    common = w2 + w1
    common_d = list(set(common))
    x = len(common) - len(common_d)
    print(common)
    print(common_d)
    print(x)
    return x

def getting_answer(final):
    answers_list = []
    for j in range(len(final)):
        id = final.iloc[j]['ID']
        id = int(id)
        try:
            req = answer_data.loc[answer_data['question_id'] == id]
            max = -1
            id = req.iloc[0]['ID']

            for i in range(len(req)):
                up_c = int(req.iloc[i]['upvote_count'])
                cm_c = int(req.iloc[i]['comment_count'])
                if up_c + cm_c > max:
                    max = up_c + cm_c
                    id = req.iloc[i]['ID']

            ans = req.loc[id-1]['Answers']
            answers_list.append(ans)
        except:
            answers_list.append("Answer not available")
    return answers_list

j=0
while True:
    # text = "Why upsee is making compulsory for the students to get admission in allotted college if they want to take part in fifth round counselling.."
    text = input("Enter Your Question: ")
    t1 = time.time()
    text_cw = text


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
    dictionary_path = os.path.join(os.path.dirname(__file__), "dictionary_final.txt")
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
    w_in_ques = words
    vs = vectors(words)

    avg_v = average_vector(vs)

    # TODO : 1. correction. 2, Make Generic thru user input
    now_date = datetime.now()
    now_date = now_date.strftime("%d/%m/%Y %H:%M:%S")
    filter_date_q = now_date

    vector_data['Similarity'] = vector_data['Average_vector'].apply(match)

    # vector_data = vector_data[vector_data['modified_on']<filter_date_q]


    # TODO : Make "30" configurable
    dummy = vector_data.nlargest(30, ['Similarity'])

    dummy['common_keyword'] = dummy['processed_words'].apply(common_keyword_new)
    min_kw = min(dummy['common_keyword'])
    max_kw = max(dummy['common_keyword'])
    if (max_kw != min_kw):
        dummy['common_keyword'] = (dummy['common_keyword'] - min_kw) / (max_kw - min_kw)
    else:
        dummy['common_keyword'] = 0
    print(dummy['common_keyword'].head())

    dummy['sum3'] = dummy['view_count'] + dummy['answer_count'] + dummy['comment_count']
    # TODO : Make normalize function
    min_s = min(dummy['sum3'])
    max_s = max(dummy['sum3'])
    dummy['sum3'] = (dummy['sum3'] - min_s) / (max_s - min_s)

    margin = 0.02
    keyword_wt = 70
    sum_wt = 30
    w1 = 1
    w2 = margin * keyword_wt / 100
    w3 = margin * sum_wt / 100

    dummy['final_score'] = (w1 * dummy['Similarity']) + (w2 * dummy['common_keyword']) + (w3 * dummy['sum3'])
    print(dummy['final_score'].head())
    final = dummy.nlargest(10, ['final_score'])
    print(final.head())
    print(final['Question'].head())

    ans_list = getting_answer(final)

    final['Answers'] = ans_list

    final = final.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Average_vector', 'answer_count', 'comment_count', 'view_count'],
                       axis=1)

    print(final.columns)
    print(final['Answers'].head())

    results_file = open("Results{}.txt".format(j), "w")
    j=j+1
    for i in range(len(final)):
        print("{} Question".format(i + 1))
        results_file.write("{} Question\n".format(i + 1))
        print(final.iloc[i]["Question"])
        results_file.write(final.iloc[i]["Question"] + '\n')
        print("Similarity Score : {}".format(final.iloc[i]['final_score']))
        results_file.write("Similarity Score : {}\n".format(final.iloc[i]['final_score']))
        print('Answer')
        results_file.write('Answer\n')
        print(final.iloc[i]['Answers'])
        results_file.write(final.iloc[i]['Answers']+'\n')

    results_file.close()
    print(time.time() - t1)
