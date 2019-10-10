import pymysql
import pandas as pd

db = pymysql.connect("localhost","root","12343249","sparsh" )
cursor = db.cursor()

def ex_questions_answers(query,file_path):

   sql = query

   try:
      cursor.execute(sql)
      data = cursor.fetchall()
      db.commit()
   except:
      db.rollback()
#
#    file_ques = open('D:/ML/QNA_project/text_files/questions.txt','w')
#
#    for i in range(len(data)):
#       d = ('{}. '.format(i + 1) + data[i][0]).encode('utf-8')
#       file_ques.write(str(d))
#       file_ques.write('\n')
#
#    file_ques.close()
#
   o_d = [data[i][0] for i in range(len(data))]
   df = pd.DataFrame(o_d,columns=['Answers'])
   df.to_csv(file_path)


def extract_keywords_filter(query , file_path):
   sql = query
   try:

      cursor.execute(sql)
      data = cursor.fetchall()
      db.commit()
   except:
      db.rollback()

   o_d = [data[i] for i in range(len(data))]
   df = pd.DataFrame(o_d,columns=['Entity','Keywords'])
   df.to_csv(file_path)

def ex_view_count(query,file_path):

   sql = query

   try:
      cursor.execute(sql)
      data = cursor.fetchall()
      db.commit()
   except:
      db.rollback()

   df = pd.DataFrame(data, columns=['ID', 'Answers', 'question_id', 'modified_on', 'upvote_count', 'comment_count'])
   df.to_csv(file_path)


# ex_questions_answers('select text from sparsh.question_answers','D:/ML/QNA_project/CSV_files/answers.csv')
# ex_questions_answers('select title from sparsh.questions','D:/ML/QNA_project/CSV_files/answers.csv')
# extract_keywords_filter('select entity_type , keyword from sparsh.keywords ','D:/ML/QNA_project/CSV_files/keywords.csv')
ex_view_count('select id ,text,question_id,modified_on , upvote_count , comment_count from sparsh.question_answers ' , 'D:/ML/QNA_project/CSV_files/answers.csv')

db.close()