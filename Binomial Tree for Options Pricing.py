#%%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

K = 100 # option strike price
T = 1 # time to maturity (in years)
r1 = 0.05 # annualized, continuously compounded return of 3-month T-bill - USE THIS FOR DISCOUNTING
r2 = 0.10 # annualized, continuously compounded return of S&P 500 index - IRRELEVANT
r3 = 0.20 # annualized, continuously compounded return of Xmazon - IRRELEVANT
sigma2 = 0.2 # volatility (i.e. annualized standard deviation) of S&P 500 index - IRRELEVANT
sigma3 = 0.3 # volatility (i.e. annualized standard deviation) of Xmazon - USE THIS VOLATILITY
S = [50+x for x in range(0,101,5)]
N= 100

# Calculating parameters

dt = T/N # Time Step
u = np.exp(sigma3*np.sqrt(dt)) # Up factor
d = 1/u # Down factor
p = (np.exp(r1*dt)-d)/(u-d) # Price movement probability

# Initialise dataframes for binomials

optree = pd.DataFrame(1.0,index=[i for i in range(0,N+1)], columns=[x for x in range(0,N+1)])
payoff = pd.DataFrame(1.0,index=[i for i in range(0,N+1)], columns=[x for x in range(0,N+1)])
eur_value = pd.DataFrame(1.0,index=[i for i in range(0,N+1)], columns=[x for x in range(0,N+1)])
amr_value = pd.DataFrame(1.0,index=[i for i in range(0,N+1)], columns=[x for x in range(0,N+1)])

# Functions to calculate payoffs

# This populates the binomial tree with payoffs for either a call or put at every time step

def cp_payoff_eur(K,optype,optree): 
    
    payoff = pd.DataFrame(1.0,index=[i for i in range(0,N+1)], columns=[x for x in range(0,N+1)])
    
    if optype == "Call":
        for i in range(1,N+1):
            for j in range(0,N+1):
                payoff.iloc[i,j] = max(optree.iloc[i,j] - K,0)
    else:
        for i in range(1,N+1):
            for j in range(0,N+1):
                payoff.iloc[i,j] = max(K - optree.iloc[i,j],0)

    return payoff

# This calculates the present value of a European option

def cp_value_eur(K, optype, optree):
    
    eur_value = pd.DataFrame(1.0,index=[i for i in range(0,N+1)], columns=[x for x in range(0,N+1)])
    
    payoff = cp_payoff_eur(K, optype, optree)
    
    eur_value.iloc[N,] = payoff.iloc[N,]
    
    for i in range(N-1,-1,-1):
        for j in range(0,N):
            eur_value.iloc[i,j] = np.exp(-r1*dt)*(((eur_value.iloc[i+1,j])*p) + (eur_value.iloc[i+1,j+1]*(1-p)))
    
    return eur_value

# This calculates the present value of an American option

def cp_value_amr(K,optype, optree):
    
    payoff = cp_payoff_eur(K,optype, optree)
    
    value = cp_value_eur(K,optype, optree)
    
    for i in range(0,N):
        for j in range(0,N):
            amr_value.iloc[i,j] = max(payoff.iloc[i,j],value.iloc[i,j])
            
    for i in range(0,N):
        for j in range(0,i+1):
            amr_value.iloc[i,j] = np.exp(-r1*dt)*(((amr_value.iloc[i+1,j])*p) + (amr_value.iloc[i+1,j+1]*(1-p)))
            
    return amr_value

def probtree(N,S):
    
    optree = pd.DataFrame(1.0,index=[i for i in range(0,N+1)], columns=[x for x in range(0,N+1)])

    for i in range(0,N):
        optree.iloc[i+1,0] = optree.iloc[i,0] * (u)
    
    for i in range(0,N):
        for j in range(0,i+1):
            optree.iloc[i+1,j+1] = optree.iloc[i,j] * d

    for i in range(0,N+1):
        for j in range(0,N+1):
            optree.iloc[i,j] = optree.iloc[i,j] * S
    
    return optree

def call_plt(K,N,S,optree):
    
    value1 = []
    value2 = []
    payoff = []
    
    for i in S:
    
        optree = probtree(N, i)
        value1 += [cp_value_eur(K, "Call", optree).iloc[0,0]]
        value2 += [cp_value_amr(K, "Call", optree).iloc[0,0]]
    
        if i<K:
            payoff += [0]
        else:
            payoff += [i-K]
    
    plt.figure()
    plt.plot(S,value1,label="European Call",color = "Blue")
    plt.plot(S,value2,label="American Call", color = "Red")
    plt.plot(S,payoff,label="Call Payoff", color = "Green")
    plt.ylabel("Call Price/Payoff")        
    plt.xlabel("Stock Price")
    plt.title("Figure 1")
    plt.legend()
    plt.show()
    
def put_plt(K,N,S,optree):
    
    value1 = []
    value2 = []
    payoff = []
    
    for i in S:
    
        optree = probtree(N, i)
        value1 += [cp_value_eur(K, "Put", optree).iloc[0,0]]
        value2 += [cp_value_amr(K, "Put", optree).iloc[0,0]]
    
        if i>K:
            payoff += [0]
        else:
            payoff += [K-i]
    
    plt.figure()
    plt.plot(S,value1,label="European Put", color = "Blue")
    plt.plot(S,value2,label="American Put", color="Red")
    plt.plot(S,payoff,label="Put Payoff", color="Green")
    plt.ylabel("Put Price/Payoff") 
    plt.xlabel("Stock Price")
    plt.title("Figure 2")
    plt.legend()
    plt.show()
    
call_plt(K, N, S, optree)
put_plt(K, N, S, optree)




