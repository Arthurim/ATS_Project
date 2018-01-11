# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:32:39 2018

@author: Arthur
"""
from trading_signals import get_bollinger
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import statsmodels.api as sm
import numpy as np

# plot the spread with its bollinger bands    
def graph_spread(df_spread,enter,close,window):
    fig, ax = plt.subplots()
    data = df_spread.values
    entry_l = get_bollinger(df_spread,enter,window,-1).values
    close_l = get_bollinger(df_spread,close,window,-1).values
    entry_s = get_bollinger(df_spread,enter,window,1).values
    close_s = get_bollinger(df_spread,close,window,1).values
    ax.plot(data)
    ax.plot(entry_l, 'r--', color='green')
    ax.plot(entry_s, 'r--', color='green')
    ax.plot(close_l, 'r--',color='red')
    ax.plot(close_s, 'r--', color='red')
    
    x = np.arange(data.shape[0])
    myt=df_spread.index.values.tolist()
    plt.xticks(x[::75], myt[::75])
    
    #ax.xaxis.set_ticks(range(len(myt)))
    #ax.xaxis.set_ticklabels(myt,rotation='vertical')
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    #plt.tight_layout()
    return fig
    
# plot acf and pcf of a time serie
def plot_acf_pacf(ts):
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(2,1,1)
    fig = sm.graphics.tsa.plot_acf(ts, lags=20, ax=ax1)
    ax2 = fig.add_subplot(2,1,2)
    fig = sm.graphics.tsa.plot_pacf(ts, lags=20, ax=ax2)  
    return fig

def graph_pnl(df_pnl):
    data = df_pnl.cumsum().values
    fig, ax = plt.subplots()
    ax.plot(data)
    myt=df_pnl.index.values.tolist()
    x = np.arange(data.shape[0])
    myt=df_pnl.index.values.tolist()
    plt.xticks(x[::75], myt[::75])
    
#    ax.xaxis.set_ticks(range(len(myt)))
#    ax.xaxis.set_ticklabels(myt,rotation='vertical')
#    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    return fig
    
def graph_pnls(df_pnl1,df_pnl2):
    plt.tight_layout()
    data1 = df_pnl1.cumsum().values
    data2 = df_pnl2.cumsum().values
    fig, ax = plt.subplots()
    ax.plot(data1)
    ax.plot(data2)
    myt=df_pnl1.index.values.tolist()
    x = np.arange(data1.shape[0])
    myt=df_pnl1.index.values.tolist()
    plt.xticks(x[::75], myt[::75])
    
#    ax.xaxis.set_ticks(range(len(myt)))
#    ax.xaxis.set_ticklabels(myt,rotation='vertical')
#    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    return fig    
    
    