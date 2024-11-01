#%%

#Black-Scholes-Merton Model

"""
Call = S*N(d1) - K*e^(-r*t)*N(d2)
Put = K*e^(-r*t)*N(-d2) - S*N(-d1)

S = Current Price of the asset
N() = normal cdf
K = Strike Price
r = rf rate
t = time till expiration
sigma = annualised volatility
d1 = (ln(S/K) + (r + (sigma**2)/2)*t)/(sigma*(t**(1/2)))
d2 = d1 - sigma*(t**(1/2))
"""

import numpy as np
import yfinance as yf
from scipy.stats import norm 
import matplotlib.pyplot as plt

N = norm.cdf
fig,ax = plt.subplots(2,2, figsize=(10,6))
fig.suptitle("BSM Model - Option Price as variables change")
fig.supylabel("Option Price")

def BSM_Call(S,K,r,t,sigma): # Price of a call using the BSM Model
    
    d1 = (np.log(S/K) + (r + ((sigma**2)/2))*t)/(sigma*np.sqrt(t))
    d2 = d1 - sigma*(np.sqrt(t))
    
    return (S * N(d1)) - K * np.exp(-r*t) * N(d2)

def BSM_Put(S,K,r,t,sigma): # Price of a put using the BSM Model
    
    d1 = (np.log(S/K) + (r + ((sigma**2)/2))*t)/(sigma*np.sqrt(t))
    d2 = d1 - sigma*(np.sqrt(t))
    
    return K * np.exp(-r*t) * N(-d2) - (S * N(-d1))

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

def price_v_time(K,r,ticker): # Price of an option as the time to maturity changes
    
    S = stock_price(ticker)
    sigma = stock_vol(ticker)
    t = np.linspace(1,5,10)
    
    calls = [BSM_Call(S,K,r,T,sigma) for T in t]
    puts = [BSM_Put(S,K,r,T,sigma) for T in t]
    
    ax[0,0].plot(t,calls,label = "Call Value")
    ax[0,0].plot(t,puts,label = "Put Value")
    ax[0,0].set_xlabel("Time")
    
def price_v_sigma(K,r,ticker,t=1): # Price of an option as the volatility changes
    
    S = stock_price(ticker)
    sigma = np.linspace(stock_vol(ticker)*0.8,stock_vol(ticker)*1.2,100)
        
    calls = [BSM_Call(S,K,r,t,Sigma) for Sigma in sigma]
    puts = [BSM_Put(S,K,r,t,Sigma) for Sigma in sigma]
    
    ax[0,1].plot(sigma,calls,label = "Call Value")
    ax[0,1].plot(sigma,puts,label = "Put Value")
    ax[0,1].set_xlabel("Sigma")
    
def price_v_exercise(r,ticker,t=1): # Price of an option as the strike price changes
    
    K = np.linspace(stock_price(ticker)*0.8, stock_price(ticker)*1.2,100)
    S = stock_price(ticker)
    sigma = stock_vol(ticker)
    
    calls = [BSM_Call(S,k,r,t,sigma) for k in K]
    puts = [BSM_Put(S,k,r,t,sigma) for k in K]
    
    ax[1,0].plot(K,calls,label = "Call Value")
    ax[1,0].plot(K,puts,label = "Put Value")
    ax[1,0].set_xlabel("Strike")

def price_v_rf(K,ticker,t=1): # Price of an option as the risk free rate changes
        
    S = stock_price(ticker)
    sigma = stock_vol(ticker)
    r = np.linspace(0.01, 0.08,50)
    
    calls = [BSM_Call(S,K,R,t,sigma) for R in r]
    puts = [BSM_Put(S,K,R,t,sigma) for R in r]
    
    ax[1,1].plot(r,calls,label = "Call Value")
    ax[1,1].plot(r,puts,label = "Put Value")
    ax[1,1].set_xlabel("Risk Free")
    
price_v_time(450, 0.05, "MSFT")
price_v_sigma(450, 0.05, "MSFT")
price_v_exercise(0.05, "MSFT")
price_v_rf(450, "MSFT")

plt.tight_layout()
plt.legend()
plt.show()


