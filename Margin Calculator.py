#%%

"""

Margin calculator for a forwards contract.
Input is list of future prices, strike/exercise of contract, the margin, the maintenace level.
Change value of variable long if forward is being sold/going short.

"""

strike = 100

future_price = [98, 94, 98, 103, 105] # Can be any list of future prices

fp_change = [future_price[0] - strike]
fp_change += [future_price[i] - future_price[i-1] for i in range(1,len(future_price))]

margin = 15
maintenance = 10
deposit = []

long = 1 # +1 for Long, -1 for Short

def PL_Future(fp_change,margin,maintenance,deposit,long):
    
    for i in fp_change:
        
        margin = margin + (long*i)
        
        if margin <= maintenance:
            deposit += [15-margin]

            margin = 15

    profit = margin - sum(deposit) - 15
    
    return profit
    
profit = PL_Future(fp_change, margin, maintenance, deposit,long)

print(profit)