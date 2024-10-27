#%%

# Question 1 and Question 2

"""
As the tax-rate does not affect the coupon payments, 
I have excluded its effect on the price of the bond.

However, assuming the tax rate reduces the coupon payments, 
I have calculated a secondary Present Value of the bond which 
DOES NOT reflect its market price. This just represents the present value
of all cash flows.

"""

import numpy as np

def PV_Bond(coupon_rate,fv,discount_rate,maturity,freq_no):

    coupon = fv * coupon_rate / freq_no

    pv_payout = []

    for i in range(1,(maturity*freq_no)+1):
        
        pv_payout += [(coupon/((1+(discount_rate/freq_no))**(i)))]
    
    pv_payout[(maturity*freq_no)-1] = pv_payout[(maturity*freq_no)-1]+(fv/((1+(discount_rate/freq_no))**(maturity*freq_no)))

    pv_payout = np.array(pv_payout)

    pv_bond = pv_payout.sum()
    
    return pv_bond,pv_payout
    
def MD_Bond(pv_bond,pv_payout,maturity,freq_no,discount_rate):
    
    pv_payout = pv_payout/pv_bond

    duration = 0

    for i in range(1,(maturity*freq_no)+1):
        
        duration += i*pv_payout[i-1]
        
    modified_dur = (duration/freq_no)/(1+(discount_rate/freq_no))
    
    return modified_dur
    
    
coupon_rate = float(input("Enter the coupon rate (%): "))/100

fv = int(input("Enter the face value: "))

discount_rate = float(input("Enter the discount rate (%): "))/100

maturity = int(input("Enter years to maturity: "))

freq_dict = {"Monthly":12,"Quarterly":4,"Semi-Annually":2,"Annually":1}
freq_no = freq_dict[str(input("Enter frequency (Monthly, Quarterly, Semi-Annually, Annually): "))]

pv,payout = PV_Bond(coupon_rate, fv, discount_rate, maturity, freq_no)

print("Present value of the bond (not accounting for taxes) is:",round(pv,3))

md = MD_Bond(pv,payout, maturity, freq_no,discount_rate)

print("Modified duration of the bond (not accounting for taxes) is:",round(md,3))

#%%

"""
Assuming we take into account the effect of taxation of coupon payments,
the payout gets reduced by the buyer's tax rate.
The Present Value calculated here is NOT the market price,
it is just the PV of all the cash flows after accounting for taxation. 
Same goes for the calculated modified duration.
"""

import numpy as np

def PV_Bond(tax_rate,coupon_rate,fv,discount_rate,maturity,freq_no):

    coupon = fv * coupon_rate / freq_no

    pv_payout = []

    for i in range(1,(maturity*freq_no)+1):
        
        pv_payout += [((coupon*(1-tax_rate))/((1+(discount_rate/freq_no))**(i)))]
    
    pv_payout[(maturity*freq_no)-1] = pv_payout[(maturity*freq_no)-1]+(fv/((1+(discount_rate/freq_no))**(maturity*freq_no)))

    pv_payout = np.array(pv_payout)

    pv_bond = pv_payout.sum()
    
    return pv_bond,pv_payout
    
def MD_Bond(pv_bond,pv_payout,maturity,freq_no):
    
    pv_payout = pv_payout/pv_bond

    duration = 0

    for i in range(1,(maturity*freq_no)+1):
        
        duration += i*pv_payout[i-1]
        
    modified_dur = (duration/freq_no)/(1+(discount_rate/freq_no))
    
    return modified_dur
    
tax_rate = float(input("Enter the tax rate (%): "))/100
coupon_rate = float(input("Enter the coupon rate (%): "))/100

fv = int(input("Enter the face value: "))

discount_rate = float(input("Enter the discount rate (%): "))/100

maturity = int(input("Enter years to maturity: "))

freq_dict = {"Monthly":12,"Quarterly":4,"Semi-Annually":2,"Annually":1}
freq_no = freq_dict[str(input("Enter frequency (Monthly, Quarterly, Semi-Annually, Annually): "))]

pv,payout = PV_Bond(tax_rate,coupon_rate, fv, discount_rate, maturity, freq_no)

print("Present value of the bond (not accounting for taxes) is:",round(pv,3))

md = MD_Bond(pv,payout, maturity, freq_no)

print("Modified duration of the bond (not accounting for taxes) is:",round(md,3))
