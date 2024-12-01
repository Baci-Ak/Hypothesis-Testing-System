#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, ttest_1samp


class Hypothesis:
    def __init__(self, df):
        self.df = df

    def validate_column(self, column):
        """Validate that a column exists and contains numeric data."""
        if column not in self.df.columns:
            raise KeyError(f"The column '{column}' is not found in the dataset.")
        if not np.issubdtype(self.df[column].dtype, np.number):
            raise ValueError(f"The column '{column}' does not contain numeric data. Please select a numeric column.")

    def handle_missing_values(self, data, column_name):
        """Handle missing values by dropping them and logging the count."""
        missing_count = data.isnull().sum()
        if missing_count > 0:
            print(f"Column '{column_name}': {missing_count} missing values were dropped.")
        cleaned_data = data.dropna()
        if len(cleaned_data) < 2:
            raise ValueError(
                f"Column '{column_name}' has insufficient valid data after dropping missing values. "
                f"At least 2 valid values are required for hypothesis testing."
            )
        return cleaned_data

    def one_tailed_test(self, item, alpha=0.05):
        try:
            # Validate the column
            self.validate_column(item)

            # Handle missing values
            df_item = self.handle_missing_values(self.df[item], item).to_numpy()

            t_stat, pvalue = ttest_1samp(df_item, 0)

            if np.isnan(t_stat) or np.isnan(pvalue):
                raise ValueError(
                    f"Calculation resulted in NaN values for column '{item}'. "
                    f"This may happen if the column contains only zeros or insufficient variability."
                )

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
            return f"Error: The item '{item}' was not found in the DataFrame. Details: {e}", None, None, None, None
        except ValueError as e:
            return f"Error: {e}", None, None, None, None
        except Exception as e:
            return f"Error: An unexpected error occurred. Details: {str(e)}", None, None, None, None

    def two_tailed_test(self, item1, item2, alpha=0.05):
        try:
            # Validate both columns
            self.validate_column(item1)
            self.validate_column(item2)

            # Handle missing values
            df_item1 = self.handle_missing_values(self.df[item1], item1).to_numpy()
            df_item2 = self.handle_missing_values(self.df[item2], item2).to_numpy()

            t_stat, pvalue = ttest_ind(df_item1, df_item2, equal_var=False)

            if np.isnan(t_stat) or np.isnan(pvalue):
                raise ValueError(
                    f"Calculation resulted in NaN values for columns '{item1}' and '{item2}'. "
                    f"This may happen if the columns contain only zeros or insufficient variability."
                )

            mean_difference = np.mean(df_item1) - np.mean(df_item2)
            correlation = np.corrcoef(df_item1, df_item2)[0, 1]

            if pvalue <= alpha:
                result = f"\nT-Statistic = {t_stat:.3f}: The observed difference in {item1} and {item2} is {t_stat:.3f} standard errors away from what would be expected by chance alone.\n" \
                         f"P-value = {pvalue:.2f}: the p-value of {pvalue:.2f} suggests that there is only a {pvalue*100:.2f}% probability of obtaining a difference in items as extreme as the one observed if there were no real difference between {item1} and {item2}.\n" \
                         f"\nConclusion: Since the p-value ({pvalue*100:.2f}%) <= {alpha}({alpha*100:.0f}%), we Reject the null hypothesis H0. There is a significant difference between {item1} and {item2}.\n"
            else:
                result = f"\nT-Statistic = {t_stat:.3f}: The observed difference in {item1} and {item2} is {t_stat:.4f} standard errors away from what would be expected by chance alone.\n" \
                         f"\nP-value = {pvalue:.2f}: the p-value of {pvalue:.2f} suggests that there is only a {pvalue*100:.2f}% probability of obtaining a difference in items as extreme as the one observed if there were no real difference between {item1} and {item2}.\n" \
                         f"Conclusion: Since the p-value ({pvalue*100:.2f}%) is greater than the chosen significance level {alpha}({alpha*100:.0f}%), we cannot reject the null hypothesis H0. Therefore, we do not have sufficient evidence to conclude that there is a significant difference in values between {item1} and {item2}. Hence, the data does not provide enough evidence to support the claim that there is a significant difference between the two items.\n"

            return result, t_stat, pvalue, mean_difference, correlation

        except KeyError as e:
            return f"Error: One or both items {e} not found in the DataFrame.", None, None, None, None
        except ValueError as e:
            return f"Error: {e}", None, None, None, None
        except Exception as e:
            return f"Error: An unexpected error occurred. Details: {str(e)}.", None, None, None, None
