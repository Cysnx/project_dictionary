import os
import pandas as pd


if os.path.exists("learn_matrix.txt"):
    learn_matrix=pd.read_csv("learn_matrix.txt", sep=';')

print(learn_matrix.sort_values(by=['p_law'], ascending=True))

print(learn_matrix[learn_matrix['p_law'] <= 0.6].sort_values(by=['p_law'], ascending=True))