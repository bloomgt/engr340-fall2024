"""
This problem requires you to calculate compounding interest and final value of a  US treasury deposit based upon
current interest rates (that will be provided). Your analysis should return the final value of the investment
after a 1-year and 20-year period. The final values should be stored in the variables "ten_year_final"
and "twenty_year_final", respectively. Perform all your calculations in this file. Do not perform the calculations by hand
and simply write in the final result.

Prompt: On October 27th, 2022, Elon Musk purchased Twitter for $44B in total, with reportedly $33B of his own money. Since
that time, it appears this investment has not worked out. If Elon has instead bought $44B of US Treasury Bonds, how much
would his investment be worth in 10-year and 20-year bonds? Assume the 10-year bonds pay 3.96%,
the 20-year bonds pay 4.32%, with each compounding annually.
"""
from ftplib import print_line

### all your code below ###

# Initial Amount
P = 33000000000
#Interest Rates
ten_year_rate = 3.96 / 100
twenty_year_rate = 4.32 / 100
#Number of Years
n_ten = 10.0
n_twenty = 20.0

#calculations

ten_year_growth = P*((1+ten_year_rate)**n_ten)

twenty_year_growth = P*((1+twenty_year_rate)**n_twenty)

# final answer for 10-year
ten_year_final = ten_year_growth

# final answer for 20-year
twenty_year_final = twenty_year_growth

print('')
print('With 10 Year Bond: ')
print('Investment  =  $', round(ten_year_final, 2), ' =  $', round(ten_year_final / 1000000000, 2), 'Billion')
print('Profit  =  $', round(ten_year_final - P, 2), ' =  $', round((ten_year_final - P) / 1000000000, 2), 'Billion')
print('')
print('With 20 Year Bond:')
print('Investment  =  $', round(twenty_year_final, 2), ' =  $' , round(twenty_year_final / 1000000000, 2), 'Billion')
print('Profit  =  $', round(twenty_year_final - P, 2), ' =  $' , round((twenty_year_final - P ) / 1000000000 , 2), 'Billion')


