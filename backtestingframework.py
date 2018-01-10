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

TICKER_LIST = ["BP_EQUITY","CAC_INDEX","CHEVRON_EQUITY","CNYUSD_CRRCY","CO1_COMDTY","CONOCOPHIL_INDEX","DJ_INDEX","EURGBP_CRRCY","EURUSD_CRRCY","EXON_EQUITY","LMECOPPER_COMDTY","MSCI_INDEX","NK_INDEX","NG1_COMDTY","SHELL_EQUITY","SPX_INDEX","TOTAL_EQUITY","USDGBP_CRRCY","XB1_COMDTY"]


    
#%%
enter=1.5
close=0.5
window=20
ticker1 =ticker_oil# "BP_EQUITY"
ticker2 = "XB1_COMDTY"

#df_pnl = pair_trading(ticker1,ticker2,K_up,K_down,window)

#%%

df1, df2 = get_same_dates(load_data_from_csv(ticker1), load_data_from_csv(ticker2))
    
# Sample data
df1_in, df1_out = sampling(df1)
df2_in, df2_out = sampling(df2)

# Compute the hedging ratio and get the spread to long
df_spread = get_spread(df1,df2)
df_spread_return = get_returns(df_spread)
#%%
def pair_trading(ticker1,ticker2,enter,close,window):
    
    # Load data
    df1, df2 = get_same_dates(load_data_from_csv(ticker1), load_data_from_csv(ticker2))
    
    # Sample data
    df1_in, df1_out = sampling(df1)
    df2_in, df2_out = sampling(df2)
    
    # Compute the hedging ratio and get the spread to long
    df_spread = get_spread(df1,df2)
    df_spread_return = get_returns(df_spread)
    
    df_pnl = pd.DataFrame(index=df1_out.index,columns=['PnL'])
    
    pos=0
    pnl=0
    pnl_r = 0
    
    invst=None
    for d in df1_out.index:
    
        
        zscore = get_zscore(d,df_spread,window)
        
        signal = get_signal(zscore,enter,close)
        
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
            
        
        df_pnl.loc[d]['PnL']=pos*df_spread_return.loc[d][0]
        
        #pnl_r+=pos*df_spread_return.loc[d]
        
    df_pnl['PnL'].plot()
    df_pnl.cumsum().plot()
    return df_pnl            
#%%                
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            