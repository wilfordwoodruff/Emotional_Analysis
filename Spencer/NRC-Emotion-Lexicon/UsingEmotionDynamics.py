#%%
import csv

# Specify the input and output file paths
input_file = 'NRC-Emotion-Lexicon/OneFilePerEmotion/trust-NRC-Emotion-Lexicon.txt'
output_file = 'trust_NRC.csv'

# Open the input and output files
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    # Create a CSV writer
    csv_writer = csv.writer(outfile)
    
    # Loop through each line in the input file
    for line in infile:
        # Split the line using tab as the delimiter
        parts = line.strip().split('\t')
        
        # Write the parts to the CSV file
        csv_writer.writerow(parts)

print(f'Conversion from {input_file} to {output_file} completed successfully.')

# %%
from tqdm import tqdm
# %%
joy = pd.read_csv('joy_NRC.csv').set_index('word')
anticipation = pd.read_csv('anticipation_NRC.csv').set_index('word')
anger = pd.read_csv('anger_NRC.csv').set_index('word')
fear = pd.read_csv('fear_NRC.csv').set_index('word')
disgust = pd.read_csv('disgust_NRC.csv').set_index('word')
positive = pd.read_csv('positive_NRC.csv').set_index('word')
sadness = pd.read_csv('sadness_NRC.csv').set_index('word')
trust = pd.read_csv('trust_NRC.csv').set_index('word')
surprise = pd.read_csv('surprise_NRC.csv').set_index('word')
negative = pd.read_csv('negative_NRC.csv').set_index('word')
combined = (joy.merge(anticipation,on='word', how='outer')
            .merge(anger,on='word', how='outer')
            .merge(fear,on='word', how='outer')
            .merge(disgust,on='word', how='outer')
            .merge(sadness,on='word', how='outer')
            .merge(positive,on='word', how='outer')
            .merge(negative,on='word', how='outer')
            .merge(surprise,on='word', how='outer')
            .merge(trust,on='word', how='outer'))
combined.to_csv('all_emotions.csv')

#%%
#Join the 10 scores back to the text
all = df[['First Date','Text Only Transcript']]
words = ['anger','anticipation','disgust','fear','joy','negative','positive','sadness','surprise','trust']
for word in words:
    file_path = f'NRC-Emotion-Lexicon/{word}.csv'
    file = pd.read_csv(file_path)
    file.columns = ["Index","speaker","text","numTokens","numLexTokens","avgLexVal"+word,"lexRatio"]
    all = pd.concat([all, file["avgLexVal"+word]],axis=1)
all.to_csv('DateTextScores.csv',index=False)