import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re

data = pd.read_csv('D:/ML/QNA_project/CSV_files/questions.csv')

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
# print(data.head())

def from_questions_csv():

    data = pd.read_csv('D:/ML/QNA_project/CSV_files/questions.csv')
    clean_questions = standardize_text(data, "Question")
    # print(clean_questions.head())
    tokenizer = RegexpTokenizer(r'\w+')
    clean_questions["tokens"] = clean_questions["Question"].apply(tokenizer.tokenize)   #Tokenization
    clean_questions.to_csv('D:/ML/QNA_project/CSV_files/words_total.csv')

    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_duplicates)      # Removing Duplicates
    clean_questions.to_csv('D:/ML/QNA_project/CSV_files/words_after_removing_duplicates.csv')

    stop_words = set(stopwords.words('english'))
    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_stopwords)       # Removing Stopwords
    clean_questions.to_csv('D:/ML/QNA_project/CSV_files/words_after_removing_stopwords.csv')

    print(clean_questions.head())

def from_keywords_filters_csv():

    clean_questions = standardize_text(data, "Entity")
    clean_questions = standardize_text(data, "Filters")

    # print(clean_questions.head())
    tokenizer = RegexpTokenizer(r'\w+')

    clean_questions["tokens"] = clean_questions["Filters"].apply(tokenizer.tokenize)  # Tokenization

    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_duplicates)  # Removing Duplicates

    clean_questions['tokens'] = clean_questions['tokens'].apply(remove_stopwords)  # Removing Stopwords

    clean_questions.to_csv('D:/ML/QNA_project/CSV_files/words_filters.csv')

    print(clean_questions.head())