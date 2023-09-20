#%%
import pandas as pd
words = pd.read_csv('Emotion_Survey.csv')['word']
text = pd.read_csv('RawTextScores.csv')['Text Only Transcript']

all_words = {}
for entry in text:
    entry = entry.split()
    for word in entry:
        if word not in all_words:
            all_words[word] = 1
        else:
            all_words[word] +=1


# %%
doc_words = (pd.DataFrame(all_words.items(), columns=['Word', 'Appearances'])
             .sort_values('Appearances',ascending=False)
             .query("Word not in @words")
).to_csv('words_missing.csv')
# %%
