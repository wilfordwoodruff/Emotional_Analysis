#%%
# Define the input file and output file names
input_file = "full_transcript.txt"
output_file_before = "first1000.txt"
output_file_after = "all the rest.txt"

import os
# Get the directory of the input file
input_directory = os.path.dirname(os.path.abspath(input_file))

# Set the working directory to the input file's directory
os.chdir(input_directory)
# Initialize counters
count = 0

# Open the input file for reading
with open(input_file, "r") as infile:
    before_content = ""
    after_content = ""

    # Read the file line by line
    for line in infile:
        # Check if the current line contains "END_ENTRY"
        if "END_ENTRY" in line:
            count += 1

            # If we have reached the 1000th occurrence of "END_ENTRY," break out of the loop
            if count == 1000:
                break
        
        # If we haven't reached the 1000th occurrence, append the line to the "before_content" string
        before_content += line

    # Read the remaining lines and append them to the "after_content" string
    for line in infile:
        after_content += line

# Write the content before and after the 1000th "END_ENTRY" to separate output files
with open(output_file_before, "w") as outfile_before:
    outfile_before.write(before_content)

with open(output_file_after, "w") as outfile_after:
    outfile_after.write(after_content)

print(f"Contents up to the 1000th END_ENTRY saved in {output_file_before}")
print(f"Contents after the 1000th END_ENTRY saved in {output_file_after}")

# %%
