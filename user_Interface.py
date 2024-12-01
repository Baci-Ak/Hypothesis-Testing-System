from Hypothesis_testing_system import Hypothesis

def hypothesis_System_interface(data, alpha, test_type=None, items=None):
    tester = Hypothesis(data)
    results = {}
    try:
        # Ensure test_type is provided
        if not test_type or test_type not in ['one-tailed', 'two-tailed']:
            results['error'] = "Invalid test type. Please select 'one-tailed' or 'two-tailed'."
            return results

        # Validate alpha value
        try:
            alpha = float(alpha)
            if alpha <= 0 or alpha >= 1:
                results['error'] = "Alpha must be a decimal between 0 and 1 (e.g., 0.05)."
                return results
        except ValueError:
            results['error'] = "Invalid alpha value. Please provide a valid number (e.g., 0.05)."
            return results

        # One-tailed test
        if test_type == 'one-tailed':
            if not items or len(items.strip()) == 0:
                results['error'] = "Please provide a valid column name for the one-tailed test."
                return results
            
            item = items.strip()
            if item not in data.columns:
                results['error'] = f"Column '{item}' does not exist in the uploaded dataset. Available columns: {', '.join(data.columns)}"
                return results

            # Perform the one-tailed test
            result, t_stat, pvalue, mean_difference, correlation = tester.one_tailed_test(item, alpha)
            if isinstance(result, str) and result.startswith("Error"):
                results['error'] = result
            else:
                results['result'] = result
                results['t_stat'] = f"T-statistic: {t_stat:.4f}" if t_stat is not None else ""
                results['pvalue'] = f"P-value: {pvalue:.9f}" if pvalue is not None else ""

        # Two-tailed test
        elif test_type == 'two-tailed':
            if not items or len(items.strip()) == 0:
                results['error'] = "Please provide two valid column names for the two-tailed test, separated by a comma."
                return results

            items = [i.strip() for i in items.split(',')]
            if len(items) != 2:
                results['error'] = "Two valid column names are required for the two-tailed test."
                return results

            item1, item2 = items
            missing_cols = [col for col in [item1, item2] if col not in data.columns]
            if missing_cols:
                results['error'] = f"The following column(s) do not exist in the uploaded dataset: {', '.join(missing_cols)}. Available columns: {', '.join(data.columns)}"
                return results

            # Perform the two-tailed test
            result, t_stat, pvalue, mean_difference, correlation = tester.two_tailed_test(item1, item2, alpha)
            if isinstance(result, str) and result.startswith("Error"):
                results['error'] = result
            else:
                results['result'] = result
                results['t_stat'] = f"T-statistic: {t_stat:.4f}" if t_stat is not None else ""
                results['pvalue'] = f"P-value: {pvalue:.9f}" if pvalue is not None else ""
                results['mean_difference'] = f"Mean Difference: {mean_difference:.4f}" if mean_difference is not None else ""
                results['correlation'] = f"Correlation: {correlation:.4f}" if correlation is not None else ""

    except Exception as e:
        results['error'] = f"An unexpected error occurred: {e}"

    return results

