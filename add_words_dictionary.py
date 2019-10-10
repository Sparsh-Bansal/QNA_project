import pandas as pd
import math
import collections

data1 = pd.read_csv('D:/ML/QNA_project/CSV_files/final_words_keys.csv')  # Keywords

data2 = pd.read_csv('D:/ML/QNA_project/CSV_files/final_words_total2.csv')  # Questions

count = data2['Total_words'].value_counts()
file = open('D:/ML/QNA_project/dictionary_words.txt','w')

for i in range(len(data1)):
    print(i)
        # if math.isnan(float('nan'))==math.isnan(float(data1['Final_filters'][i])):
    # if str(data1['Final_filters'][i])=='nan':
    if i==79:
        print('sparsh')
        # x = count(str(data1['Final_filters'][i]))
        # x=0
        continue
    else:
        try:
            x = count[data1['Final_filters'][i]]
        except:
            x=0

    x = x + 2022459848
    x = str(x)
    s = data1['Final_filters'][i] + " " + x
    file.write(s)
    file.write('\n')

file.close()


file = open('D:/ML/QNA_project/dictionary_words.txt','r')
data = file.read().split('\n')
file.close()
m = {}
for i in range(len(data)-1):
    print("s {}".format(i))

    w = data[i].split(' ')
    m[w[0]]=w[1]

sorted_x = sorted(m.items(), key=lambda kv: int(kv[1]))
print('hgfhg')
sorted_dict = collections.OrderedDict(sorted_x)

file2 = open('D:/ML/QNA_project/dictionary_words.txt','w')

for key , value in sorted_dict.items():
    file2.write(key+" "+value)
    file2.write('\n')
print('compelete')
file2.close()

file1 = open('D:/ML/QNA_project/dictionary_words.txt','r')
file2 = open('D:/ML/QNA_project/final_dictionary.txt','w')
data = file1.read().split('\n')
file1.close()
for i in range(len(data)-1,-1,-1):
    file2.write(data[i])
    file2.write('\n')

file2.close()