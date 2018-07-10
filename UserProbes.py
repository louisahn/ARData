#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 14:02:00 2018

@author: Louis



"""


import sys
import json
import os.path
import csv
import pandas as pd
import datetime
import dateutil.parser

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


probeInstruments = ['Spectrograph','Radar','Seismograph', 'Magnetometer', 'Thermometer', 'Barometer', 'Infrared Camera', 'Wide Angle Camera','Narrow Angle Camera']

selectedProbeCommunication = ['Low Gain Antenna','High Gain Antenna']
selectedProbeSource = ['Battery', 'Solar Panels', 'Thermoelectric']
selectedProbeType = ['Flyby', 'Orbiter', 'Orbiter with Lander']

selectedProbeType.extend(selectedProbeSource)
selectedProbeType.extend(selectedProbeCommunication)

def CODETYPE(jsonobj):
    returnStr = '00000000'

    try:
        jsonarray = jsonobj['selectedProbeCommunication']
        for idx in jsonarray:
            i = selectedProbeType.index(idx['name'])
            returnStr= returnStr[:i]+'1'+returnStr[i+1:]

        jsonarray = jsonobj['selectedProbeSource']
        for idx in jsonarray:
            i = selectedProbeType.index(idx['name'])
            returnStr= returnStr[:i]+'1'+returnStr[i+1:]

        i = selectedProbeType.index(jsonobj['selectedProbeType']['name'])
        returnStr= returnStr[:i]+'1'+returnStr[i+1:]
    except KeyError as err:
        #print("CODETYPE error: {0}".format(err))
        pass

    return returnStr

def CODEINST(jsonarray):
    returnStr = '000000000'
    try:
        for idx in jsonarray:
            i = probeInstruments.index(idx['name'])
            returnStr= returnStr[:i]+'1'+returnStr[i+1:]
            #b_s[probeInstruments.index(idx['name'])] = '1'
    except KeyError as err:
        #print("CODEINST error: {0}".format(err))
        pass
    return returnStr


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
        idCnt += 1
        TryYN = '0'
        try:
            USERID = RAW_DATA[user]
            GRPCODE = USERID['basicInfo']['groupCode']
            if GRPCODE == 'LB201701':
                idCnt -= 1
                continue           
            #if GRPCODE == 'LB201701' test group
            #WriteString = GRPCODE + ',' + user 
            trialCnt = 0

            try:
                PROBES = USERID['probes']
                TryYN = '1'
                for attempts in PROBES:
                    WriteString = str(idCnt) + ',' + GRPCODE + ',' + user 
                    trialCnt += 1
                    ptype = '00000000'
                    pinst = '000000000'
                    try:
                        ATTEMPT = PROBES[attempts]
                    except KeyError as err:
                        trialCnt -= 1
                        print('attempts in PROBES KeyError ', WriteString)
                        continue
                    
                    try:
                        DESTI = ATTEMPT['destination']['selectedPlanet']
                    except KeyError as err:
                        trialCnt -= 1
                        print('DESTI KeyError ', WriteString)
                        continue                   
                    try:
                        PROBETYPE = ATTEMPT['probeSpecifications']
                        ptype = CODETYPE(PROBETYPE)
                    except KeyError as err:
                        #print('PROBETYPE KeyError ', WriteString)
                        pass                            
                    try:
                        PROBEINST = ATTEMPT['probeInstruments']
                        pinst = CODEINST(PROBEINST)
                    except KeyError as err:
                        #print('PROBEINST KeyError ', WriteString)
                        pass   
                    timeStamp  = ATTEMPT['timeStamp']
                    t = dateutil.parser.parse(timeStamp)
                    #print("{:%Y%m%d}".format(t) )
                    
                    WriteString = WriteString + ',' + "{:%Y%m%d}".format(t) + ',' + str(trialCnt) + ',' + ptype + ',' + pinst + ','  
                    for itemDESTI in DESTI:
                        fp.writelines(WriteString + itemDESTI + '\n')
                        
                    #WriteString = WriteString + ',' + "{:%Y%m%d}".format(t) + ',' + str(trialCnt) + ',' + ptype + ',' + pinst + ',' + ' '.join(DESTI)
                    #fp.writelines(WriteString + '\n')
                    

            except KeyError:
                print('No Probes: ', user)
                idCnt -= 1
                #WriteString = WriteString + ',' + '0' + ',' + '00000000' + ',' + '000000000' + ',' + ' '
                #fp.writelines(WriteString + '\n')      
                TryYN = '0'
                pass

            
            
            #print(Probes['email'])
        except KeyError:
            print('USERID     KeyError ', WriteString)
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


