#%%
import pandas as pd

# Sample data (replace this with your actual Series)
large_series = pd.read_csv('../../derived_data.csv')['Text Only Transcript']  # Replace with your large Series
output_file = "full_transcript.txt"
chunk_size = 100  # Define the size of each chunk

# Determine the total number of chunks
total_chunks = len(large_series) // chunk_size + 1

for chunk_num in range(total_chunks):
    start_idx = chunk_num * chunk_size
    end_idx = start_idx + chunk_size

    # Extract the chunk
    chunk = large_series[start_idx:end_idx]
    with_ends = ''
    for i in range(chunk.head(n=1).index.start,chunk.tail(n=1).index.start):
        with_ends += str(chunk[i])
        with_ends += ' END_ENTRY '

    with open(output_file, "a", errors="ignore") as file:
        file.write(with_ends)


    # Process the chunk (for example, you can add and save the data)
    # Replace this with your processing and saving logic
    # For demonstration, we'll just print the chunk.
    print(f"Processing Chunk {chunk_num + 1}:\n{chunk}")

    # Save the processed chunk to a file, database, or any storage method you prefer
    # Replace this with your saving logic

# Continue processing or saving other chunks as needed

# %%
