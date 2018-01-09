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
END_OUT = "01/02/2017"

path = "C:\\Users\\Arthur\\Documents\\Studies\\ParisDauphineUniversity\\Master203\\M2\\ATS\\project\\data\\"
ticker_oil = "CO1_COMDTY"
ticker_gas = "NG1_COMDTY"


#%%
# Load data
df1, df2 = get_same_dates(load_data_from_csv(ticker1), load_data_from_csv(ticker2))

# Sample data
df1_in, df1_out = sampling(df1)
df2_in, df2_out = sampling(df2)

# Compute the hedging ratio and get the spread to long
df_spread = get_spread(df1, df2)

# model is OIL - ratio * GAS = const if spread = 1
# else if spread = -1 it is OIL - GAS/ratio = - const/ratio
ratio, spread = get_ratio(df1, df2)

if spread == 1:
    data_spread = df1['Value'].values - ratio * df2['Value'].values
else:
    data_spread = df2['Value'].values - ratio * df1['Value'].values

df_spread = pd.DataFrame(data_spread, index = df1.index, columns=['Value'])

df_spread_return = get_returns(df_spread)

invst = None
pnl=0
#%%
window = 15
K_up = 1.5
K_down = 0.5
base_quantity = 10000

df_out_oil['Position'] = 0
df_out_gas['Position'] = 0
          
df_pf_val = pd.DataFrame(index = df_out_oil.index, columns=['Value'])

udl_list = [df_out_oil, df_out_gas]

prev_d = df_out_oil.index[0]          
pnl=0
spread = 15
pos=0

invst = None

#%%
pnl=0

pnl_r = 0

invst=None
for d in df1_out.index:

    
    zscore = get_zscore(d,df_spread,window)
    
    signal = get_signal(zscore,K_up,K_down)
    
    if invst is None:
        if signal is "LONG_ENTRY":
            pos = 1
            invst = "Long"
            print(signal+" on the " + str(d))
        elif signal is "SHORT_ENTRY":
            pos = -1
            invst = "Short"
            print(signal+" on the " + str(d))
            
    if invst is not None:       
        if invst is "Short" and signal is "SHORT_CLOSE":
            pos = 1
            invst = None
            print(signal+" on the " + str(d))
        elif invst is "Long" and signal is "LONG_CLOSE":
            pos = -1
            invst = None
            print(signal+" on the " + str(d))
        
        
    pnl+=pos*df_spread.loc[d]
    
    pnl_r+=pos*df_spread_return.loc[d]
    
print('P&L is ', pnl[0])



#%%
def get_portfolio_value(d, udl_list):
    pf = 0
    for df in udl_list:
        pf += df.loc[d]['Position']*df.loc[d]['Value']
    return pf
    
    
#%%
def pair_trading(start, end, ticker1, ticker2, entry, close, window):
    
    # Load data
    df1, df2 = get_same_dates(load_data_from_csv(ticker1), load_data_from_csv(ticker2))
    
    # Sample data
    df1_in, df1_out = sampling(df1)
    df2_in, df2_out = sampling(df2)
    
    # Compute the hedging ratio and get the spread to long
    df_spread = get_spread(df1,df2)
    
    window = 15
    K_up = 1.5
    K_down = 0.5
    
    for d in df_spread.index:
        
        zscore = get_zscore(d, df_spread, window)
        
        signal = get_signal(zscore,K_up,K_down)
        print(signal)
        
        if signal in ["LONG_ENTRY","SHORT_CLOSE"]:
            pos = 1
        elif signal in ["LONG_CLOSE","SHORT_ENTRY"]:
            pos = -1
        else:
            pos = 0
            
        pnl+=pos*df_spread.loc[d]
        
        df_out_oil['Position'] = pos * w_oil
        df_out_gas['Position'] = pos * w_gas
                
                
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            