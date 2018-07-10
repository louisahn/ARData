#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:29:11 2018

@author: Louis
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 14:28:46 2017

@author: Louis
"""

import sys
import json
import os.path
import csv

RAW_DATA_FILE = sys.argv[1]
with open(RAW_DATA_FILE, encoding='utf-8', errors='ignore') as data_file:
    try:
        RAW_DATA = json.load(data_file)
    except UnicodeEncodeError:
        print('     FILE UnicodeEncodeError ')
        pass
        


with open(sys.argv[2], 'w') as fp:
    idCnt = 0
    for user in RAW_DATA:
        WriteString = ''
        trialCnt = 0
        idCnt += 1
        try:
            USERID = RAW_DATA[user]
            #WriteString = user
            PROBES = USERID['probes']
            for attempts in PROBES:
                trialCnt += 1
                try:
                    ATTEMPT = PROBES[attempts]
                    dest = ATTEMPT['destination']['selectedPlanet'] 
                except TypeError:
                    trialCnt -= 1
                    pass
                #print(attempt['results']['isSuccessful'])
                #if attempt['results']['isSuccessful']:
                #    print(1)
                if len(dest) < 2:
                    WriteString = str(idCnt) + ' ' + str(trialCnt) + ' ' + str(len(dest)) + ' ' + ",".join(dest)
                    fp.writelines(WriteString + '\n')
                else:
                    trialCnt -= 1
                
            #print(Probes['email'])
        except KeyError:
            print('     KeyError ', WriteString)
            idCnt -= 1
            pass
        except NameError:
            print('     NameError ', WriteString)
            idCnt -= 1
            pass
        except UnicodeEncodeError:
            print('     UnicodeEncodeError ')
            idCnt -= 1
            pass

    #json.dump(attempt, fp, sort_keys=True, indent=4)
    fp.close()
