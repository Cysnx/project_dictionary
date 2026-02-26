import random
import pandas as pd

""" I need to write a code, such that:
1. It should list the p_law values from the 'learn_matrix'.
2. It should pick the value from that list, biased towards the lowest number, in random fashion.
3. That value should be matched: p_law and corresponding word,
4. Finally, program should return that word as an input for 'items'."""

learn_matrix=pd.read_csv("learn_matrix.txt", sep=';')

def randomness(learn_matrix):
    num=learn_matrix['p_law']
    #print(type(num))
    randnum=float(random.choices(num, weights=1/(num+0.05), k=1)[0])
    #print(type(randnum))
    randword=learn_matrix.loc[learn_matrix['p_law']==randnum, 'word'].values[0]
    #print(type(randword))
    return randword
print(randomness(learn_matrix))

