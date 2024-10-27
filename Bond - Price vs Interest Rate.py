#%%

import numpy as np
import matplotlib.pyplot as plt

def PV_Bond(coupon_rate,fv,discount_rate,maturity,freq_no):

    coupon = fv * coupon_rate / freq_no

    pv_payout = []

    for i in range(1,(maturity*freq_no)+1):
        
        pv_payout += [(coupon/((1+(discount_rate/freq_no))**(i)))]
    
    pv_payout[(maturity*freq_no)-1] = pv_payout[(maturity*freq_no)-1]+(fv/((1+(discount_rate/freq_no))**(maturity*freq_no)))

    pv_payout = np.array(pv_payout)

    return round(pv_payout.sum(),3)

    
coupon_rate = float(input("Enter the coupon rate (%): "))/100
fv = int(input("Enter the face value: "))
maturity = int(input("Enter years to maturity: "))
freq_dict = {"Monthly":12,"Quarterly":4,"Semi-Annually":2,"Annually":1}
freq_no = freq_dict[str(input("Enter frequency (Monthly, Quarterly, Semi-Annually, Annually): "))]

discount_rates = np.linspace(1, 10, 100)/100

bond_prices = []

for i in discount_rates:
    
    bond_prices += [PV_Bond(coupon_rate,fv,i,maturity,freq_no)]
    
x = discount_rates
y = bond_prices

plt.figure(figsize=(10,10))
plt.xlabel("Interest Rate")
plt.ylabel("Bond Prices")
plt.suptitle("Price vs Interest Rate")
plt.plot(x,y)

