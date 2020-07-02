# QNA Project (A major NLP Project):

As we all know , after passing 12th Grade , one has to appear and clear his/her respective examination for higher studies (JEE for Engineering , NEET for Medical,BBA,MTech etc. etc.).

There are lot of questions thats comes in our mind and we do extensive google searching to get our answers, like (Previous year ranks, Placement , Fees ,which college is best for our rank etc etc ..thousands of questions).

So here is a NLP based BOT trained on huge question/answers dataset to give the best/most appropriate answer of all the questions about colleges in every field.


# Process:
1. Data Preprocessing (M. IMP).
2. Storing Vectors of questions and words in to a dictionary.
3. Spell Correction and Word Segmentation on the input question.
4. Finding Cosine Similarity between vectors(to find Top 30 answers).
5. Best Answer is calculated by :
	w1*(Similarity) + w2*(Upvote count on answers) + w3*(number of common words)


# Files : 

add_words_dictionary.py : This file add important specific words from the dataset into a dictionary for Spell Correction and Word Segmentation . dictionary_final.txt(contains                               original words + words from the dataset)

correction_count.py :  To check the accuracy of SymSpell Correction /           
                      Word Segmentation after training on the dataset (Accuracy : 85%)

extract_database.py : To extract CSV files from the SQL database.

matching.py : Single question to answer main file

testing.py : Main file which calls all other files(includes the main code) 
			       Run Command : python testing.py 

one_time.py : One Can auto train a updated dataset by running this file.

preprocessing_original_question.py : Data(Question-Answers) Preprocessing

server.py : Flask Application(Deploy the model on web server).

separate_words.py : Data Processing

word2vec.py : Convert Each question into a Single Vector
               Download the Google Word to vector model(GoogleNews-vectors-negative300.bin) trained on News Dataset(4.92GB)

# Results:

Some Results are Shown below ....A same question is asked in a different way with a lot of speling mistakes 

a) Question : 

1. What is the total fee of VIT VELLORE of 4 year
2. annual fees of vit velor..??????
3. can you tellme totalfees of vitvellore in 2019.
4. VIT VELLLOre1 totalannual fees..of full year....?????

Answer : 
Total fees will be around 12-13 lacs while u r in category 1 it's including hostel and mess fees. And for category 2 it will be around 16-17 lacs.&nbsp; 1-2 lac increases as category increases...



b) Question :

1. What is the registration date of bba entrance
2. entrance registration date(BBA)..??
3. can you tell me the regstrtion examdate of bba.....

Answer :
The application form will be tenatively available in third week of February 2019.Application closes on first week of May 2019.The application mode will be available online . Thanks




c) Question
1. what is the fees structure for B tech , computer science including hostel fee in lmnit jaipur
2. Feesstructure (B.tech) in computerscience in LMNIT jaipurrr..???
3. btech fees struture in LMNIT jaipur coputer scince...???

Answer : 
It is genereally same fee for all branches in a college.And it is 1,78,000 for first semester.Please go through the below link for the fee structure of LNMIIT, Jaipur:- https://www.lnmiit.ac.in/Admissions/ugadmissions/Fee_Structure.html . Hope you found this helpful...!!!. All the best...!!!



d) Question : 

1. where can i get the refund list of neet 2019
2. if i dont want to take admissssssion , How can i get the 		reefund after neet counceling.... ..???

Answer: 

Refund Procedure : If candidate do not wish to pursue the study in college after 2nd round of counselling in this case only refund is initiated.Aspirants get their amount refunded on the same account through which they had submitted their fee.
And once all the rounds of Counselling are completed, MCI will release the list of the Xandidated eligible for the refund of the Security deposit at their official website at mcc.nic.in.
However candidate has to contact on MCC tollfree no and drop a mail to their finance department.This is the only way a candidate may get a refund. Hope this help you aspirants.


e) Question : 

1. Previous year rank od computer science branch in different NIT's
2. tell me the previos year ranks of computerscience brnch in all (NIT))))>>>...?????????? 

Answer:

Following is the 2018 JEE MAIN cutoff for Computer Science for some NITs:-
NIT Warangal : 1745
NIT Suratkhal : 1767
NIT Trichy : 1140
MNNIT Allahbad : 3504
NIT Rourkela : 3576
NIT Calicut : 4822
NIT Durgapur : 8516
NIT Hamirpur : 15821
MANIT Bhopal : 6827
MANIT Jaipur : 4875
Hope this helps :)
Best of luck!

f) Question :

1. my mat score September 735.50 get my chance of good MBA college
2. what are the chancesof geting gud mba colllegee ,,,, my score 	is around 700.

Answer :

Yes you have a good MAT score and you stand a good chance in getting colleges in Bengaluru (Your profile looks great, wait for the moment )

https://bschool.careers360.com/articles/mat-cutoff
Cutoff reports and college information shared above.


# Conclusion :

Results are Pretty Good .

Average time for Question with enough imformation (13-18 sec)

Average time for questions with a little imformation (25-30 sec)
