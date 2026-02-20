import os
import pandas as pd
from learning_method import power_law

learn_matrix=pd.read_csv("learn_matrix.txt", sep=";")

print(learn_matrix["p_law"])

for word in learn_matrix["word"]:
    c_response=learn_matrix.loc[learn_matrix["word"]==word,'c_response'].iloc[0]
    w_response=learn_matrix.loc[learn_matrix["word"]==word,'w_response'].iloc[0]
    datetime_last_c_response=learn_matrix.loc[learn_matrix["word"]==word,'datetime_last_c_response'].iloc[0]
    learn_matrix.loc[learn_matrix["word"] == word, 'p_law']=power_law(c_response,w_response,datetime_last_c_response)

print(learn_matrix["p_law"])

learn_matrix.to_csv("learn_matrix.txt",sep=";",index=False)
print("learning values updated")