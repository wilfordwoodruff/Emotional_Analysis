import pandas as pd


with open("full_transcript.txt", 'r') as f:
    lines = f.read()

lines = lines.split("END_ENTRY")

lines = [line.replace('\n', ' ') for line in lines]

with open('output_file.txt', 'w') as file:
    for line in lines:
        file.write(line + 'ENDENTRY\n')
