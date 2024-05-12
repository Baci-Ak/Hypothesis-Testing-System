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
                result = f"\nT-statistic = {t_stat:.3f}: The observed difference in {item} is {t_stat:.3f} standard errors away from what would be expected by chance alone.\n" \
                         f"(P-value) = {pvalue:.2f}: The p-value of {pvalue:.2f} suggests that there is only a {pvalue*100:.2f}% probability of obtaining a difference in {item} as extreme as the one observed if there were no real difference between {item} and the general population of the data.\n" \
                         f"Conclusion: Since the p-value ({pvalue*100:.2f}%) is less than or equal to the chosen significance level {alpha}({alpha*100:.0f}%) and ({t_stat:.3f}) > 0, we reject the null hypothesis H0. Therefore, we conclude that {item} values are significantly higher than the general population.\n"
    
            else:
                result = f"\nT-statistic = {t_stat:.3f}: The observed difference in {item} is {t_stat:.3f} standard errors away from what would be expected by chance alone.\n" \
                         f"P-value = {pvalue:.2f}: The p-value of {pvalue:.2f} suggests that there is only a {pvalue*100:.2f}% probability of obtaining a difference in {item} as extreme as the one observed if there were no real difference between {item} and the general population of the data.\n" \
                         f"Conclusion: Since the p-value ({pvalue*100:.2f}%) > {alpha}({alpha*100:.0f}%), there's no sufficient evidence to reject the null hypothesis H0. There is no significant difference in {item} values compared to the general population."
                
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
                result = f"\nT-Statistic = {t_stat:.3f}: The observed difference in {item1} and {item2} is {t_stat:.3f} standard errors away from what would be expected by chance alone.\n" \
                         f"P-value = {pvalue:.2f}: the p-value of {pvalue:.2f} suggests that there is only a {pvalue*100:.2f}% probability of obtaining a difference in items as extreme as the one observed if there were no real difference between {item1} and {item2}.\n" \
                         f"\nConclusion: Since the p-value ({pvalue*100:.2f}%) <= {alpha}({alpha*100:.0f}%), we Reject the null hypothesis H0. There is a significant difference between {item1} and {item2}.\n"
            else:
                result = f"\nT-Statistic = {t_stat:.3f}: The observed difference in {item1} and {item2} is {t_stat:.4f} standard errors away from what would be expected by chance alone.\n" \
                         f"\nP-value = {pvalue:.2f}: the p-value of {pvalue:.2f} suggests that there is only a {pvalue*100:.2f}% probability of obtaining a difference in items as extreme as the one observed if there were no real difference between {item1} and {item2}.\n" \
                         f"Conclusion: Since the p-value ({pvalue*100:.2f}%) is greater than the chosen significance level {alpha}({alpha*100:.0f}%), we cannot reject the null hypothesis H0. Therefore, we do not have sufficient evidence to conclude that there  is a significant difference in values between {item1} and {item2}. hence, the data does not provide enough evidence to support the claim that there is a significant difference between the two items.\n"
           
            mean_difference = np.mean(df_item1) - np.mean(df_item2)
            correlation = np.corrcoef(df_item1, df_item2)[0, 1]
            
            return result, t_stat, pvalue, mean_difference, correlation
            
        except KeyError as e:
            return f"Error: One or both items {e} not found in the DataFrame."
        except Exception as e:
            return f"Error: An unexpected error occurred. Details: {str(e)}."




        
        
    