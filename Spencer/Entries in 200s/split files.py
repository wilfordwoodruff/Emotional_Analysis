#%%
import os

# Function to split a file into multiple smaller files
def split_file(input_file, lines_per_file=200):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    total_lines = len(lines)
    num_files = (total_lines + lines_per_file - 1) // lines_per_file
    
    for i in range(num_files):
        start = i * lines_per_file
        end = (i + 1) * lines_per_file
        file_chunk = lines[start:end]
        
        # Create a new output file
        output_filename = f'output_file_{i+1}.txt'
        with open(output_filename, 'w') as output_file:
            output_file.writelines(file_chunk)

if __name__ == "__main__":
    input_file = '../AJ/output_file.txt'
    
    if os.path.exists(input_file):
        split_file(input_file)
        print("File split complete.")
    else:
        print(f"{input_file} not found.")
