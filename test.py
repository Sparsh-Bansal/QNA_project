import pandas as pd

data = pd.read_csv('D:/ML/QNA_project/CSV_files/final_words_keys2.csv')
list2 = data['Final_filters'].to_list()

file = open('D:/ML/QNA_project/left_words.txt','r')
list1 = file.read().split('\n')
file.close()

w=[]
i=0
for item in list2:
    print(i)
    i=i+1
    if item in list1:
        continue
    else:
        w.append(item)

print(len(w))
df  = pd.DataFrame(w,columns=['Final_filters'])
df.to_csv('D:/ML/QNA_project/CSV_files/final_words_keys3.csv')