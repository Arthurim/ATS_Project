# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 22:03:24 2018

@author: Arthur
"""

import pandas as pd

def get_performance(dff):
    df = dff.copy()
    an_ret = get_annual_return(df)
    for y in an_ret.index:
        print("the annual return for year " + y + " was " + str(round(an_ret.loc[str(y)][0]*100,2))+"%")
    
    mdd, start, end = max_dd(pd.Series(dff['PnL'].values))
    print("Maximum draw down of "+ str(round(mdd*100,2))+ "% happened between "+  dff.index[start] + " and " + dff.index[end])
    sr = get_sharpe_ratio(dff)[0]
    print("Sharpe ratio of " + str(round(sr,2)))


def get_df_pnl_annual_index(df):
    K = []
    L = df.index.tolist()
    for d in L:
        K.append(d[6:10])
    df.set_index([K], inplace=True)
    return df
    
def get_annual_return(df):
    dfa = get_df_pnl_annual_index(df)
    d=get_annualised_return(dfa)
    return d

def get_annualised_return(df_pnl):
    y0 = int(df_pnl.index[0])
    yn = int(df_pnl.index[len(df_pnl)-1])
    dfy = pd.DataFrame(columns=['r'])
    for y in range(y0, yn + 1):
        dfy.loc[str(y)] = df_pnl.loc[str(y)].values.sum()
    return dfy

def max_dd(returns):
    """Assumes returns is a pandas Series"""
    r = returns.add(1).cumprod()
    dd = r.div(r.cummax()).sub(1)
    mdd = dd.min()
    end = dd.argmin()
    start = r.loc[:end].argmax()
    return mdd, start, end

def get_sharpe_ratio(dfr):
    return (dfr.mean() / dfr.std())

