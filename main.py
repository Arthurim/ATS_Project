# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 20:58:03 2018

@author: Arthur
"""

from trading_strategies import cointegration_trading, long, short
from performance import get_performance
from graph import graph_pnl, graph_pnls
from data_handling import path

def main():
    
    # tickers you want to apply the strategy to
    ticker1 = "SXEE_INDEX"
    ticker2 = "SXEP_INDEX"
    
    # define the parameters of the trading strategy
    enter = 1.5
    close = 0.5
    window = 15
    
    # dates for in sample and out of sample
    start_in = "09/10/2000"
    end_in = "31/12/2015"
    start_out = "01/01/2016"
    end_out = "02/01/2017"
    sampling_dates = [start_in,end_in,start_out,end_out]
    
    # compute the pnl of the co-integration strategy
    df_pnl1 = cointegration_trading(ticker1,ticker2,enter,close,window,"OUT",sampling_dates)
    
    fig = graph_pnl(df_pnl1)
    fig.savefig(path+ ticker1 + "_"+ ticker2+"_COINTEGRATION" +"_PNL.png")
    
    # test a S&P long only strategy
    long_ticker = "SPX_INDEX"
    df_pnl2 = long(long_ticker,sampling_dates,"OUT")
    
    fig = graph_pnl(df_pnl2)
    fig.savefig(path+ long_ticker +"_PNL.png")
    
    # look at the difference
    fig = graph_pnls(df_pnl1,df_pnl2)
    fig.savefig(path+ "COMPARISON" +"_PNL.png")
    
    
    # get performance
    get_performance(df_pnl1)
    get_performance(df_pnl2)
    
    # compare with other strategies
    #df_pnl = short(ticker1,sampling_dates,"OUT")
    #df_pnl = long(ticker1,sampling_dates,"OUT")
    return df_pnl1


if __name__ == "__main__":
    df_pnl_final = main()
    #df_pnl_final.cumsum().plot()
    
    