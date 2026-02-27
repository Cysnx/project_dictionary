import pandas as pd
import random
import os
from datetime import datetime
from learning_method import power_law
from learn_matrix_update import update_lm
from randomness import randomness
df=pd.read_csv("items.txt",sep=';')



c_response=0
w_response=0
num_old=[]
response=""

if os.path.exists("learn_matrix.txt"):
    learn_matrix=pd.read_csv("learn_matrix.txt", sep=';')
else:
    learn_matrix=pd.DataFrame(columns=["word","c_response","w_response","w/c_ratio","datetime_seen_first","datetime_last_c_response","p_law"])

update_lm()
num=int(df.loc[df['word']==randomness(learn_matrix)].index[0])
row = learn_matrix.loc[learn_matrix["word"] == df["word"][num]].iloc[0]
while True:
    print(f"What is the word ({df['type'][num]}) for the following: {df['meaning'][num]}")
    response=input("")
    if response=="exit":
        break
    elif response==df["word"][num]: # doğru cevap
        if df["word"][num] in learn_matrix["word"].values: # eğer kaydı VAR ise
            learn_matrix.loc[learn_matrix["word"]==df["word"][num],"c_response"]+=1 # doğru cevap sayısını güncelle

            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"] = power_law(
                row["c_response"],
                row["w_response"],
                row["datetime_last_c_response"]
            )
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "datetime_last_c_response"] =datetime.now().isoformat() # son doğru cevap tarihini güncelle
        else: # eğer kaydı YOK ise
            learn_matrix.loc[len(learn_matrix)]=[df["word"][num],0,0,0.0,datetime.now().isoformat(),datetime.now().isoformat(),0] # kaydını oluştur
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "c_response"] += 1 # doğru cevap sayısını güncelle
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"] = power_law(
                row["c_response"],
                row["w_response"],
                row["datetime_last_c_response"]
            )
            #learn_matrix.loc[learn_matrix["word"] == df["word"][num], "datetime_last_c_response"] =datetime.now().isoformat()
        print("Correct!")
    else: # yanlış cevap
        if df["word"][num] in learn_matrix["word"].values: # eğer kaydı VAR ise
            learn_matrix.loc[learn_matrix["word"]==df["word"][num],"w_response"]+=1 # yanlış cevap sayısını güncelle
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"] = power_law(
                row["c_response"],
                row["w_response"],
                row["datetime_last_c_response"]
            )
        else: # eğer kaydı YOK ise
            learn_matrix.loc[len(learn_matrix)]=[str(df["word"][num]),0,0,0.0,datetime.now().isoformat(),None,0] # kaydını oluştur
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w_response"] += 1 # yanlış cevap sayısını güncelle
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"] = power_law(
                row["c_response"],
                row["w_response"],
                row["datetime_last_c_response"]
            )
        print("Wrong. Correct answer is: ",df["word"][num])
    learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w/c_ratio"] =round(learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w_response"]/(1+learn_matrix.loc[learn_matrix["word"] == df["word"][num], "c_response"]),4)
    num_old.append(num)
    num=int(df.loc[df['word']==randomness(learn_matrix)].index[0])
    row = learn_matrix.loc[learn_matrix["word"] == df["word"][num]].iloc[0]
print(learn_matrix)
print(num_old)
learn_matrix.to_csv("learn_matrix.txt",sep=";",index=False)

