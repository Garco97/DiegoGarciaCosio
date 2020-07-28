import pandas as pd 
import numpy as np
from values import *
from numpy_financial import pmt, ipmt, ppmt, npv, irr
from industrial_process import Capital_factors
class Equipment:
    def __init__(self, fm=1):
        self.fm = fm
        self.capital_factors = Capital_factors
        self.C = 0.0
        
    def william(self):
        self.C *= ((1+Capital_factors.loc["fp"]["Fluids"])*self.fm+(Capital_factors.loc["fer"]["Fluids"] + Capital_factors.loc["fel"]["Fluids"]
                                                            + Capital_factors.loc["fi"]["Fluids"] + Capital_factors.loc["fc"]["Fluids"]
                                                            + Capital_factors.loc["fs"]["Fluids"] + Capital_factors.loc["fl"]["Fluids"]))
    
class Boiler(Equipment):
    def __init__(self,Q, p, fm=1, installed=True ):
        Equipment.__init__(self, fm)
        self.Q = Q
        self.p = p
        self.installed = installed

    def calculate_costs(self):
        """Return boiler cost. Inputs:
        Vapor production (kg/h): 5000 < Q < 800000
        Pressure (bar): 			   10 < p < 70
        fm = material factor"""

        assert type(self.installed) == bool

        if self.Q < 5000 or self.Q > 800000:
            print(f"    - WARNING: boiler vapor production out of method bounds, 5000 < self.Q < 800000. Results may not be accurate.")

        if self.p < 10 or self.p > 70:
            print(f"    - WARNING: boiler pressure out of method bounds, 10 < self.p < 70. Results may not be accurate.")

        if self.Q < 20000:
            self.C = 106000 + 8.7*self.Q
        elif self.Q < 200000:
            if self.p < 15:
                self.C = 110000 + 4.5*self.Q**0.9
            elif self.p < 40:
                self.C = 106000 + 8.7*self.Q
            else:
                self.C = 110000 + 4.5*self.Q**0.9
        else:
            self.C = 110000 + 4.5*self.Q**0.9

        if self.installed:
            self.william()       

class Turbine(Equipment):
    def __init__(self, kW, fm=1, installed=True):
        Equipment.__init__(self, fm)
        self.kW = kW    
        self.installed = installed

       
    def calculate_costs(self):
        """Return steam turbine cost for a power between 100 and 20000 kW. Inputs:
        fm = material factor"""

        assert type(self.installed) == bool
        
        if self.kW < 100 or self.kW > 20000:
            print(f"    - WARNING: steam turbine power out of method bounds, 100 < self.kW < 20000. Results may not be accurate.")
        
        self.C = -12000 + 1630*self.kW**0.75

        if self.installed:
            self.william()
            
class Pump(Equipment):
    def __init__(self,Q, fm=1, installed=True ):
        Equipment.__init__(self, fm)
        self.Q = Q
        self.installed = installed

       
    def calculate_costs(self):
        """Return centrifuge pump cost for a caudal between 0.2 and 126 L/s. Inputs:
        phase = 'Fluids', 'Fluids - Solids' or 'Solids'
        fm = material factor"""

        assert type(self.installed) == bool

        if self.Q < 0.2 or self.Q > 126:
            print(f"    - WARNING: pump caudal out of method bounds, 0.2 < self.Q (L/s) < 126. Results may not be accurate.")
        
        self.C = 6900 + 206*self.Q**0.9

        if self.installed:
            self.william()       

class Condenser(Equipment):
    def __init__(self, fm=1):
        Equipment.__init__(self, fm)
        self.C = 400000 * (10000 / 15000)**n_will
