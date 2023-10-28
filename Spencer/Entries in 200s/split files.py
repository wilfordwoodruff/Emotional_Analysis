#%%
import os
import pandas as pd
by_date = pd.read_csv("C:/Users/spenc/OneDrive/Documents/Practice Python/Dates/Third Try fixing tags.csv",encoding = "utf-8",encoding_errors='ignore')['text']
by_date = (by_date.str.replace("<.*>",repl='',regex=True)
           .str.replace("\[\[.*\|",repl='',regex=True)
           .str.replace(']','').str.replace('[','')
           .str.replace('\n',' ')
           .str.replace('\u25c7','')
           .str.replace('\u25ca','')
           .str.replace('\u2b26','')
           .str.replace('\u0151','')
           .str.replace('\u04d0','')
           .str.replace('\u014d','')
           .str.replace('\u25a0','')
)

# Function to split a file into multiple smaller files
def split_file(input_file, lines_per_file=200):
    
    total_lines = len(by_date)
    num_files = (total_lines + lines_per_file - 1) // lines_per_file
    
    for i in range(num_files):
        start = i * lines_per_file
        end_maybe = (i + 1) * lines_per_file
        if end_maybe < len(by_date):
            end = end_maybe
        else: 
            end = len(by_date)
        file_chunk = by_date.iloc[start:end].to_string()
        text = ''
        for row in range(start,end):
            text = text + by_date.iloc[row] + " ENDENTRY "
        
        # Create a new output file
        output_filename = f'output_file_{i+1}.txt'
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.writelines(text)

split_file(by_date)


# %%
