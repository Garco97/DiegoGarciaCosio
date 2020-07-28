# Prueba desarrollador Python junior
## Classes
2 different files:

    - industrial_process.py: contains the classes IndustrialProcess, Loan, Depreciation:
        - IndustrialProcess: is the one that manages everything: from creating the other classes to calculate the financial model. 
        It contains the different equipement information and the loan and depreciation.
        It also has 4 different functions:
            - calculate_capex(): this is used to get all the calculations from the different equipment (boiler, turbine, pump, condenser)
            - calculate_financial_model()
            - export_to_csv()
            - plot_data()

        - Loan: this class calculates the loan and contains the different input arguments. It has one function:
            - calculate_loan()
        
        - Depreciation: thi class contains the input data and calculates the depreciation with its function:
            - calculate_depreciation()

    - equipment.py: contains the classes Equipment, Boiler, Turbine, Pump and Condenser:
        - Equipment: is the father class of the rest in order to inherit its attributes and functions, because some attributes are common for the equipment. It has one function:
            - william(): in order to calculate William's correlation.
        
        - Boiler, Turbine, Pump and Condenser: they contain their own attributes and their own calculate_costs() function.

## values.py
This file contains the different data used in the script. I made this file in order to have all the data together coming from a source, because I imagine that all the data would come from a form or a database.

## Explanation of my code
I made a lot of classes, because I imagine this implementation being mapped with a database or something like that. I also think it is cleaner in order to terms of scalability of the code.

## Optional tasks
I did the plotting task, it's the method plot_data() in the class IndustrialProcess, and also I did the export to excel one in the methos export_to_csv() (I used CSV, but other format could be use)