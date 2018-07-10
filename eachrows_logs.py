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
    USERS = RAW_DATA['logs']

with open(sys.argv[2], 'w') as fp:
    for user in USERS:
        WriteString = ''
        TotalTrial = 0
        SuccessTrial = 0
        try:
            USERID = USERS[user]
            PROBES = USERID['dataLog']
            
            #WriteString = PROBES['action']  + '\t' +  PROBES['note']  + '\t' +  PROBES['timestamp']  + '\t' + PROBES['tool']  + '\t' + PROBES['userId']  
            WriteString = PROBES['action']  + '\t' +  PROBES['note']  + '\t' +  PROBES['tool']  + '\t' + PROBES['userId']  
            
            """            
            for attempts in PROBES:
                attempt = PROBES[attempts]
                TotalTrial += 1
                
                result = attempt['results']
                print(result('action'))
                
                try:
                    isSuccess = attempt['results']['isSuccessful']
                    if isSuccess:
                        SuccessTrial += 1
                except TypeError:
                    pass
                """
                #print(attempt['results']['isSuccessful'])
                #if attempt['results']['isSuccessful']:
                #    print(1)
                
            #print(Probes['email'])
            #WriteString = WriteString + ',' + str(TotalTrial) + ',' + str(SuccessTrial) 
            fp.writelines(WriteString + '\n')
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
        

    #json.dump(attempt, fp, sort_keys=True, indent=4)
    fp.close()
