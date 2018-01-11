# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:17:44 2018

@author: Arthur
"""

import pandas as pd
import datetime as dt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

# DATA PATH
path = "C:\\Users\\Arthur\\Documents\\Studies\\ParisDauphineUniversity\\Master203\\M2\\ATS\\project\\data\\"


# AVAILABLES TICKERS
TICKER_LIST = ["HO1_COMDTY","CL1_COMDTY","OEX_INDEX","SXEE_INDEX","SXEP_INDEX","BP_EQUITY","CAC_INDEX","CHEVRON_EQUITY","CNYUSD_CRRCY","CO1_COMDTY","CONOCOPHIL_INDEX","DJ_INDEX","EURGBP_CRRCY","EURUSD_CRRCY","EXON_EQUITY","LMECOPPER_COMDTY","MSCI_INDEX","NK_INDEX","NG1_COMDTY","SHELL_EQUITY","SPX_INDEX","TOTAL_EQUITY","USDGBP_CRRCY","XB1_COMDTY"]


###############################################################################
########################## DATA LOADING AND SAMPLING ##########################
###############################################################################

#Load data and clean it
def load_data_from_csv(ticker):
    if ticker in TICKER_LIST:
        df = pd.read_csv(path+ticker+".csv", delimiter=";",encoding='latin1', index_col=0, header=None)
        df.columns = ['Value']
        df = df.dropna()
    else:
        df=pd.DataFrame()
    return df

# returns the dataframe data with the common dates
def get_same_dates(df1,df2):
    idx = df1.index.intersection(df2.index)
    df1 = df1.loc[idx]
    df2 = df2.loc[idx]
    return df1, df2

def get_returns(df):  
    return df.pct_change().dropna()

def sampling_one(df, sampling_dates):
    df_in, df_out, i,d= sampling_two(df, df,sampling_dates)
    return df_in, df_out

# Given some start and end dates, return the in and out samples    
def sampling_two(df1, df2,sampling_dates):
    start_in = sampling_dates[0]
    end_in = sampling_dates[1]
    
    # check that start in is in both dataframes
    while (start_in not in df1.index) and (start_in not in df2.index):
        start_in = str(get_nearest(df1, start_in, 'h'))
        
    # check that end in is in both dataframes and after start in
    while (end_in not in df1.index) and (end_in not in df2.index):
        if is_later(end_in, start_in):
            end_in = get_nearest(df1, end_in, 'l')
        else:
            print("END IN is before START IN")
            end_in = get_nearest(df1, end_in, 'h')
    df1_in = df1.loc[start_in:end_in]
    df2_in = df2.loc[start_in:end_in]
    
    start_out = sampling_dates[2]
    end_out = sampling_dates[3]
    
    # check that out of sample starts after the end of in sample
    while is_later(end_in,start_out):
        start_out = get_nearest(df1, start_out, 'h')
        
    # check that start out of sample is in both dataframes
    while (start_out not in df1.index) and (start_out not in df2.index):
        start_out = get_nearest(df1, start_out, 'h')
        
    # check that end_out is in both dataframes and that it is later than the start
    while (end_out not in df1.index) and (end_out not in df2.index):
        if is_later(end_out, start_out):
            end_out = get_nearest(df1, end_out, 'l')
        else:
            print("END OUT is before START OUT")
            end_out = get_nearest(df1, end_out, 'h')
    df1_out = df1.loc[start_out:end_out]
    df2_out = df2.loc[start_out:end_out]
    return df1_in, df1_out, df2_in, df2_out

###############################################################################
############################## DATES MANIPULATION #############################
###############################################################################

# compare two string dates
def is_later(d1,d2):
    return dt.datetime.strptime(d1, '%d/%m/%Y').date() > dt.datetime.strptime(d2, '%d/%m/%Y').date()

def nearest_l(items, pivot):
    return min(items, key=lambda x: abs( pivot-x))

def nearest_h(items, pivot):
    	return min(item for item in items if item > pivot)
    
# get the nearest date, lower (l) or higher (h) that is in the dataframe index
def get_nearest(df,d,lh):
    d = dt.datetime.strptime(d, '%d/%m/%Y').date()
    dates_list = [dt.datetime.strptime(date, '%d/%m/%Y').date() for date in df.index]
    if lh == 'l':
        d = nearest_l(dates_list, d)
    else:
        d = nearest_h(dates_list, d)
    return d.strftime('%d/%m/%Y')

def get_next_day(d,df):
    d = dt.datetime.strptime(d, '%d/%m/%Y').date()
    d+=dt.timedelta(days=1)
    while d.strftime('%d/%m/%Y') not in df.index:
        d+=dt.timedelta(days=1)
    return d.strftime('%d/%m/%Y')








