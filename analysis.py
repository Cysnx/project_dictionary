import os
import pandas as pd


if os.path.exists("learn_matrix.txt"):
    learn_matrix=pd.read_csv("learn_matrix.txt", sep=';')

print("****the best****\n",learn_matrix[learn_matrix['p_law']>=0.9].sort_values(by=['p_law'],ascending=True))

print("****the worst****\n",learn_matrix[learn_matrix['p_law'] <= 0.6].sort_values(by=['p_law'], ascending=True))