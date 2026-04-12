import pandas as pd
import os
from datetime import datetime
from learning_method import power_law
from learn_matrix_update import update_lm
from randomness import randomness
from items_lm_comparison import update_source
from time_series_imp import time_series_imp

# Reading the main input file.
df=pd.read_csv("items.txt",sep=';')

N_OF_EXERCISES=25

c_response=0
w_response=0
num_old=[]
response=""

#Check whether a learn matrix exist or not. If not, create one.
if os.path.exists("learn_matrix.txt"):
    update_source()
    learn_matrix=pd.read_csv("learn_matrix.txt", sep=';')
else:
    learn_matrix=pd.DataFrame(columns=["word","c_response","w_response","w/c_ratio","datetime_seen_first","datetime_last_c_response","p_law"])

update_lm() # Update the learn matrix before the actual study.

num=int(df.loc[df['word']==randomness(learn_matrix)].index[0]) # find the index number belongs to dataframe from learn matrix
row = learn_matrix.loc[learn_matrix["word"] == df["word"][num]].iloc[0]

for i in range(0,N_OF_EXERCISES):
    print(f"What is the word ({df['type'][num]}) for the following: {df['meaning'][num]}")
    response=input("")
    if response=="exit":
        break
    elif response==df["word"][num]: # correct answer
        learn_matrix.loc[learn_matrix["word"]==df["word"][num],"c_response"]+=1 # update the number of correct answers
        learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"] = power_law(
            row["c_response"],
            row["w_response"],
            row["datetime_last_c_response"]
        )
        learn_matrix.loc[learn_matrix["word"] == df["word"][num], "datetime_last_c_response"] =datetime.now().isoformat() # update the datetime of last correct answer.
        print("Correct!")
    else:    # wrong answer
        learn_matrix.loc[learn_matrix["word"]==df["word"][num],"w_response"]+=1 # update the number of wrong answers
        learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"] = power_law(
            row["c_response"],
            row["w_response"],
            row["datetime_last_c_response"]
        )
        print("Wrong. Correct answer is: ",df["word"][num])

    learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w/c_ratio"]=round(learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w_response"]/(1+learn_matrix.loc[learn_matrix["word"] == df["word"][num], "c_response"]),4)
    num_old.append(num)
    learn_matrix.to_csv("learn_matrix.txt", sep=";", index=False)
    time_series_imp(df["word"][num],float(learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"].values[0]))
    update_lm() # update after
    num=int(df.loc[df['word']==randomness(learn_matrix)].index[0])
    a=0
    for n in num_old:
        while n==num:
            print('alert') # need a fix here: it cannot stay like this.
            num = int(df.loc[df['word'] == randomness(learn_matrix)].index[0]) # fix required.
            a=a+1
            if a>100:
                break
    row = learn_matrix.loc[learn_matrix["word"] == df["word"][num]].iloc[0]
#print(learn_matrix)
print(num_old)


