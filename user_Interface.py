
from Hypothesis_testing_system import Hypothesis


def hypothesis_System_interface(data, alpha, test_type=None, items=None):
    tester = Hypothesis(data)
    results = {}
    try:
        print("\nAvailable items for testing are:", ", ".join(data.columns))
        print("\nAvailable test types are: one-tailed, two-tailed")
        
        # Check if test_type and items are provided and use them if available
        if test_type is None:
            test_type = input("\nWhat type of test do you want to perform? (Enter 'one-tailed', 'two-tailed', or 'quit'): ").lower()

        if test_type == 'quit' or test_type == 'q':
            results['error'] = "Exiting the application. Goodbye!"
            return results
        elif test_type == 'one-tailed':
            if items is None:
                item = input("\nPlease enter the name of the item/product you want to test: ").strip()
            else:
                item = items.strip()
            result, t_stat, pvalue, mean_difference, correlation = tester.one_tailed_test(item, alpha)
        elif test_type == 'two-tailed':
            if items is None:
                items = input("\nPlease enter the names of the items you want to test (comma-separated): ").split(',')
            else:
                items = [i.strip() for i in items.split(',')]
            item1, item2 = items[0], items[1]
            result, t_stat, pvalue, mean_difference, correlation = tester.two_tailed_test(item1, item2, alpha)
        else:
            result = "Error: Invalid test type. Please choose either 'one-tailed' or 'two-tailed'."
        
        results['result'] = result
        results['t_stat'] = f"T-statistic: {t_stat:.4f}" if t_stat is not None else ""
        results['pvalue'] = f"P-value: {pvalue:.9f}" if pvalue is not None else ""
        results['mean_difference'] = f"Mean Difference: {mean_difference:.4f}" if mean_difference is not None else ""
        results['correlation'] = f"Correlation: {correlation:.4f}" if correlation is not None else ""
        
    except KeyError as e:
        results['error'] = f"Error: One or both items {e} not found in the DataFrame."
    except Exception as e:
        results['error'] = f"An error occurred: {e}"
    
    return results




 
























