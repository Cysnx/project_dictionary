import pandas as pd
import random

df=pd.read_csv("items.txt",sep=';')

#print(df["meaning"][14])
#print(len(df["word"]))

num=random.randint(0,len(df["word"])-1)

c_response=0
w_response=0
num_old=[]
response=""

while response!="exit":
    print(f"What is the word for the following: {df['meaning'][num]}")
    response=input("")
    if response==df["word"][num]:
        c_response+=1
        print("Correct!")
    else:
        w_response+=1
        print("Wrong")
    num_old.append(num)
    num=random.randint(0,len(df["word"])-1)