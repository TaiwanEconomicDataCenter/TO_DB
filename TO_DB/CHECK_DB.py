# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=E1101
import math, re, sys, calendar, os, copy, time, csv, pymysql, warnings, random, xlsxwriter
import pandas as pd
import numpy as np
import sqlalchemy
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR
from sqlalchemy.dialects.mysql import DOUBLE
from datetime import datetime, date
from TO_DB import *
warnings.simplefilter("ignore")

ENCODING = 'utf-8-sig'
out_path = './output/'

tStart = time.time()
NAME = input("\nCheck Bank: ")

print('\n\nSELECT * FROM '+NAME.lower()+'_old'+'.'+NAME.lower()+'_key'+'\n')
df_key_old = SELECT_DF_KEY(NAME+'_old')
DATA_BASE_t_old = SELECT_DATABASES(NAME+'_old')
print('\n\nSELECT * FROM '+NAME.lower()+'.'+NAME.lower()+'_key'+'\n')
df_key = SELECT_DF_KEY(NAME)
DATA_BASE_t = SELECT_DATABASES(NAME)

print('Run Time: '+str(int(time.time() - tStart))+' s'+'\n')
blank = pd.DataFrame([''])
result = pd.DataFrame([['Bank Name', NAME]])
print("Old Bank's Size = "+str(df_key_old.shape[0]))
print("New Bank's Size = "+str(df_key.shape[0]))
size = pd.DataFrame([["Old Bank's Size", df_key_old.shape[0]], ["New Bank's Size", df_key.shape[0]]])
result = pd.concat([result, size])
result = pd.concat([result, blank])

print('\nRun Time: '+str(int(time.time() - tStart))+' s'+'\n')
sample_num = 30
freqlist = list(df_key_old["freq"].drop_duplicates())
freqdata = {}
freqsample = {}
for f in freqlist:
    freqdata[f] = list(df_key_old.loc[df_key_old["freq"] == f]["name"])
    random.shuffle(freqdata[f])
    freqsample[f] = freqdata[f][:sample_num]
print('Samplings: '+str(sample_num*len(freqlist))+' items in total')
result = pd.concat([result, pd.DataFrame([['Samplings:', str(sample_num*len(freqlist))+' items in total']])])
result = pd.concat([result, pd.DataFrame([['FREQ', 'NAME']])])
for f in freqlist:
    for name in freqsample[f]:
        print(f, name)
        result = pd.concat([result, pd.DataFrame([[f, name]])])
result = pd.concat([result, blank])
print('\nComparison:')
modified = 0
modified_data = {}
for f in freqlist:
    modified_data[f] = pd.DataFrame()
result = pd.concat([result, pd.DataFrame([['Comparison:', '']])])
result = pd.concat([result, pd.DataFrame([['BANK', 'NAME', 'FREQ', 'START', 'LAST', 'DESCRIPTION']])])
result = pd.concat([result, blank])
for f in freqlist:
    for name in freqsample[f]:
        sys.stdout.write("\rName = "+name+"     ")
        sys.stdout.flush()

        old_item = df_key_old.loc[df_key_old['name'] == name].squeeze()
        new_item = df_key.loc[df_key['name'] == name].squeeze()
        if old_item.empty:
            ERROR('Name Not Found in database '+NAME.lower()+': '+name)
        if new_item.empty:
            ERROR('Name Not Found in database '+NAME.lower()+'_old: '+name)
        result = pd.concat([result, pd.DataFrame([['Old', name, f, old_item['start'], old_item['last'], old_item['desc_e']]])])
        result = pd.concat([result, pd.DataFrame([['New', name, f, new_item['start'], new_item['last'], new_item['desc_e']]])])
        old_data = DATA_BASE_t_old[old_item['db_table']][old_item['db_code']]
        new_data = DATA_BASE_t[new_item['db_table']][new_item['db_code']]
        if not old_data.dropna().equals(new_data.dropna()):
            result = pd.concat([result, pd.DataFrame([['modified:', True]])])
            modified += 1
            modified_old_item = pd.DataFrame([name, 'Old'], index=['NAME', 'BANK'])
            if f != 'D':
                modified_old_item = pd.concat([modified_old_item, old_data.iloc[::-1]]).T
            else:
                modified_old_item = pd.concat([modified_old_item, old_data]).T
            modified_new_item = pd.DataFrame([name, 'New'], index=['NAME', 'BANK'])
            if f != 'D':
                modified_new_item = pd.concat([modified_new_item, new_data.iloc[::-1]]).T
            else:
                modified_new_item = pd.concat([modified_new_item, new_data]).T
            modified_data[f] = pd.concat([modified_data[f], pd.concat([modified_new_item, modified_old_item]).iloc[::-1]])
        else:
            result = pd.concat([result, pd.DataFrame([['modified:', False]])])
        result = pd.concat([result, blank])
    modified_data[f] = modified_data[f].dropna(axis=1, how="all")
sys.stdout.write("\n\n")

print('\nRun Time: '+str(int(time.time() - tStart))+' s'+'\n')
print("Total Modified items = "+str(modified))
result = pd.concat([result, pd.DataFrame([['Total Modified items:', modified]])])

print('\nOutputing Results, Time: '+str(int(time.time() - tStart))+' s'+'\n')
with pd.ExcelWriter(out_path+"Check Results - "+NAME+" - "+datetime.now().strftime("%Y-%m-%d %H.%M.%S")+".xlsx", engine='xlsxwriter') as writer:
    result.to_excel(writer, sheet_name='results', header=False, index=False)
    worksheet = writer.sheets['results']
    worksheet.set_column("A:B", 20)
    worksheet.set_column("C:E", 10)
    worksheet.set_column("F:F", 20)
    for f in modified_data:
        sys.stdout.write("\rOutputing sheet: "+str(f))
        sys.stdout.flush()
        if modified_data[f].empty == False:
            modified_data[f].to_excel(writer, sheet_name=f, index=False)
            worksheet = writer.sheets[f]
            worksheet.set_column("A:A", 20)
    sys.stdout.write("\n")

print('\nRun Time: '+str(int(time.time() - tStart))+' s'+'\n')