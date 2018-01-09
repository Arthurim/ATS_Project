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
START_IN = "04/10/2005"
END_IN = "11/12/2015"
START_OUT = "16/12/2015"
END_OUT = "21/12/2017"

path = "C:\\Users\\Arthur\\Documents\\Studies\\ParisDauphineUniversity\\Master203\\M2\\ATS\\project\\data\\"
ticker_oil = "CO1_COMDTY"
ticker_gas = "NG1_COMDTY"
ticker_oil2= "XB1_COMDTY"
#%%
#Load data and clean it
def load_data_from_csv(ticker):
    df = pd.read_csv(path+ticker+".csv", delimiter=";",encoding='latin1', index_col=0, header=None)
    df.columns = ['Value']
    df = df.dropna()
    return df

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
'''
def make_stationary(ts):
    while(not is_stationary(ts))
        ts = diff(ts)
    return ts'''
    
def is_more_stationary(ts1,ts2):
    return adfuller(ts1)[0]<adfuller(ts2)[0]

def get_same_dates(df1,df2):
    idx = df1.index.intersection(df2.index)
    df1 = df1.loc[idx]
    df2 = df2.loc[idx]
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

def get_signal(zscore,entry,close):
    if zscore <= -entry:
        return "LONG_ENTRY"
    if zscore > entry:
        return "SHORT_ENTRY"
    if zscore >= -close:
        return "LONG_CLOSE"
    if zscore <= close:
        return "SHORT_CLOSE"
    
def get_zscore(day, pf_value,window):
    value = pf_value.loc[day] 
    roll_avg = pd.rolling_mean(pf_value,window).loc[day]
    roll_std =pd.rolling_std(pf_value,window).loc[day]
    return ( (value-roll_avg )/ roll_std )[0]

def get_spread(df1,df2):
    # model is OIL - ratio * GAS = const if spread = 1
    # else if spread = -1 it is OIL - GAS/ratio = - const/ratio
    ratio, spread = get_ratio(df1, df2)

    if spread == 1:
        data_spread = df1['Value'].values - ratio * df2['Value'].values
    else:
        data_spread = df2['Value'].values - ratio * df1['Value'].values
    
    df_spread = pd.DataFrame(data_spread, index = df1.index, columns=['Value'])
    return df_spread
#%%

# compute the hedging ratio for the spread
def get_ratio(df_in_1, df_in_2):

    ts_in_1 = df_in_1['Value']
    ts_in_2 = df_in_2['Value']
    
    # test the two regressions models
    model_1on2 = sm.OLS(ts_in_1,sm.add_constant(ts_in_2)).fit()
    resid_1on2 = model_1on2.resid
    
    model_2on1 = sm.OLS(ts_in_2,sm.add_constant(ts_in_1)).fit()
    resid_2on1 = model_2on1.resid
    
    # then chose the regression model for which the stationarity is more important
    if is_more_stationary(resid_2on1,resid_1on2):
        hedge_ratio = model_2on1.params[1]
        return hedge_ratio, -1
    else:
        hedge_ratio = model_1on2.params[1]
        return hedge_ratio, 1
#%%
df_oil = load_data_from_csv(ticker_oil)
df_gas = load_data_from_csv(ticker_oil2)
df_oil, df_gas = get_same_dates(df_oil, df_gas)

pd.concat([df_oil, df_gas], axis=1).plot()
pd.concat([np.log(df_oil), np.log(df_gas)], axis=1).plot()

#%%
df_in_oil, df_out_oil = sampling(df_oil)
df_in_gas, df_out_gas = sampling(df_gas)


#%%
ts_in_oil = df_in_oil[ticker_oil + ' Returns']
ts_in_gas = df_in_gas[ticker_oil2 + ' Returns']


model_o_g = sm.OLS(ts_in_oil,sm.add_constant(ts_in_gas)).fit()
predictions_o_g = model_o_g.predict(sm.add_constant(ts_in_gas))
resid_o_g = model_o_g.resid

model_g_o = sm.OLS(ts_in_gas,sm.add_constant(ts_in_oil)).fit()
predictions_g_o = model_g_o.predict(sm.add_constant(ts_in_oil))
resid_g_o = model_g_o.resid

if is_more_stationary(resid_g_o,resid_o_g):
    hedge_ratio = model_g_o.params[1]
else:
    hedge_ratio = model_o_g.params[1]
    





