#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 11:16:58 2018

@author: Louis
"""

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
import pandas as pd

ans_df = pd.read_csv("AR_answer.csv")

def check_answer(alien, planet):
    check = 0
    s = ans_df[alien] 
    try:
       i = ans_df.index[ans_df['Planet']==planet].tolist()
       if s[i[0]] == 'Acceptable':
           check = 1
    except (RuntimeError, TypeError, NameError):  
       check = 0 
    return check


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
        AnsDict = dict()
        AnsChkLDict = dict()
        WriteString = ''
        trialCnt = 0
        idCnt += 1
        TryYN = '0'
        try:
            USERID = RAW_DATA[user]
            GRPCODE = USERID['basicInfo']['groupCode']
            if GRPCODE == 'LB201701':
                continue
            
            #if GRPCODE == 'LB201701' test group
            BUDGET =  USERID['probeBudget']
            #groupcode, userid, probeBudget, # of probe Attempt, Attemp N ProbeType, Attemp N TargetPlanet,.., Attemp N-11 ProbeType, Attemp N-11 TargetPlanet, 
            #.... , AkonaHabitat, Akona 1/0, EolaniHabitat, Eolani 1/0, ..., Sum 1/0  
            #WriteString = user
            WriteString = GRPCODE + ',' + user + ',' + str(BUDGET)
            totalScore = 0

            try:
                COMM = USERID['communication']
                TryYN = '1'
                for attempts in COMM:
                    trialCnt += 1
                    try:
                        ATTEMPT = COMM[attempts]
                        selectedAlien = ATTEMPT['selectedAlien']
                        selectedHabitat = ATTEMPT['selectedHabitat'] 
                        AnsDict[selectedAlien] = selectedHabitat
                        a = check_answer(selectedAlien, selectedHabitat)
                        totalScore = totalScore + a
                        AnsChkLDict[selectedAlien] = a
                    except TypeError:
                        trialCnt -= 1
                        pass
            except KeyError:
                print('     communication KeyError ', WriteString)
                TryYN = '0'
                pass

            for alien in ans_df.iloc[[0]]:
                if alien == 'Planet':
                    continue
                if alien in AnsDict.keys():
                    WriteString = WriteString + ',' + AnsDict[alien] + ',' + str(AnsChkLDict[alien])      
                else:
                    WriteString = WriteString + ',     ,0'
                    
                
            WriteString = WriteString  + ',' + str(totalScore) + ',' + TryYN
            fp.writelines(WriteString + '\n')
            
            
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


