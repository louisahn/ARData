#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 14:28:46 2017

@author: Louis
"""

import sys
import json
import os.path


RAW_DATA_FILE = sys.argv[1]
with open(RAW_DATA_FILE, encoding='utf-8') as data_file:
    RAW_DATA = json.load(data_file)
    USERS = RAW_DATA['users']

with open(sys.argv[2], 'w') as fp:
    for user in USERS:
        WriteString = ''
        TotalTrial = 0
        SuccessTrial = 0
        try:
            USERID = USERS[user]
            GRPCODE = USERID['basicInfo']['groupCode']

            PROBES = USERID['probes']
            for attempts in PROBES:
                attempt = PROBES[attempts]
                #TotalTrial += 1
                #print(attempts)
                result = attempt['results']
                TIME = attempt['timeStamp']
                try:
                    isSuccess = attempt['results']['isSuccessful']
                    if isSuccess:
                        SuccessTrial = 1
                    else:
                        SuccessTrial = 0
                except TypeError:
                    pass
                #print(attempt['results']['isSuccessful'])
                #if attempt['results']['isSuccessful']:
                #    print(1)
                WriteString = GRPCODE + '\t' + user + '\t' + str(SuccessTrial) + '\t' +  TIME
                
                fp.writelines(WriteString + '\n')
                
            #print(Probes['email'])
        except KeyError:
            print('     KeyError ', WriteString)
            pass
        except NameError:
            print('     NameError ', WriteString)
            pass

    #json.dump(attempt, fp, sort_keys=True, indent=4)
    fp.close()
