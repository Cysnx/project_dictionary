import pandas as pd
import random
import os
import time

df=pd.read_csv("items.txt",sep=';')

#print(df["meaning"][14])
#print(len(df["word"]))
SIZE_DICT=len(df["word"])
num=random.randint(0,len(df["word"])-1)

c_response=0
w_response=0
num_old=[]
response=""


if os.path.exists("learn_matrix.txt"):
    learn_matrix=pd.read_csv("learn_matrix.txt",sep=';')
else:
    learn_matrix=pd.DataFrame(columns=["word","c_response","w_response","w/c ratio"])

while True:
    print(f"What is the word ({df['type'][num]}) for the following: {df['meaning'][num]}")
    response=input("")
    if response=="exit":
        break
    elif response==df["word"][num]:
        if df["word"][num] in learn_matrix["word"].values:
            learn_matrix.loc[learn_matrix["word"]==df["word"][num],"c_response"]+=1
        else:
            learn_matrix.loc[len(learn_matrix)]=[df["word"][num],0,0,0.0]
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "c_response"] += 1
        print("Correct!")
    else:
        if df["word"][num] in learn_matrix["word"].values:
            learn_matrix.loc[learn_matrix["word"]==df["word"][num],"w_response"]+=1
        else:
            learn_matrix.loc[len(learn_matrix)]=[str(df["word"][num]),0,0,0.0]
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w_response"] += 1
        print("Wrong. Correct answer is: ",df["word"][num])
    learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w/c_ratio"] =learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w_response"]/(1+learn_matrix.loc[learn_matrix["word"] == df["word"][num], "c_response"])
    num_old.append(num)
    num=random.randint(0,len(df["word"])-1)
print(learn_matrix)
print(num_old)
learn_matrix.to_csv("learn_matrix.txt",sep=";",index=False)