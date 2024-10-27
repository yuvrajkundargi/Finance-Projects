#%%

"""
Data extraction from wrds. 
Create your account and enter the username in the conn function.
Add a path to the to_csv function on line 40 to store the price data as it is used in the next code.
"""

import wrds
import pandas as pd

conn = wrds.Connection(wrds_username="")

query_1 = """
    select a.fic, a.datadate, a.prccd, a.conm
    from comp.g_secd a
    where a.conm='TESCO PLC' and a.datadate>='1991-01-01' and a.datadate<='1995-12-31'
"""

tesco_raw = conn.raw_sql(query_1)

query_2 = """
    select a.fic, a.datadate, a.prccd, a.conm
    from comp.g_secd a
    where a.conm='SAINSBURY (J) PLC' and a.datadate>='1991-01-01' and a.datadate<='1995-12-31'
"""

sains_raw = conn.raw_sql(query_2)

tesco_raw["datadate"] = pd.to_datetime(tesco_raw["datadate"],format = "%Y-%m-%d")
sains_raw["datadate"] = pd.to_datetime(sains_raw["datadate"],format = "%Y-%m-%d")


tesco_raw = tesco_raw.rename(columns = {"prccd":"Tesco CP"})
sains_raw = sains_raw.rename(columns = {"prccd":"Sains CP"})

price_data = pd.merge(tesco_raw,sains_raw, how="inner", on="datadate")
price_data = price_data.sort_values(by="datadate").reset_index(drop=True)

price_data.to_csv(r"")

#%%

"""
Creates an efficient frontier plot for a portfolio of two securities as called from above.
Add path to the read_csv to access the price data, same as the path created above.
Add another path to the to_csv function on line 101 to write data if you want to check it.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

price_data = pd.read_csv(r"")

price_data = price_data.drop(columns = ["fic_x","fic_y","conm_x","conm_y","Unnamed: 0"])
price_data = price_data.set_index("datadate")



price_data["pct_ret_tesco"] = price_data["Tesco CP"].pct_change()
price_data["pct_ret_sains"] = price_data["Sains CP"].pct_change()

price_data = price_data.iloc[1:]
print(price_data.shape)
tesco_ret = ((price_data.iloc[1213,0]/price_data.iloc[0,0])**(1/5)) -1
sains_ret = ((price_data.iloc[1213,1]/price_data.iloc[0,1])**(1/5)) -1

print(tesco_ret,sains_ret)

tesco_std = price_data["pct_ret_tesco"].std()*np.sqrt(252)
sains_std = price_data["pct_ret_sains"].std()*np.sqrt(252)

print(tesco_std,sains_std)

correl = price_data.corr().loc["pct_ret_tesco","pct_ret_sains"]

print(correl)

cov = price_data.cov().loc["pct_ret_tesco","pct_ret_sains"]*252
print(cov)

weights = np.linspace(0, 1, num=50)

weighted_ret = []

for i in weights:
    weighted_ret += [(tesco_ret*i) + (sains_ret*(1-i))]

print(weighted_ret)

portfolio_std = []

for i in weights:
     portfolio_std += [np.sqrt((((i**2)*(tesco_std**2)) + (((1-i)**2)*(sains_std**2)) + 2*i*(1-i)*cov))]

data_out = pd.DataFrame()
data_out["Weights"] = weights
data_out["Weighted Return"] = weighted_ret
data_out["Std Dev"] = portfolio_std
data_out.to_csv(r"")

plt.figure(figsize=(10,6))
plt.xlabel("Std Dev")
plt.ylabel("Weighted Return")
plt.suptitle("Mean-Variance Plot")

plt.plot(portfolio_std,weighted_ret)