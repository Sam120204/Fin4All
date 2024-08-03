import os
import glob

# Get the list of all CSV files in the current directory
csv_files = glob.glob('*.csv')
json_files = glob.glob('*.json')

# Loop through the list and remove each file
for csv_file in csv_files:
    os.remove(csv_file)
    print(f'Removed {csv_file}')
for i in json_files:
    os.remove(i)
    print(f'Removed {i}')

print("All CSV files have been removed.")
