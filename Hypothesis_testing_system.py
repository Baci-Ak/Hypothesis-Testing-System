#!/usr/bin/env python
# coding: utf-8






import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, ttest_1samp


class Hypothesis:
    def __init__(self, df):
        self.df = df
        
    def one_tailed_test(self, item, alpha=0.05):
        try:
            df_item = np.array(self.df[item])
            t_stat, pvalue = ttest_1samp(df_item, alpha)
            
            if pvalue <= alpha and t_stat > 0:
                result = f"Since p-value = {pvalue:.9f} <= {alpha} and {t_stat:.4f} > 0, we Reject the null hypothesis H0. There is a significant positive difference in {item}."
            else:
                result = f"Since p-value = {pvalue:.9f} > {alpha}, there's no sufficient evidence to reject the null hypothesis H0. There is no significant difference in {item}."
                
            return result, t_stat, pvalue, None, None
            
        except KeyError as e:
            return f"Error: The item {e} not found in the DataFrame."
        except Exception as e:
            return f"Error: An unexpected error occurred. Details: {str(e)}"
        
    def two_tailed_test(self, item1, item2, alpha=0.05):
        try:
            df_item1 = np.array(self.df[item1])
            df_item2 = np.array(self.df[item2])
            
            t_stat, pvalue = ttest_ind(df_item1, df_item2, equal_var=False)  
            
            if pvalue <= alpha:
                result = f"Since p-value = {pvalue:.4f} <= {alpha}, we Reject the null hypothesis H0. There is a significant difference between {item1} and {item2}."
            else:
                result = f"Since p-value = {pvalue:.4f} > {alpha}, we cannot reject the null hypothesis H0. There is no significant difference between {item1} and {item2}. hence, the data does not provide enough evidence to support the claim that there is a significant difference between the two items."
                
            mean_difference = np.mean(df_item1) - np.mean(df_item2)
            correlation = np.corrcoef(df_item1, df_item2)[0, 1]
            
            return result, t_stat, pvalue, mean_difference, correlation
            
        except KeyError as e:
            return f"Error: One or both items {e} not found in the DataFrame."
        except Exception as e:
            return f"Error: An unexpected error occurred. Details: {str(e)}."




        
        
    