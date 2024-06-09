import csv

# This program is a solution to the multi record issue with the export 
# from Integrate.io . The program will use Python csv library to read,
# manipulate, and write the data into a suitable format.

file_path = '/home/kristen-descant/IntegrateSolution/mock_clients.csv' # path to csv file, hard coded for testing
output_file_path = '/home/kristen-descant/IntegrateSolution/output.csv'

# function to read data from csv file
def read_csv(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# function to add related member,spouse,children to dictionary
def group_by_member(records):
    grouped = {}        # a nested dictionary 
    for record in records:
        member_ssn = record['Member SSN']
        if member_ssn not in grouped:
            grouped[member_ssn] = {
                'Member': [],
                'Spouse': [],
                'Child': []
            }
        grouped[member_ssn][record['Relationship']].append(record)  # relationship: record, will append multiple child records
    return grouped

# function to reformat data so that member, spouse, and child records are inline
def reformat_grouped_data(grouped_data):
    reformatted_records = []
    for member_ssn, relationships in grouped_data.items():
        if 'Member' in relationships and relationships['Member']:
            member_record = relationships['Member'][0].copy()  # Copy the member's record
            # Initialize empty lists to hold spouse and child records
            spouses = relationships['Spouse']
            children = relationships['Child']
            
            # Check and add details of the spouse record
            if relationships['Spouse']:
                spouse = relationships['Spouse'][0]  # There is only one spouse
                for key, value in spouse.items():
                    member_record[f'Spouse_{key}'] = value
            
            # Add details of child records inline
            for i, child in enumerate(children):
                for key, value in child.items():
                    member_record[f'Child_{i+1}_{key}'] = value
            
            reformatted_records.append(member_record)
    return reformatted_records

# function to write formatted data to csv file
def write_csv(output_file_path, records, fieldnames):
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

# Read the CSV file
records = read_csv(file_path)

# Group records by Member SSN
grouped_data = group_by_member(records)

# Reformat the grouped data
formatted_data = reformat_grouped_data(grouped_data)

# Determine the fieldnames for the output file
# Start with the member's fields
output_fieldnames = list(records[0].keys())

# Since there can only be one spouse, add fields for a single spouse
for key in records[0].keys():
    output_fieldnames.append(f'Spouse_{key}')

# Dynamically add fields for each child based on their positions
max_children = max(len(relationships['Child']) for relationships in grouped_data.values())

# Add fields for children
for i in range(1, max_children + 1):
    for key in records[0].keys():
        output_fieldnames.append(f'Child_{i}_{key}')

# Write the reformatted data to a new CSV file
write_csv(output_file_path, formatted_data, output_fieldnames)
