# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:02:12 2018

@author: Arthur
"""
import pandas as pd
from data_handling import get_same_dates, path, load_data_from_csv, get_returns, sampling_two, sampling_one, get_next_day
from trading_signals import get_zscore, get_signal, get_spread
from graph import graph_spread#, graph_pnl


def short(ticker,sampling_dates,inout):
    return long(ticker,sampling_dates,inout,-1)

def long(ticker,sampling_dates,inout,pos=1):
    print(pos)
    df = load_data_from_csv(ticker)
    df_in, df_out = sampling_one(df,sampling_dates)
    
    df_returns_in = get_returns(df_in)
    df_returns_out = get_returns(df_out)
    
    # do we bactest on in sample or on out of sample
    if inout is "IN":
        df_returns = df_returns_in
        print("Start backtest on in sample")
    elif inout is "OUT":
        df_returns = df_returns_out
        print("Start backtest on out of sample")
    else: 
        print("IN/OUT sample parameter is invalid")
        return pd.DataFrame()
    
    df_returns.cumsum().plot()
    df_returns.columns=['PnL']
    if pos == 1:
        return df_returns[1:]
    else:
        return -df_returns[1:]
    
    
# Cointegration trading strategy using bollinger bands
def cointegration_trading(ticker1,ticker2,enter,close,window,inout,sampling_dates):
    
    # Load data
    df1, df2 = get_same_dates(load_data_from_csv(ticker1), load_data_from_csv(ticker2))
    
    # Sample data
    df1_in, df1_out,df2_in, df2_out = sampling_two(df1,df2,sampling_dates)

    # Compute the hedging ratio and get the spread to long
    df_spread_in = get_spread(df1_in,df2_in)
    df_spread_out = get_spread(df1_out,df2_out)
    df_spread_return_out = get_returns(df_spread_out)
    df_spread_return_in = get_returns(df_spread_in)
    
    pos=0    
    invst=None
    
    # do we bactest on in sample or on out of sample
    if inout is "IN":
        df_pnl = pd.DataFrame(index=df1_in.index,columns=['PnL'])
        df = df_spread_in
        df_spread_return = df_spread_return_in
        print("Start backtest on in sample")
    elif inout is "OUT":
        df_pnl = pd.DataFrame(index=df1_out.index,columns=['PnL'])
        df = df_spread_out
        df_spread_return = df_spread_return_out
        print("Start backtest on out of sample")
    else: 
        print("IN/OUT sample parameter is invalid")
        return pd.DataFrame()
    
    fig = graph_spread(df_spread_out,enter,close,window)
    fig.savefig(path+"myspread.png")
    
    for d in df.index[:-1]:
        
        zscore = get_zscore(d,df,window)
        
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
                pos = 0
                invst = None
                print(signal+" on the " + str(d))
            elif invst is "Long" and signal is "LONG_CLOSE":
                pos = 0
                invst = None
                print(signal+" on the " + str(d))
            
        next_d = get_next_day(d,df)
        df_pnl.loc[next_d]['PnL']=pos*df_spread_return.loc[next_d][0]
        
    return df_pnl[1:]       
            