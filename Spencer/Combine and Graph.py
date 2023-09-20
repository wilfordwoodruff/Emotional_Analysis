#%%
import pandas as pd
import altair as alt
import string as str
import numpy as np
import matplotlib.pyplot as plt
all=pd.read_csv('DateTextScores.csv')
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