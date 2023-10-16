#%%
import pandas as pd
FILE = 'first10.csv'

results = pd.read_csv(FILE)

# Initialize variables for grouping
current_group = 0
group_scores = []

# Create a new column 'Group' to identify groups based on 'Word' column
results['Entry'] = 0

# Iterate through the rows and assign groups
for index, row in results.iterrows():
    if row['Text'] == 'END_ENTRY':
        current_group += 1
    results.at[index, 'Entry'] = current_group

# Filter out rows with 'NEW_ENTRY' in 'Word' column
df = results[results['Text'] != 'END_ENTRY']

# Group by 'Group' and calculate the average score for each group
columns = df.columns[8:61]
result = df.groupby('Entry')[columns].mean().reset_index()

result.reset_index(drop=True, inplace=True)
print(result)

original = pd.read_csv('../../derived_data.csv')
original[columns] = result[columns]
original.to_csv('first 6 with Emotion Scores.csv')
# %%
#Save Hume scores to WORDCLOUD format

all_words = df
cols = ['Id','EndPosition','BeginTime','EndTime','Confidence','SpeakerConfidence','1', '2',
       '3', '4', '5', '6', '7', '8', '9', 'toxic', 'severe_toxic', 'obscene',
       'threat', 'insult', 'identity_hate']

score_columns = df.drop(columns=cols,axis=1).columns[2:-1]  # Exclude the first two and the last column

def find_highest_score(row):
    max_column = row[score_columns].idxmax()
    max_score = row[score_columns].max()
    return pd.Series([max_column, max_score], index=['MaxColumn', 'MaxScore'])

# Apply the function to each row in the DataFrame
top_scores = df.apply(find_highest_score, axis=1)
top_scores[['Word','Entry']] = df[['Text','Entry']]

# %%
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

remove_words = [
    "i", 'I', "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", '&',
    'January','February','March','April','May','June','July','August','September','October',
    'November','December'
]

top_15 = top_scores[top_scores['Entry']==3].query('Word not in @remove_words').sort_values('MaxScore',ascending=False).head(n=15)
word_cloud_data = top_15[['Word', 'MaxScore', 'MaxColumn']].to_dict(orient='records')

# Initialize the WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white')
wordcloud.generate_from_frequencies(frequencies={item['Word']: item['MaxScore'] for item in word_cloud_data})

#Currently Unused, but makes colors?
unique_max_columns = top_15['MaxColumn'].unique()
color_map = {max_col: sns.color_palette("husl", n_colors=len(unique_max_columns))[i] for i, max_col in enumerate(unique_max_columns)}
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return color_map[top_15[top_15['Word'] == word]['MaxColumn'].values[0]]

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

'''
Needs break words (the, is, &, etc.)
'''