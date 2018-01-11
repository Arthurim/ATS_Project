# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:14:11 2018

@author: Arthur
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

# return the trading signals from a Zscore and two lvls
def get_signal(zscore,entry,close):
    if zscore <= -entry:
        return "LONG_ENTRY"
    if zscore > entry:
        return "SHORT_ENTRY"
    if zscore >= -close:
        return "LONG_CLOSE"
    if zscore <= close:
        return "SHORT_CLOSE"
    
# compute the Z score with a rolling window
def get_zscore(day, pf_value,window):
    value = pf_value.loc[day][0]
    roll_avg = pd.rolling_mean(pf_value,window).loc[day][0]
    roll_std =pd.rolling_std(pf_value,window).loc[day][0]
    return (value-roll_avg )/ roll_std 

# compute the hedging ratio and returns the spread data
def get_spread(df1,df2):
    # model is OIL - ratio * GAS = const if spread = 1
    # else if spread = -1 it is OIL - GAS/ratio = - const/ratio
    ratio, spread = get_ratio(df1, df2)
    print(spread)
    if spread == 1:
        data_spread = df1['Value'].values - ratio * df2['Value'].values
    else:
        data_spread = df2['Value'].values - ratio * df1['Value'].values
    
    df_spread = pd.DataFrame(data_spread, index = df1.index, columns=['Value'])
    return df_spread

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

#def returns the bollinger band for a certain K lvl and a window
def get_bollinger(df_spread,K,window,P):
    df_bollinger = pd.DataFrame(index=df_spread.index, columns=['K'])
    for d in df_bollinger.index:
        df_bollinger.at[d,'K'] = pd.rolling_mean(df_spread,window).loc[d] + P*K *pd.rolling_std(df_spread,window).loc[d]
    return df_bollinger


###############################################################################
################################# STATIONARITY ################################
###############################################################################


# return true if the time serie is stationarry, else false
def is_stationary(ts):
        return adfuller(ts)[1]<0.05

# tells if one serie is more stationary than another by comparing their ADF tests stats
def is_more_stationary(ts1,ts2):
    return adfuller(ts1)[0]<adfuller(ts2)[0]
