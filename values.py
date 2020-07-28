import numpy as np
import pandas as pd 

#Boiler
kgH_boiler = 10000
pressure_boiler = 70

#Turbine
value_turbine = 1500
#Pump
ls_pump = 2.84
#Condenser


#Willliam
n_will = 0.8

# Loan 
value_loan = 0.6 
years_loan = 10 
interest_loan = 0.04

# Depreciation
value_depr = 0.07


#Costs
capacity_factor = 0.9

water_price = 1.29
water       = water_price * 10 * 8760 * capacity_factor
people = 4 
turns = 3 
salary = 30000
salaries    = people * turns * salary
# Calculating sales
elect_wh = 0.05
hours_year = 8760
sales = 1500 * elect_wh * hours_year * capacity_factor
#financial model
years = 20
percentage_ebt = 0.3
#  financial metrics
discount_rate = 0.053


#capital_factors
data_factors = np.array([[0.3, 0.5, 0.6],
                         [0.8, 0.6, 0.2],
                         [0.3, 0.3, 0.2],
                         [0.2, 0.2, 0.15],
                         [0.3, 0.3, 0.2],
                         [0.2, 0.2, 0.1],
                         [0.1, 0.1, 0.05],
                         [0.3, 0.4, 0.4],
                         [0.35, 0.25, 0.2],
                         [0.1, 0.1, 0.1]])

Capital_factors = pd.DataFrame(data_factors,
                               index=["fer", "fp", "fi", "fel", "fc", "fs", "fl", "OS", "D&E", "X"], 
                               columns=["Fluids", "Fluids-Solids", "Solids"])