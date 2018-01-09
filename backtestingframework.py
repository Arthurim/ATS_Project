# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 00:24:13 2018

@author: Arthur
"""

import pandas as pd
import numpy as np
import datetime as dt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
#%%
START_IN = "28/11/2000"
END_IN = "11/12/2015"
START_OUT = "16/12/2015"
END_OUT = "21/12/2017"

path = "C:\\Users\\Arthur\\Documents\\Studies\\ParisDauphineUniversity\\Master203\\M2\\ATS\\project\\data\\"
ticker_oil = "CO1_COMDTY"
ticker_gas = "NG1_COMDTY"
#%%
#Load data and clean it
def load_data(ticker):
    df = pd.read_csv(path+ticker+".csv", delimiter=";",encoding='latin1', index_col=0, header=None)
    df.columns = ['Returns']
    df = df.dropna()
    df_returns = get_returns(df)
    return df_returns

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def func2(dates_list):
    b_d = dt.datetime.strptime('25/12/2016', '%d/%m/%Y').date()
    def func(x):
       d =  x[0] #dt.datetime.strptime(x[0], "%m/%d %I:%M %p")
       delta =  d - b_d if d > b_d else dt.timedelta.max
       return delta
    return min(dates_list, key = func)

def nearest_l(items, pivot):
    return min(items, key=lambda x: abs( pivot-x))

def get_nearest(df,d,lh):
    d = dt.datetime.strptime(d, '%d/%m/%Y').date()
    dates_list = [dt.datetime.strptime(date, '%d/%m/%Y').date() for date in df.index]
    if lh == 'l':
        d = nearest(dates_list, d)
    else:
        d = nearest(dates_list, d)
    return d
    
def sampling(df):
    if (START_IN in df.index):
        start = START_IN
    else:
        start = get_nearest(START_IN,'h')
    if (END_IN in df.index):
        end = END_IN
    else:
        start = get_nearest(START_IN,'l')
    in_sample = df.loc[start: end]
    if (START_OUT in df.index):
        start = START_OUT
    else:
        start = get_nearest(START_IN,'h')
    if (END_OUT in df.index):
        end = END_OUT
    else:
        start = get_nearest(START_IN,'l')
    out_sample = df.loc[start: end]
    return in_sample, out_sample
    
def standardization(df):
    df_std = (df - df.mean()) / (df.max() - df.min()) if len(df) > 1 else df
    return df_std

def get_returns(df):  
    return df.pct_change().dropna()

def is_stationary(ts):
    return adfuller(ts)[1]<0.05

def make_stationary(ts):
    while(not is_stationary(ts))
        ts = diff(ts)
    return ts
    
def is_more_stationary(ts1,ts2):
    return adfuller(ts1)[0]<adfuller(ts2)[0]

def get_same_dates(df1,df2):
    idx = df1.join(df2, rsuffix='_', how='inner').index
    df1 = df1.reindex(idx)
    df2 = df2.reindex(idx)
    return df1, df2

def plot_acf_pacf(ts):
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(2,1,1)
    fig = sm.graphics.tsa.plot_acf(ts, lags=20, ax=ax1)
    ax2 = fig.add_subplot(2,1,2)
    fig = sm.graphics.tsa.plot_pacf(ts, lags=20, ax=ax2)   
    
def plot_ts(ts1,ts2):
    plt.figure()
    plt
    
#%%
df_oil = load_data(ticker_oil)
df_gas = load_data(ticker_gas)
df_oil, df_gas = get_same_dates(df_oil, df_gas)

df_in_oil, df_out_oil = sampling(df_oil)
df_in_gas, df_out_gas = sampling(df_gas)

ts_in_oil = df_in_oil['Returns']
ts_in_gas = df_in_gas['Returns']

model_o_g = sm.OLS(ts_in_oil,sm.add_constant(ts_in_gas)).fit()
predictions_o_g = model_o_g.predict(sm.add_constant(ts_in_gas))

model_g_o = sm.OLS(ts_in_gas,sm.add_constant(ts_in_oil)).fit()
predictions_g_o = model_g_o.predict(sm.add_constant(ts_in_oil))

if is_more_stationary(predictions_g_o,predictions_o_g):
    model = model_g_o
else:
    model = model_o_g
    
#%%
def backtesting_framework(start,end,data,strat):
    
    pnl = pd.dataframe()
    
    for i in range(start,end,delimiter=";",encoding='latin1', index_col=0):
        pnl = 
    return 2