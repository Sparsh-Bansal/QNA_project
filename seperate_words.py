import pandas as pd
import re
import time


def original():

    data = pd.read_csv("D:/ML/QNA_project/CSV_files/words_total.csv")

    # t1 = time.time()
    s = ""
    # s = data.head()['tokens'].sum()
    print(data.head())
    for i in range(len(data.head())):
        print(i)
        s = s + data['tokens'][i]+" "
    s = s[:-1]

    print(s)
    # t2 = time.time()

    # print(t2-t1)

    s = re.sub('\[|\]|\,|\'', '', s)
    print(s)
    words = s.split(' ')
    print(words)
    df = pd.DataFrame(words,columns=['Total_words'])
    df.to_csv('D:/ML/QNA_project/CSV_files/final_words_total.csv')


    words = list(set(words))

    df2 = pd.DataFrame(words,columns=['Final_words'])
    df2.to_csv('D:/ML/QNA_project/CSV_files/final_words_total_rd.csv')



def keywords_filters(path_to_data):
    # data = pd.read_csv("D:/ML/QNA_project/CSV_files/words_filters.csv")
    data = pd.read_csv(path_to_data)
    # s = data.head()['tokens'].sum()
    s = ""
    print(data.head())
    for i in range(len(data)):
        print(i)
        s = s + data['tokens'][i]+" "
    s = s[:-1]
    # print(t2-t1)

    s = re.sub('\[|\]|\,|\'', '', s)
    words = s.split(' ')
    words = list(set(words))

    s2 = ""
    for i in range(len(data)):
        print(i)
        s2 = s2+data['Entity'][i]+" "

    s2=s2[:-1]


    words2 = s2.split(' ')
    words2 = list(set(words2))
    final = words +words2
    final = list(set(final))
    return final

def combine():
    word_k = keywords_filters('D:/ML/QNA_project/CSV_files/words_keywords.csv')
    word_f = keywords_filters('D:/ML/QNA_project/CSV_files/words_filters.csv')
    print(word_k)
    print(word_f)
    total = word_f + word_k
    total = list(set(total))
    df = pd.DataFrame(total,columns=['Final_filters'])
    df.to_csv('D:/ML/QNA_project/CSV_files/final_words_keys2.csv')


# original()
combine()