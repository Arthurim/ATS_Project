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


def get_signal(zscore,entry,close):
    if zscore <= -entry:
        return "LONG_ENTRY"
    if zscore > entry:
        return "SHORT_ENTRY"
    if zscore >= -close:
        return "LONG_CLOSE"
    if zscore <= close:
        return "SHORT_CLOSE"
    
def get_zscore(day,pf_price,rolling_mean,rolling_std):
    zscore = ( pf_price[day] - rolling_mean[day]) / rolling_std[day]
    return zscore

#%%


df_oil_p = load_data_from_csv(ticker_oil)
df_gas_p = load_data_from_csv(ticker_oil2)
df_oil_p, df_gas_p = get_same_dates(df_oil, df_gas)

df_in_oil, df_out_oil = sampling(df_oil)
df_in_gas, df_out_gas = sampling(df_gas)

# model is OIL - ratio * GAS = const if spread = 1
# else if spread = -1 it is OIL - GAS/ratio = - const/ratio
const, ratio, spread = get_ratio(df_in_oil, df_in_gas)

window = 15
entry = 1.5
close = 0.5
base_quantity = 10000

df_out_oil['Position'] = 0
df_out_gas['Position'] = 0
df_pf_val = pd.DataFrame(index = df_out_oil.index, columns=['Value'])
df_spread = pd.DataFrame(data = df_out_gas['Value'].values-df_out_oil['Value'].values, index = df_out_oil.index, columns=['Value'])

udl_list = [df_out_oil, df_out_gas]

prev_d = df_out_oil.index[0]          
pnl=0
spread = 15
pos=0

#%%
for d in df_out_gas.index:
    
    df_pf_val.loc[d]['Value'] = get_portfolio_value(d, udl_list)
    
    zscore = get_zscore(d,df_spread,window)
    
    signal = get_signal(zscore,entry,close)
    print(signal)
    
    if signal in ["LONG_ENTRY","SHORT_CLOSE"]:
        pos = 1
    elif signal in ["LONG_CLOSE","SHORT_ENTRY"]:
        pos = -1
    else:
        pos = 0
    
    df_out_oil['Position'] = pos * w_oil
    df_out_gas['Position'] = pos * w_gas



#%%
def get_portfolio_value(d, udl_list):
    pf = 0
    for df in udl_list:
        pf += df.loc[d]['Position']*df.loc[d]['Value']
    return pf
    
    
#%%
def backtesting(start, end, entry, close, rolling_period):
    
    df_oil_p = load_data_from_csv(ticker_oil)
    df_gas_p = load_data_from_csv(ticker_gas)
    df_oil_p, df_gas_p = get_same_dates(df_oil, df_gas)
    
    df_in_oil, df_out_oil = sampling(df_oil)
    df_in_gas, df_out_gas = sampling(df_gas)
    
    hedging_ratio = get_ratio(df_in_oil, df_in_gas)
    rolling_period = 15
    entry = 1.5
    close = 0.5
    base_quantity = 10000

    
    for i in range(len(df)):
        
        zscore = get_zscore(day)
        signal = get_signal(zscore,entry,close)
        
        if signal
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            