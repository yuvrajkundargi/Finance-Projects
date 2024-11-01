#%%

# Calculating Implied Volatility for Call Options

import numpy as np
import yfinance as yf
from scipy.stats import norm
import scipy.optimize as opt
from datetime import datetime

N = norm.cdf
today = datetime.now()
ticker = input("Enter stock ticker:")

def TNX_yield(): # 10 Year Treasury Yield
    
    data = yf.Ticker("^TNX")
    yield_data = data.history(period='1d')
    
    return float(yield_data["Close"].iloc[-1])/100

def stock_price(ticker): # Latest stock price using ticker as input
    
    stock_tic = yf.Ticker(ticker)
    stock_data = stock_tic.history(period = "1mo")

    return stock_data["Close"].iloc[-1]

def stock_vol(ticker): # 1 year annualised volatility using ticker as input

    stock_tic = yf.Ticker(ticker)
    stock_data = stock_tic.history(period = "1y")
    stock_data["Returns"] = stock_data["Close"].pct_change()  
    stock_data = stock_data.dropna()    
    stock_std = stock_data["Returns"].std()*np.sqrt(252)
    
    return stock_std

def Call_Option_Data(ticker): # Extract call option data
    
    stock = yf.Ticker(ticker)
    print("Expiration Dates:",stock.options)

    date = input("Enter expiration date:")

    expiration = datetime.strptime(date,"%Y-%m-%d") - today
    expiration_years = expiration.days/365
    
    options_chain = stock.option_chain(date)
    calls = options_chain.calls
    strikes = calls["strike"]
    idx = len(strikes)//2
    strike = strikes.iloc[idx]
    prices = calls["lastPrice"]
    price = prices.iloc[idx]
    return expiration_years,strike,price

def BSM_Call(S,K,r,t,sigma): # Price of a call using the BSM Model
    
    d1 = (np.log(S/K) + (r + ((sigma**2)/2))*t)/(sigma*np.sqrt(t))
    d2 = d1 - sigma*(np.sqrt(t))
    
    return (S * N(d1)) - K * np.exp(-r*t) * N(d2)

def BSM_Put(S,K,r,t,sigma): # Price of a put using the BSM Model
    
    d1 = (np.log(S/K) + (r + ((sigma**2)/2))*t)/(sigma*np.sqrt(t))
    d2 = d1 - sigma*(np.sqrt(t))
    
    return K * np.exp(-r*t) * N(-d2) - (S * N(-d1))

def Implied_Vol_Call(S,K,r,t,market_price,ticker): # Optimiser to calculate implied volatility for a call option
    
    obj_func = lambda sigma: BSM_Call(S, K, r, t, sigma) - market_price
    
    initial_guess = stock_vol(ticker)
    
    implied_vol = opt.newton(obj_func, initial_guess)
    
    return implied_vol

S = stock_price(ticker)

t , K, market_price = Call_Option_Data(ticker)

r = TNX_yield()

implied_volatility = Implied_Vol_Call(S, K, r, t, market_price, ticker)



