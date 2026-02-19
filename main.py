import pandas as pd
import random
import os
import time
from datetime import datetime

df=pd.read_csv("items.txt",sep=';')

#print(df["meaning"][14])
#print(len(df["word"]))
SIZE_DICT=len(df["word"])

num=random.randint(0,len(df["word"])-1)

c_response=0
w_response=0
num_old=[]
response=""

def power_law(c_response,w_response,datetime_last_c_response): ## bunu çalışmam gerek
    k = w_response / (1 + c_response)
    today = datetime.now()

    if (
        datetime_last_c_response is None
        or datetime_last_c_response == ''
        or pd.isna(datetime_last_c_response)
        or datetime_last_c_response == 'N/A'
    ):
        return 0.0

    if isinstance(datetime_last_c_response, str):
        last_c = datetime.fromisoformat(datetime_last_c_response)
    else:
        last_c = pd.to_datetime(datetime_last_c_response).to_pydatetime()

    delta = (today - last_c).total_seconds()/86400

    return round((1 + delta) ** (-k),4)



if os.path.exists("learn_matrix.txt"):
    learn_matrix=pd.read_csv("learn_matrix.txt", sep=';')
else:
    learn_matrix=pd.DataFrame(columns=["word","c_response","w_response","w/c_ratio","datetime_seen_first","datetime_last_c_response","p_law"])

while True:
    print(f"What is the word ({df['type'][num]}) for the following: {df['meaning'][num]}")
    response=input("")
    if response=="exit":
        break
    elif response==df["word"][num]: # doğru cevap
        if df["word"][num] in learn_matrix["word"].values: # eğer kaydı VAR ise
            learn_matrix.loc[learn_matrix["word"]==df["word"][num],"c_response"]+=1 # doğru cevap sayısını güncelle
            row = learn_matrix.loc[learn_matrix["word"] == df["word"][num]].iloc[0]  ### burayı da çalışmam gerek

            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"] = power_law(
                row["c_response"],
                row["w_response"],
                row["datetime_last_c_response"]
            )
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "datetime_last_c_response"] =datetime.now().isoformat() # son doğru cevap tarihini güncelle
        else: # eğer kaydı YOK ise
            learn_matrix.loc[len(learn_matrix)]=[df["word"][num],0,0,0.0,datetime.now().isoformat(),datetime.now().isoformat(),0] # kaydını oluştur
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "c_response"] += 1 # doğru cevap sayısını güncelle
            row = learn_matrix.loc[learn_matrix["word"] == df["word"][num]].iloc[0]  ### burayı da çalışmam gerek

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
            row = learn_matrix.loc[learn_matrix["word"] == df["word"][num]].iloc[0]  ### burayı da çalışmam gerek

            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"] = power_law(
                row["c_response"],
                row["w_response"],
                row["datetime_last_c_response"]
            )
        else: # eğer kaydı YOK ise
            learn_matrix.loc[len(learn_matrix)]=[str(df["word"][num]),0,0,0.0,datetime.now().isoformat(),None,0] # kaydını oluştur
            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w_response"] += 1 # yanlış cevap sayısını güncelle
            row = learn_matrix.loc[learn_matrix["word"] == df["word"][num]].iloc[0]  ### burayı da çalışmam gerek

            learn_matrix.loc[learn_matrix["word"] == df["word"][num], "p_law"] = power_law(
                row["c_response"],
                row["w_response"],
                row["datetime_last_c_response"]
            )
        print("Wrong. Correct answer is: ",df["word"][num])
    learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w/c_ratio"] =round(learn_matrix.loc[learn_matrix["word"] == df["word"][num], "w_response"]/(1+learn_matrix.loc[learn_matrix["word"] == df["word"][num], "c_response"]),4)
    num_old.append(num)
    num=random.randint(0,len(df["word"])-1)
print(learn_matrix)
print(num_old)
learn_matrix.to_csv("learn_matrix.txt",sep=";",index=False)

