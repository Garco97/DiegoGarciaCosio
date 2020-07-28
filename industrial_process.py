from values import *
import pandas as pd 
import numpy as np
from equipment import *
import seaborn as sb
import matplotlib.pyplot as plt 

from numpy_financial import pmt, ipmt, ppmt, npv, irr

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

class IndustrialProcess:
    def __init__(self):
        self.boiler = Boiler(kgH_boiler, pressure_boiler)
        self.turbine = Turbine(value_turbine)
        self.pump = Pump(ls_pump)
        self.condenser = Condenser()
        self.boiler.calculate_costs()
        self.turbine.calculate_costs()
        self.pump.calculate_costs()
        self.calculate_capex()
        self.loan = Loan(self.capex*value_loan, interest_loan, years_loan)
        self.loan.calculate_loan()
        self.depreciation = Depreciation(value_depr,self.capex)
        self.depreciation.calculate_depreciation()
        self.df = self.calculate_financial_model()
        
    
    def calculate_capex(self):
        self.capex =  self.boiler.C + self.turbine.C + self.condenser.C + self.pump.C 
    
    def export_to_csv(self):
        self.df.to_csv("data.csv")

    def calculate_financial_model(self):
        
        investment    = np.array([-self.capex*0.4] + [0 for i in range(years-1)])
        depreciation  = np.hstack(([0], self.depreciation.depr_array, [0 for i in range(years-1-len(self.depreciation.depr_array))]))
        loan_prin     = np.hstack(([0], self.loan.res_principal, [0 for i in range(years-1-len(self.loan.res_principal))]))
        loan_int      = np.hstack(([0], self.loan.res_interest, [0 for i in range(years-1-len(self.loan.res_interest))]))

        sales_array    = np.zeros(years)
        water_array    = np.zeros(years)
        salaries_array = np.zeros(years)   

        for i in range(years):
            if i == 0:
                sales_array[i]    = 0
                water_array[i]    = 0
                salaries_array[i] = 0
            elif i == 1:
                sales_array[i]    = sales
                water_array[i]    = -1*water
                salaries_array[i] = -1*salaries
            else:
                sales_array[i]    = sales_array[i-1]*1.03
                water_array[i]    = water_array[i-1]*1.03
                salaries_array[i] = salaries_array[i-1]*1.02

        ebt   = np.vstack((investment, depreciation, loan_int, sales_array, water_array, salaries_array)).sum(axis=0)
        taxes = ebt * -percentage_ebt
        for i in range(len(taxes)):
            if taxes[i] > 0:
                taxes[i] = 0
        eat = ebt - taxes
        cash_flow = eat - depreciation + loan_prin
        cumulative_cash_flow = np.cumsum(cash_flow)

        data = np.vstack((investment, sales_array, depreciation, loan_prin, loan_int, salaries_array, water_array, ebt, 
                        taxes, eat, cash_flow, cumulative_cash_flow))
        df   = pd.DataFrame(data,
                            index=['Investment', 'Sales', 'Depreciation', 'Loan principal', 'Loan interest', 'Salaries',
                                'Water', 'EBT', 'Taxes', 'EAT', 'Cash Flow', 'Cumulative Cash Flow'],
                            columns=[i for i in range(years)])

        
        # Calculating financial metrics

        npv_value = npv(discount_rate, cash_flow)
        irr_value = irr(cash_flow)

        # Printing results
        print(df)
        
        print(f"The project has a net present value of {'{:,.2f}'.format(npv_value)}€ and an internal rate of return of {round(irr_value*100, 2)}%")
        
        return df
    
    def plot_data(self):
        df_plot = self.df.transpose()
        df_plot = df_plot[['Sales', 'Salaries','Water', 'Cash Flow' , 'Cumulative Cash Flow']]

        plt.style.use('seaborn-whitegrid')


        df_plot[['Sales','Salaries','Water','Cash Flow']].plot(kind='bar')
        df_plot['Cumulative Cash Flow'].plot(secondary_y=False) 
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        
        plt.xticks(np.arange(min(self.df.columns), max(self.df.columns)+1, 1.0))

        plt.show()

class Loan:
    def __init__(self, quantity, interest, years):
        assert quantity > 0
        assert interest >= 0 and interest <= 1
        assert years > 1
        self.quantity = quantity
        self.interest = interest
        self.years = years
        self.res_payment = 0
        self.res_interest = 0
        self.res_principal = 0

    def calculate_loan(self):
        """Compute annual payment of a loan. Inputs:
        quantity [monetary units] == investment which will be funded
        interest [as fraction of unity] == annual interest
        years == number of yeras to return the loan."""

        assert type(self) is Loan

        self.res_payment   = pmt(self.interest, self.years, self.quantity)
        self.res_interest  = ipmt(self.interest, np.arange(self.years) + 1, self.years, self.quantity)
        self.res_principal = ppmt(self.interest, np.arange(self.years) + 1, self.years, self.quantity)

class Depreciation:
    def __init__(self, annual_percent, capex, residual_value=0):
        self.annual_percent = annual_percent   
        self.capex = capex 
        self.residual_value = residual_value 
        self.depr_array = self.calculate_depreciation()

    def calculate_depreciation(self):
        """Compute annual depreciation of investment. Inputs:
        annual_percent [as fraction of unity] == annual percent of depreciation.
        capex [monetary units] == capital expenditure
        residual_value[monetary units] == plant value at the end of its life."""

        assert self.annual_percent >= 0 and self.annual_percent <= 1

        annual_depreciation = []
        prev = 1

        while True:
            if prev < self.annual_percent:
                annual_depreciation.append(prev)
                break
            annual_depreciation.append(self.annual_percent)
            prev = prev - self.annual_percent

        depr_array = -1 * np.array(annual_depreciation) * (self.capex - self.residual_value)

        return depr_array
    
if __name__ == "__main__":
    industrial = IndustrialProcess()
    industrial.plot_data()
    industrial.export_to_csv()
