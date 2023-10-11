#%%
import pandas as pd
FILE = 'Adjusted Scores for Testing.csv'

results = pd.read_csv(FILE)

# Initialize variables for grouping
current_group = 0
group_scores = []

# Create a new column 'Group' to identify groups based on 'Word' column
results['Entry'] = 0

# Iterate through the rows and assign groups
for index, row in results.iterrows():
    if row['Text'] == 'NEW_ENTRY':
        current_group += 1
    results.at[index, 'Entry'] = current_group

# Filter out rows with 'NEW_ENTRY' in 'Word' column
df = results[results['Text'] != 'NEW_ENTRY']

# Group by 'Group' and calculate the average score for each group
columns = df.columns[8:61]
result = df.groupby('Entry')[columns].mean().reset_index()

result.reset_index(drop=True, inplace=True)
print(result)

original = pd.read_csv('../../derived_data.csv')
original[columns] = result[columns]
original.to_csv('Full Data with Emotion Scores.csv')
# %%
