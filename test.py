import pandas as pd
import numpy as np

id = 4545

data = pd.read_csv('D:/ML/QNA_project/CSV_files/answers.csv')

req = data.loc[data['question_id']==id]

max = -1
id = req.iloc[0]['ID']
date = req.iloc[0]['modified_on']

for i in range(len(req)):
    up_c = int(req.iloc[i]['upvote_count'])
    cm_c = int(req.iloc[i]['comment_count'])
    d1 = req.iloc[i]['modified_on']
    if up_c + cm_c > max:
        max = up_c + cm_c
        id = req.iloc[i]['ID']
    if up_c == cm_c:
        if d1 > date:
            date = d1

