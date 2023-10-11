#%%
word_scores = {
    "python": .95,
    "programming": .80,
    "data": .70,
    "machine": .90,
    "learning": .85,
    "word": .60,
    "cloud": .75,
}
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color="white")
wordcloud.generate_from_frequencies(word_scores)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# %%
