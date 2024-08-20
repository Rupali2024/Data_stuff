import os

# Define the path to the folder containing annotation files and the output folder
input_folder = 'LINKNET/data_auto_annotate_labels'
output_folder = 'LINKNET/labels'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename)
        
        with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            
            for line in infile:
                # print(line, "length of file")

                # Assuming the class label is the first element on each line, split the line by spaces
                parts = line.split()
                
                # Check if the line contains at least one element and the class is 15
                if len(parts) > 0 and parts[0] == '15':
                    # Write the line to the output file if class is 15
                    outfile.write(line)


print(f"Filtered annotations have been saved to {output_folder}")
