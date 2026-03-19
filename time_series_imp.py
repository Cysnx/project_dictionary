'''
1.  When prompted, record the date&time.
1.1 Does it have a folder/file? Yes: Read the file. No: Create the folder/file.
2.  Acquire the P_Score.
3.  Plot and save, based on:
3.1 If only '1' datapoint. No Action.
3.2 If '2' datapoints, linear fit.
3.3 If '3' or more, polynomial fit. Order: 3
3.4 Apply R^2 to plot.
'''

import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

def time_series_imp(word,p_score):
    filename=''
    for w in word:
        if w=='-'or w=='/':
            w=''
            filename=filename+w
        else:
            filename=filename+w
    '''Does it have a folder/file?'''
    if os.path.exists(f"time_series/{filename}/{filename}_pts.txt"):# pts: p score time series
        pts = pd.read_csv(f"time_series/{filename}/{filename}_pts.txt", sep=';')
    else:
        os.mkdir(f"time_series/{filename}")
        pts = pd.DataFrame({'time': pd.Series(dtype='str'),
                            'p_scr': pd.Series(dtype='float')})


    ''' Record the datetime'''
    timenow=datetime.now().isoformat()

    '''map the datetime and p_score, write them into the file.'''
    new_row = pd.DataFrame([{'time': timenow, 'p_scr': p_score}])
    pts = pd.concat([pts, new_row], ignore_index=True)

    pts.to_csv(f"time_series/{filename}/{filename}_pts.txt",sep=';',index=False)

    '''Plot and save'''

    plt.plot(pts['time'], pts['p_scr'],'o')
    plt.ylim(-0.05,1.05)
    plt.ylabel('p_score')
    plt.xlabel('datetime')
    plt.xticks(rotation=45)
    plt.title(filename)
    plt.savefig(f"time_series/{filename}/{filename}_pts.png")
    plt.close() # This one is important!!






