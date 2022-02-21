#sql="SELECT * FROM intline_key"
#pd.read_sql_query(sql, engine)
import math, re, sys, calendar, os, copy, time, csv, pymysql
import pandas as pd
import numpy as np
import sqlalchemy
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR
from sqlalchemy.dialects.mysql import DOUBLE

ENCODING = 'utf-8-sig'

def ERROR(special_text):
    sys.stdout.write('\n\n')
    print('= ! = '+error_text)
    sys.stdout.write('\n\n')
    sys.exit()
def readExcelFile(dir, default=pd.DataFrame(), acceptNoFile=False, \
             header_=None,skiprows_=None,index_col_=None,sheet_name_=None):
    try:
        t = pd.read_excel(dir,sheet_name=sheet_name_, header=header_,index_col=index_col_,skiprows=skiprows_)
        #print(t)
        return t
    except FileNotFoundError:
        if acceptNoFile:
            return default
        else:
            ERROR('找不到檔案：'+dir)
    except Exception as error:
        raise error

# using_database = True
def GET_PWD():
    pwd = open('../TO_DB/password.txt','r',encoding='ANSI').read()
    return pwd

def INSERT_TABLES_FROM_EXCEL():
    pwd = open('./password.txt','r',encoding='ANSI').read()
    tStart = time.time()
    data_path = './output/'
    out_path = './output/'
    BANKS = ['QNIA','MEI','GERFIN','EIKON','FOREX','US','INTLINE','ASIA']
    NAME = input("Bank: ")
    if NAME not in BANKS:
        SPECIAL('Unknown Bank: '+NAME)
    if NAME == 'EIKON':
        data_path = Path(os.path.realpath(data_path)).as_posix().replace('TO_DB','GERFIN')+'/'
    elif NAME == 'ASIA':
        data_path = Path(os.path.realpath(data_path)).as_posix().replace('TO_DB','INTLINE')+'/'
    else:
        data_path = Path(os.path.realpath(data_path)).as_posix().replace('TO_DB',NAME)+'/'
    data_suffix = input("Database suffix: ")
    print('Reading file: '+NAME+'_key'+data_suffix+', Time: ', int(time.time() - tStart),'s'+'\n')
    df_key = readExcelFile(data_path+NAME+'_key'+data_suffix+'.xlsx', header_ = 0, acceptNoFile=False, index_col_=0, sheet_name_=NAME+'_key')
    try:
        with open(data_path+NAME+'_database_num'+data_suffix+'.txt','r',encoding=ENCODING) as f:  #用with一次性完成open、close檔案
            database_num = int(f.read().replace('\n', ''))
        DATA_BASE_t = {}
        for i in range(1,database_num+1):
            print('Reading file: '+NAME+'_database_'+str(i)+data_suffix+', Time: ', int(time.time() - tStart),'s'+'\n')
            DB_t = readExcelFile(data_path+NAME+'_database_'+str(i)+data_suffix+'.xlsx', header_ = 0, index_col_=0, acceptNoFile=False, sheet_name_=None)
            for d in DB_t.keys():
                DATA_BASE_t[d] = DB_t[d]
    except:
        print('Reading file: '+NAME+'_database'+data_suffix+', Time: ', int(time.time() - tStart),'s'+'\n')
        DATA_BASE_t = readExcelFile(data_path+NAME+'_database'+data_suffix+'.xlsx', header_ = 0, index_col_=0, acceptNoFile=False)
    print(df_key)

    INSERT_TABLES(NAME, df_key, DATA_BASE_t, pwd=pwd)

def INSERT_TABLES(NAME, df_key, DATA_BASE_t, pwd=None):
    tStart = time.time()
    if pwd == None:
        pwd = GET_PWD()
    
    engine = create_engine('mysql+pymysql://root:'+pwd+'@localhost:3306/'+NAME.lower())
    print('Time: '+str(int(time.time() - tStart))+' s'+'\n')
    print('CREATE TABLE '+NAME+'_key'+'\n')
    df_key.to_sql(NAME.lower()+'_key', con=engine, if_exists='replace', index=False, dtype={'name':VARCHAR(20)})
    with engine.connect() as con:
        con.execute('ALTER TABLE `'+NAME.lower()+'_key'+'` ADD PRIMARY KEY (`name`);')
    print('Time: '+str(int(time.time() - tStart))+' s'+'\n')
    for d in DATA_BASE_t:
        sys.stdout.write("\rCREATE TABLE "+str(d))
        sys.stdout.flush()
        if DATA_BASE_t[d].empty == False:
            datatypes = {}
            datatypes[DATA_BASE_t[d].index.name] = VARCHAR(15)
            for col in DATA_BASE_t[d].columns:
                datatypes[col] = DOUBLE
            DATA_BASE_t[d] = DATA_BASE_t[d].applymap(lambda x: None if str(x) == '' else x)
            DATA_BASE_t[d].to_sql(d.lower(), con=engine, if_exists='replace', index=True, dtype=datatypes)
    sys.stdout.write("\n")

    print('Time: '+str(int(time.time() - tStart))+' s'+'\n')
    shape_info = pd.read_sql_query("SELECT count(*) AS shape FROM "+NAME.lower()+'_key', engine)
    print(shape_info)


def SELECT_DF_KEY(NAME):
    pwd = GET_PWD()
    
    engine = create_engine('mysql+pymysql://root:'+pwd+'@localhost:3306/'+NAME.lower())
    DF_KEY = pd.read_sql_query("SELECT * FROM "+NAME.lower()+"_key", engine)
    DF_KEY = DF_KEY.applymap(lambda x: int(x) if str(x).isnumeric() else x)

    return DF_KEY

def SELECT_DATABASES(NAME):
    tStart = time.time()
    pwd = GET_PWD()
    
    engine = create_engine('mysql+pymysql://root:'+pwd+'@localhost:3306/'+NAME.lower())
    print("SELECT db_table FROM "+NAME.lower()+"_key GROUP BY db_table, Time: "+str(int(time.time() - tStart))+" s"+"\n")
    table_keys = pd.read_sql_query("SELECT db_table FROM "+NAME.lower()+"_key GROUP BY db_table", engine).squeeze().tolist()
    print('Time: '+str(int(time.time() - tStart))+' s'+'\n')

    DATA_BASE_dict = {}
    for db_table in table_keys:
        sys.stdout.write("\rSELECT * FROM "+str(db_table))
        sys.stdout.flush()
        DB = pd.read_sql_query("SELECT * FROM "+str(db_table).lower(), con=engine, index_col='index')
        if str(db_table).upper().find('A') > 0:
            DB.index = DB.index.astype(int)
        if DB.empty == False:
            DATA_BASE_dict[db_table] = DB
    sys.stdout.write("\n")
    print('Time: '+str(int(time.time() - tStart))+' s'+'\n')
    
    return DATA_BASE_dict

#INSERT_TABLES_FROM_EXCEL()
