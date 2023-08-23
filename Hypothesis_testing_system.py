#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[9]:


# loading the datasest

#df = pd.read_sas("bs04retail.sas7bdat")
#df


# In[10]:


#df.dtypes


# In[ ]:





# In[11]:


#df['Store'] = df['Store'].astype(int)
#df.head()


# In[12]:


#df.isnull()


# In[ ]:





# # Building the Hypothesis Testing system

# In[ ]:





# In[6]:


import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, ttest_1samp

#Initialize the Hypothesis class
class Hypothesis:
    def __init__(self, df):
        self.df = df
        
        # one tail test method
    def one_tailed_test(self, item, alpha=0.05):
        try:
            df_item = np.array(self.df[item])
            mean_difference = None
            correlation = None
            t_stat, pvalue = ttest_1samp(df_item, alpha)
            
            if pvalue <= alpha and t_stat > 0:
                result = f"\n since p_value = {pvalue:.9f} <= {alpha} and {t_stat:.4f} > 0, we Reject the null hypothesis. There is a significant positive difference in {item}."
                
            else:
                result = f"\n since p_value = {pvalue:.9f} > {alpha}, there's no sufficient evidence to reject the null hypothesis H0. There is no significant difference in {item}."
                

            return result, t_stat, pvalue, mean_difference, correlation

        except KeyError as e:
            return f"Error: The item {e} not found in the DataFrame. Please enter a valid item name."

        except Exception as e:
            return f"Error: An unexpected error occurred. Details: {str(e)}"
        
        # two tail test method
    def two_tailed_test(self, item1, item2, alpha=0.05):
        try:
            df_item1 = np.array(self.df[item1])
            df_item2 = np.array(self.df[item2])
            
            t_stat, pvalue = ttest_ind(df_item1, df_item2, equal_var=False)  # Using Welch's t-test
            mean_difference = df_item1.mean() - df_item2.mean()
            correlation = np.corrcoef(df_item1, df_item2)[0, 1]
            
            
            if pvalue <= alpha:
                result = f"\nsince p_value = {pvalue:.4f} <= {alpha}, we Reject the null hypothesis. There is a significant difference between {item1} and {item2}."
                
            else:
                result = f"\nsince p_value = {pvalue:.4f} > {alpha}, we cannot reject the null hypothesis H0. There is no significant difference between {item1} and {item2}. hence, the data does not provide enough evidence to support the claim that there is a significant difference between the two items"
                

            return result, t_stat, pvalue, mean_difference, correlation

        except KeyError as e:
            return f"Error: One or both items {e} not found in the DataFrame. Please enter valid item names."
        

        except Exception as e:
            return f"Error: An unexpected error occurred. Details: {str(e)}"
        
        except:
            print("Some other exception happened.")

        
        
      



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




