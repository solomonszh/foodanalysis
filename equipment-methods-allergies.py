#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 11:38:16 2019

@author: janiceteo
"""

import requests
import json
import pandas as pd
from pprint import pprint
from openpyxl import load_workbook
import numpy as np

path = '/Users/janiceteo/Documents/YoRipe/Recipes/Simpliigood/SimpliiGood Recipes 24012020.xlsx'
worksheet = 'Sheet1'
df = pd.read_excel(path, worksheet)
equip = pd.read_excel('/Users/janiceteo/Documents/YoRipe/Recipes Masterfile_Dec 2019.xlsx', 'Kitchen Equipment')
method = pd.read_excel('/Users/janiceteo/Documents/YoRipe/Recipes Masterfile_Dec 2019.xlsx', 'Method')
allergies = pd.read_excel('/Users/janiceteo/Documents/YoRipe/Allergy-ingredients list.xlsx', 'Allergy-Ingredients')
foodList = list(allergies['Ingredient'])
foodList = [j.split(", ") if ", " in j else j.split(", ") if "," in j else j for j in foodList]
exceptions = pd.read_excel('/Users/janiceteo/Documents/YoRipe/Allergy-ingredients list.xlsx', 'Exceptions')
exceptionList = list(exceptions['Exception'])
exceptionList = [j.split(", ") if ", " in j else j.split(", ") if "," in j else j for j in exceptionList]

#equipment
equiplist = [] 
for d in range(len(df)):
    equipmentList = []
    for e in range(len(equip)):
        if type(df.instructions[d]) != float:
            if equip['Kitchen Equipment'][e].lower() in df['instructions'][d].lower():
                if int(equip['ID'][e]) not in equipmentList:
                    equipmentList.append(int(equip['ID'][e]))
    equipmentList = sorted(equipmentList)
    equipmentList = [str(x) for x in equipmentList]
    equiplist.append(','.join(equipmentList))
df['Kitchen Equipment'] = equiplist

#cooking method
methodlist = [] 
for d in range(len(df)):
    meanslist = []
    if not(np.isnan(df['Method'][d])):
        meanslist.append(int(df['Method'][d]))
    for m in range(len(method)):
        if type(df.instructions[d]) != float:
            if method['Method'][m].lower() in df['instructions'][d].lower():
                if int(method['ID'][m]) not in meanslist:
                    meanslist.append(int(method['ID'][m]))
    meanslist = sorted(meanslist)
    meanslist = [str(x) for x in meanslist]
    methodlist.append(','.join(meanslist))
df['Method'] = methodlist

#allergies
allergyList = []       
for i in range(len(df)):
    allergiesList = []
    for j in range(len(foodList)):
        if type(foodList[j]) is list:
            for k in foodList[j]:
                if k in df['ingredients'][i]:
                    if int(allergies['Allergy_ID'][j]) not in allergiesList:
                        allergiesList.append(int(allergies['Allergy_ID'][j]))
        else:
            if foodList[j] in df['ingredients'][i]:
                if int(allergies['Allergy_ID'][j]) not in allergiesList:
                    allergiesList.append(int(allergies['Allergy_ID'][j]))
    for j in range(len(exceptionList)):
        if type(exceptionList[j]) is list:
            for e in exceptionList[j]:
                if e in df['ingredients'][i]:
                    if int(exceptions['Allergy_ID'][j]) in allergiesList:
                        allergiesList.remove(int(exceptions['Allergy_ID'][j]))
        else:
            if exceptionList[j] in df['ingredients'][i]:
                if int(exceptions['Allergy_ID'][j]) in allergiesList:
                    allergiesList.remove(int(exceptions['Allergy_ID'][j]))
    allergiesList = sorted(allergiesList)
    allergiesList = [str(x) for x in allergiesList]
    allergyList.append(','.join(allergiesList))
df['allergy'] = allergyList

newpath = path[:path.find('.xlsx')] + ' edited.xlsx'
writer = pd.ExcelWriter(newpath, engine='xlsxwriter', options={'strings_to_urls': False})
df.to_excel(writer,'Sheet1', index = False)
writer.save()



