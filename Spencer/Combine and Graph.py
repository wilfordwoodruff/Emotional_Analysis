#%%
import pandas as pd
import altair as alt
import string as str
import numpy as np
import matplotlib.pyplot as plt

all=pd.read_csv('RawTextScores.csv')
all_s = all[pd.notna(all['First Date'])].sample(n=500).sort_values('First Date')

#%%
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

plt.plot(all_s['First Date'], all_s['avgLexValsurprise'], color='blue', marker='o', linestyle='-')
plt.plot(all_s['First Date'], all_s['avgLexValpositive'], color='red', marker='o', linestyle='-')
plt.title('Timeline of Anger & Joy')
plt.xlabel('First Date')
plt.ylabel('Scores')
plt.grid(True)

# Show the plot
plt.show()


# %%
#pendulum 

#%%
#Connect back to full text
df = pd.read_csv("../derived_data.csv")

uuids = ['49e2ab1c-4e61-4a90-b109-4c216e9fd7a4',
'683a68cc-fda4-43ca-a6cb-360fff93ddc8',
'7685247d-8215-474a-b75b-174c146558f3',
'bfac4c8c-b683-476d-9692-20987d1bf12e',
'a7eef15d-e36b-4653-98ff-296ec93ea2aa',
'fb4934b2-7830-41f9-b070-31126ebc5134',
'd7edb0ef-4712-40e5-ad0c-8a1442236363',
'6f45867c-6f95-4ad9-85aa-d19862fd783e',
'de3368c0-8ad2-498a-891a-987d3cbf3785',
'093763d7-fd65-417d-8993-99e97d74e2a1',
'dbc5a49a-539c-41a8-82fd-7ad957fe42aa']
filtered_df = df[df['UUID'].isin(uuids)].filter(['Text Only Transcript','UUID'])

my10 = pd.merge(filtered_df, all,how='left',on='Text Only Transcript')
top_columns = my10.set_index('UUID').drop(columns=['Text Only Transcript','First Date']).apply(lambda row: row.nlargest(5).index.tolist(), axis=1)

# %%
# new df from the column of lists
split_df = pd.DataFrame(top_columns.tolist(), columns=['Score1', 'Score2','Score3','Score4','Score5'])
# concat df and split_df
top5ScoresPer = pd.concat([my10, split_df], axis=1)
# display df
top5ScoresPer

# %%
