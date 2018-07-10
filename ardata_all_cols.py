import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from keras.layers import *
from keras.models import *
from keras.utils.np_utils import to_categorical

path = '/Volumes/Storage/0.SAGAbackup/ARData/'

import sys
import json
import os.path

RAW_DATA_FILE = path + 'ar_data.json'
OUT_DATA_FILE = path + 'ardata_all_cols.txt'
NP = np.empty((0,3), object)
with open(RAW_DATA_FILE, encoding='utf-8') as data_file:
    RAW_DATA = json.load(data_file)
    USERS = RAW_DATA['logs']

    for user in USERS:
        WriteString = ''
        TotalTrial = 0
        SuccessTrial = 0
        try:
            USERID = USERS[user]
            PROBES = USERID['dataLog']
            tmparr = np.array([PROBES['action'],PROBES['note'],PROBES['tool']])
            NP = np.vstack((NP, tmparr))

        except KeyError:
            print('     KeyError ', WriteString)
            pass
        except NameError:
            print('     NameError ', WriteString)
            pass
        except UnicodeEncodeError:
            print('     UnicodeEncodeError ')
            pass
        except TypeError:
            print('     TypeError ', WriteString)
            pass

np.savetxt(OUT_DATA_FILE, NP)        
#with open(OUT_DATA_FILE, 'w') as fp:
    #json.dump(attempt, fp, sort_keys=True, indent=4)
    #fp.close()
