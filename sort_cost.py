import pandas as pd

# Load the CSV file
df = pd.read_csv('costs.csv')

# Extract the second row (actual cost data, excluding the 'Service' column)
costs = df.iloc[1, 1:].astype(float)

# Filter for values greater than $10 and drop 'Total costs($)'
filtered_costs = costs[costs > 10].drop(labels='Total costs($)', errors='ignore')

# Sort the result in descending order
sorted_costs = filtered_costs.sort_values(ascending=False)

# Display the result
with open('filtered_costs_over_10.txt', 'w') as f:
    f.write(sorted_costs.to_string())

print("Filtered costs have been saved to 'filtered_costs_over_10.txt'")