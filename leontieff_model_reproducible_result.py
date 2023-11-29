#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Model for assessing the expected size of demand and 
    supply shocks hitting a random sector in a random country. 
    The Leontief matrices in the model are constructed from OECD 2018 world 
    input-output tables.
    
    The Leontief_Model.shock() method exposes some parameters for the 
    experiment.
    
Name: Md Mohidul Haque
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

""" Class for holding, preparing, and assessing a Leonfief model from world
    inpit-output data."""
class Leontief_Model():
    def __init__(self):
        """
        Constructor method.
        Generates Leontief matrices from world input-output table for 2018 
        (most recent one available). It assumes the data to be in the current
        working directory under the file name ICIO2021_2018.csv.
        Data can be downloaded from the OECD website:
            https://www.oecd.org/sti/ind/inter-country-input-output-tables.htm
            http://stats.oecd.org/wbos/fileview2.aspx?IDFile=59a3d7f2-3f23-40d5-95ca-48da84c0f861
        
        Returns
        -------
        None.

        """
        """ Read data"""
        self.df = pd.read_csv("ICIO2021_2018.csv")
    
        """ Acertain that table is correct"""
        assert (self.df.iloc[0:3195,0] == self.df.columns[1:3196]).all()
    
        """ Extract Input-Output-Tables from rows 0-3194, columns 1-3195"""
        self.io_table =  self.df.iloc[0:3195,1:3196]
        self.io_table.index = list(self.df.iloc[0:3195,0])
        self.io_matrix = np.asarray(self.io_table)

        """ Extract final demand from rows 0-3195, columns 3195-3597"""
        self.demand = self.df.iloc[0:3195,3196:3598].sum(axis=1, numeric_only=True)

        """ Extract output from rows 0-3195, column 3598"""
        self.output = self.df.iloc[0:3195,3598]

        """ Compute production utilization coefficient matrix A"""
        self.A = np.divide(self.io_matrix, np.asarray(self.output)) 
        self.A[np.isnan(self.A)] = 0

        """ Output identity 
                np.dot(self.A, self.output) + self.demand == self.output
            holds only approximately because of rounding errors etc.
        """
        
        """ Compute Leontief inverse and inverse Leontief inverse"""
        self.I_minus_A = np.identity(3195) - self.A
        self.leontief_inverse = np.linalg.inv(self.I_minus_A)
        
        """ Output identity
                np.dot(self.leontief_inverse, self.demand)
            holds only approximately because of rounding errors etc.
            Prive level estimation can be dome like so:
                costs_plus_markup = np.ones(3195)
                self.price_levels = np.dot(costs_plus_markup, self.leontief_inverse)
        """

        """ Compute total output and total final demand for comparison for computing shock size"""
        self.total_output = np.sum(self.output)
        self.total_final_demand = np.sum(self.demand)


    def shock(self, 
              shock_type="Demand",
              shock_size=0.3,
              sample_size=300):
        """
        Method for assessing the direct and indirect effect of random supply 
        and demand shocks (hitting random sectors in random countries) on the 
        world economy.

        Parameters
        ----------
        shock_type : str, optional
            Type of shock, either "Demand" or "Supply". The default is "Demand".
        shock_size : float, optional
            Share by which supply or demand is decreased. The default is 0.3.
        sample_size : int, optional
            Number of random country-sectors to be sampled to assess the 
            expected effect of a random shock on the world economy. The 
            default is 300.

        Returns
        -------
        result_dict : dict
            Raw data and statistical measures on the expected shock effect.
            Contains:
                - Shock_effect_data: Raw data
                - Average
                - Standard_deviation
                - Median
                - Upper_5%_quantile
                - Upper_1%_quantile
        """
        
        """ Parse type of shock, select appropriate data for computation"""
        if shock_type == "Demand":
            matrix = self.leontief_inverse
            vector = self.demand
            benchmark = self.total_output
        elif shock_type == "Supply":
            matrix = self.I_minus_A
            vector = self.output
            benchmark = self.total_final_demand
        else:
            assert False, "Unknown shock type {:s}".format(shock_type)

        """ Shock experiment select <sample_size> sectors randomly, run 
            experiment for each: Decrease final_demand/output in sector  
            by factor <shock_size>, record result"""
        shock_effects = []
        sectors = np.random.choice(np.arange(3195), replace=False, size=sample_size)
        for sec in sectors:
            mod_vector = vector.copy()
            mod_vector[sec] = mod_vector[sec] * (1 - shock_size)
            result = np.dot(matrix, mod_vector)
            effect = 1 - np.sum(result) / benchmark
            shock_effects.append(effect)
        
        """ Compute statistics in sample"""
        result_dict = {"Shock_effect_data": shock_effects, 
                       "Average": np.mean(shock_effects), 
                       "Standard_deviation":  np.std(shock_effects), 
                       "Median": np.quantile(shock_effects, 0.5),
                       "Upper_5%_quantile":  np.quantile(shock_effects, 0.95), 
                       "Upper_1%_quantile":  np.quantile(shock_effects, 0.99)}
        
        return result_dict


