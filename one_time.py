import pymysql
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import math
import collections

db = pymysql.connect("localhost","root","12343249","sparsh" )
cursor = db.cursor()

def extract_from_database(query,column_list):
    sql = query
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    df = pd.DataFrame(data, columns=column_list)
    return df

org_ques_data = extract_from_database('select id ,title,answer_count , comment_count,view_count,modified_on from sparsh.questions',
                                      ['ID','Question','answer_count','comment_count','view_count','modified_on'])
org_ans_data = extract_from_database('select id ,text,question_id,modified_on , upvote_count , comment_count from sparsh.question_answers ',
                                     ['ID', 'Answers', 'question_id', 'modified_on', 'upvote_count', 'comment_count'])
org_keyword_data = extract_from_database('select entity_type , keyword from sparsh.keywords' , ['Entity','Keywords'])
org_filter_data = extract_from_database('select entity_type , filters from sparsh.filters' ,['Entity','Filter'])


stop_words = set(stopwords.words('english'))
def remove_stopwords(words):
    wx = [w for w in words if not w in stop_words]  ## Removing Stopwords
    return wx


def remove_duplicates(my_list):
    return list(set(my_list))


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


def words_from_keywords_filters(data,column_name):

    clean_questions = standardize_text(data, column_name)
    clean_questions = standardize_text(clean_questions,'Entity')
    tokenizer = RegexpTokenizer(r'\w+')
    clean_questions["tokens"] = clean_questions[column_name].apply(tokenizer.tokenize)   #Tokenization
    clean_questions['Entity'] = clean_questions['Entity'].apply(tokenizer.tokenize)
    clean_questions['tokens'] = clean_questions['tokens'] + clean_questions['Entity']
    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_duplicates)      # Removing Duplicates

    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_stopwords)       # Removing Stopwords

    return clean_questions


def words_from_question(data,column_name):

    clean_questions = standardize_text(data, column_name)

    tokenizer = RegexpTokenizer(r'\w+')

    clean_questions["tokens"] = clean_questions[column_name].apply(tokenizer.tokenize)   #Tokenization

    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_duplicates)      # Removing Duplicates

    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_stopwords)       # Removing Stopwords

    return clean_questions


words_keywords = words_from_keywords_filters(org_keyword_data , 'Keywords')
words_filters = words_from_keywords_filters(org_filter_data , 'Filters')
words_ques = words_from_question(org_ques_data,'Question')

def original(data):
    w = []
    for i in range(len(data.head())):
        w = w + data['tokens'][i]

    words = list(set(w))

    df = pd.DataFrame(words,columns=['Final_words'])
    return df


def keywords_filters(data):
    w = []
    for i in range(len(data)):
        print(i)
        w = w + data['tokens'][i]
    words = list(set(w))
    return words


def combine():
    word_k = keywords_filters(words_keywords)
    word_f = keywords_filters(words_filters)
    total = word_f + word_k
    total = list(set(total))
    df = pd.DataFrame(total,columns=['Final_filters'])
    df.to_csv('D:/ML/QNA_project/CSV_files/final_words_keys2.csv')
    return df

total_words_data = original(words_ques)  # TODO : data2
keys_data = combine()                     # TODO : data1


def add_to_dictionary():

    count = total_words_data['Total_words'].value_counts()

    w_keys = []
    for i in range(len(keys_data)):
        print(i)
        if i==79:
            print('sparsh')
            continue
        else:
            try:
                x = count[keys_data['Final_filters'][i]]
            except:
                x=0

        x = x + 2022459848
        x = str(x)
        s = keys_data['Final_filters'][i] + " " + x
        w_keys.append(s)

    m = {}
    for i in range(len(w_keys)-1):
        print("s {}".format(i))

        w = w_keys[i].split(' ')
        m[w[0]]=w[1]

    sorted_x = sorted(m.items(), key=lambda kv: int(kv[1]))
    sorted_dict = collections.OrderedDict(sorted_x)

    file = open('D:/ML/QNA_project/dictionary_words.txt','w')

    for key , value in sorted_dict.items():
        file.write(key+" "+value)
        file.write('\n')
    print('compelete')
    file.close()

    file1 = open('D:/ML/QNA_project/dictionary_words.txt' , 'r')
    data = file1.read().split('\n')
    file1.close()

    file1 = open('D:/ML/QNA_project/frequency_dictionary.txt' , 'r')
    data2 = file1.split('\n')
    file1.close()

    file2 = open('D:/ML/QNA_project/dictionary_final.txt' , 'w')
    for i in range(len(data)-1,-1,-1):
        file2.write(data[i])
        file2.write('\n')

    for i in range(len(data2)):
        file2.write(data2[i])
        file2.write('\n')
    file2.close()

db.close()