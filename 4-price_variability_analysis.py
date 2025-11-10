import pandas as pd

# Read the data from the 'return.xlsx' Excel file, assuming it's in 'Sheet1'
df = pd.read_excel('return.xlsx', sheet_name='Sheet1')

# Remove rows with 0 values in the 'Price Per Acre' column
df = df[df['Price Per Acre'] != 0]

# Define a function to remove outliers based on the highest and lowest 10% of price per acre
def remove_outliers_percentile(data):
    if len(data) >= 4:  # Skip outlier removal if less than 4 entries per title
        lower_limit = data['Price Per Acre'].quantile(0.1)
        upper_limit = data['Price Per Acre'].quantile(0.9)
        return (data['Price Per Acre'] >= lower_limit) & (data['Price Per Acre'] <= upper_limit)
    else:
        return pd.Series(True, index=data.index)  # Return True for all entries if less than 5

# Apply the function to filter out rows with outliers for each title
filtered_data = df.groupby('Title').apply(lambda x: x[remove_outliers_percentile(x)])

# Reset the index to avoid a MultiIndex in the resulting DataFrame
filtered_data.reset_index(drop=True, inplace=True)

# Calculate median, mean, and coefficient of variation for each title, rounded to the nearest decimal
summary_stats = (
    filtered_data.groupby('Title')['Price Per Acre']
    .agg(['median', 'mean'])
    .round()  # Round to the nearest whole number for median and mean
    .reset_index()
)

# Calculate the coefficient of variation for each title
cv_values = df.groupby('Title')['Price Per Acre'].apply(lambda x: (x.std() / x.mean()) * 100).reset_index()
cv_values.columns = ['Title', 'Coefficient of Variation']

# Calculate quartiles for categorization
lower_quartile, upper_quartile = cv_values['Coefficient of Variation'].quantile([0.46, 0.80])

# Categorize the coefficient of variation
def categorize_cv(cv):
    if cv < lower_quartile:
        return 'Yes'
    elif cv > upper_quartile:
        return 'No'
    else:
        return 'Somewhat'

# Add a new column for the CV category
cv_values['CV Category'] = cv_values['Coefficient of Variation'].apply(categorize_cv)

# Merge the coefficient of variation and its category back into the original DataFrame
filtered_data = pd.merge(filtered_data, summary_stats, on='Title', suffixes=('', '_summary'))
filtered_data = pd.merge(filtered_data, cv_values, on='Title')

# Print the DataFrame with rounded median, mean, and coefficient of variation columns
print(filtered_data)

# Save the filtered DataFrame with rounded summary stats, coefficient of variation, and its category to a new Excel file if needed
filtered_data.to_excel('filtered_data_summary_cv_category_rounded.xlsx', index=False)