"""class for the reproducible result"""
class ReproducibleResult():
    def __init__(self, number_of_replications = 20):
        """
        Constructor method.
        Run the model (Leontief_Model) by different  demand shocks for the upper 1% quantile and analyze the results.
        Here we used three demand shocks: 30%, 70%, and 100%.
        
        Patameters
        ----------
        number_of_replications : int
            How many replications we are using for each demand shocks to get a reproducible effect.
            Default value 20.
        
        
        Returns
        -------
        None.

        """
        
        self.number_of_replications = number_of_replications
        self.shock_sizes = [0.3, 0.7, 1.0] #different demand shocks
        self.return_result = {"for_30%_shock_size": [],
                              "for_70%_shock_size": [],
                              "for_100%_shock_size":[]}
        
    def run(self):
        """
        Method for using different demand shocks in the class Leontief_Model, and collect results.
        
        Parameters
        ----------
        None
        
        Return
        ------
        return_result : dict
            effect of different demand shock sizes for each number of replications 
        
        """
        for shock_size in self.shock_sizes:
            for replication in range(self.number_of_replications):
                L = Leontief_Model()
                demand_shock_effects = L.shock(shock_size = shock_size)
                if shock_size == self.shock_sizes[0]:
                    self.return_result["for_30%_shock_size"].append(demand_shock_effects["Upper_1%_quantile"])
                elif shock_size == self.shock_sizes[1]:
                    self.return_result["for_70%_shock_size"].append(demand_shock_effects["Upper_1%_quantile"])
                else:
                    self.return_result["for_100%_shock_size"].append(demand_shock_effects["Upper_1%_quantile"])
        return self.return_result
    
    def analyze_result(self, show_plot = False):
        
        """
        Method for analyze the effect of different demand shocks for the upper 1% quantile.
        
        parameters
        ----------
        show_plot : bool
            optional, default value false.
        
        """
        print("Effect of demand shocks by 30%  for the upper 1% quantile = ", np.mean(self.return_result["for_30%_shock_size"]), "+/-", np.std(self.return_result["for_30%_shock_size"]))
        print("\nEffect of demand shocks by 70%  for the upper 1% quantile = ", np.mean(self.return_result["for_70%_shock_size"]), "+/-", np.std(self.return_result["for_70%_shock_size"]))        
        print("\nEffect of demand shocks by 100%  for the upper 1% quantile = ", np.mean(self.return_result["for_100%_shock_size"]), "+/-", np.std(self.return_result["for_100%_shock_size"]))
        
        if show_plot:
            fig, ax = plt.subplots(nrows = 1, ncols = 1, squeeze = False)
            ax[0,0].hist(self.return_result["for_30%_shock_size"], bins = 15, rwidth = 0.85, label = "30% shock size")
            ax[0,0].hist(self.return_result["for_70%_shock_size"], bins = 15, rwidth = 0.85, label = "70% shock size")
            ax[0,0].hist(self.return_result["for_100%_shock_size"], bins = 15, rwidth = 0.85, label = "100% shock size")
            ax[0,0].set_title("Effect of different shock_sizes on upper 1% quantile")
            ax[0,0].set_xlabel("Effect of different shock size")
            ax[0,0].set_ylabel("Frequency")
            ax[0][0].legend()
            plt.tight_layout()
            plt.savefig("Effect of different shock_sizes on upper 1% quantile.png", dpi=300)
            plt.show()

"""main entry point"""
if __name__ == '__main__':
    test = ReproducibleResult()
    test.run()
    test.analyze_result(show_plot=True)