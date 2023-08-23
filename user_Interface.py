#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


from Hypothesis_testing_system import Hypothesis


# In[ ]:





# In[3]:


#import numpy as np

#i import pandas for data anlysis and manipulations
#import pandas as pd


# In[13]:


#df = pd.read_sas("bs04retail.sas7bdat")
#df.head()


# In[14]:


#df.dtypes


# In[15]:


#df['Store'] = df['Store'].astype(int)
#df.head()


# In[ ]:





# In[11]:


import pandas as pd


def hypothesis_System_interface(data):
    tester = Hypothesis(data)
    
    while True:
        try:
            print("\nAvailable items for testing are:", ", ".join(data.columns))
            
            print("\nAvailable test types are: one-tailed, two-tailed")
            test_type = input("\nWhat type of test do you want to perform? (Enter 'one-tailed', 'two-tailed', or 'quit'): ").lower()
            
            if test_type == 'quit' or test_type == 'q':
                print("Exiting the application. Goodbye!")
                break
            elif test_type == 'one-tailed':
                item = input("\nPlease enter the name of the item/product you want to test: ").strip()
                alpha = float(input("\nPlease enter the significance level for your test (alpha): "))
                result, t_stat, pvalue, mean_difference, correlation = tester.one_tailed_test(item, alpha)
            elif test_type == 'two-tailed':
                items = input("\nPlease enter the names of the items you want to test (comma-separated): ").split(',')
                alpha = float(input("\nEnter significance level (alpha): "))
                result, t_stat, pvalue, mean_difference, correlation = tester.two_tailed_test(items[0], items[1], alpha)
            else:
                result = "Error: Invalid test type. Please choose either 'one-tailed' or 'two-tailed'."
            
            print(result)
            
            if 'mean_difference' in locals() and 'correlation' in locals() and mean_difference is not None and correlation is not None:
                print(f"\nMean Difference between {items[0]} and {items[1]}: {mean_difference:.2f}")
                print(f"Correlation between {items[0]} and {items[1]}: {correlation:.3f}")
                if mean_difference > 0:
                    print(f"The data constitutes significant evidence that the underlying mean number was greater for {items[0]}, by an estimated value of {mean_difference:.3f}. The result suggests that {items[0]} should be preferred.")
                else:
                    print(f"The data constitutes significant evidence that the underlying mean number was greater for {items[1]}, by an estimated value of {abs(mean_difference):.3f}. The result suggests that {items[1]} should be preferred.")
            
            print(f"\nT-statistic: {t_stat:.4f}")
            print(f"P-value: {pvalue:.9f}")
            
            stat_table = pd.DataFrame(columns=['Item', 'N', 'Mean', 'Median', 'Std_Deviation', 'Variance', 'Min_Val', 'Max_Val'])
            for item in data.columns:
                sample_size = len(data[item])
                mean = round(data[item].mean(), 3)
                median = round(data[item].median(), 2)
                st_deviation = round(data[item].std(), 2)
                variance = round(data[item].var(), 2)
                mini_val = data[item].min()
                max_val = data[item].max()
                stat_table = pd.concat([stat_table, pd.DataFrame({
                    'Item': [item],
                    'N': [sample_size],
                    'Mean': [mean],
                    'Median': [median],
                    'Std_Deviation': [st_deviation],
                    'Variance': [variance],
                    'Min_Val': [mini_val],
                    'Max_Val': [max_val]
                })], ignore_index=True)
            
            print("\nStatistic Table:")
            print(stat_table)
            
            more_operations = input("\nDo you want to perform more operations? (Enter 'yes' to continue or 'no' to quit): ").lower()
            if more_operations != 'yes':
                print("Exiting the application. Goodbye!")
                break
            
        except IndexError:
            print("Error: Invalid item name or index error. Please enter the correct item/product names.")
        except UnboundLocalError:
            print("UnboundLocalError: Invalid test type. Please choose either 'one-tailed' or 'two-tailed'.")
        except ValueError:
            print("ValueError: Please enter a numeric value and not a character.")
        except Exception as e:
            print(f"An error occurred: {e}")

 


# In[ ]:





# In[ ]:





# In[16]:


#hypothesis_System_interface(df)


# In[ ]:




