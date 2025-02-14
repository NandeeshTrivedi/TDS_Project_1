import json

def sort_contacts(input_file, output_file):
    # Read the contacts from the input file
    with open(input_file, 'r') as f:
        contacts = json.load(f)
    
    # Sort the contacts by last_name, then first_name
    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
    
    # Write the sorted contacts to the output file
    with open(output_file, 'w') as f:
        json.dump(sorted_contacts, f, indent=2)
    
    print(f"Contacts sorted and written to {output_file}")
