import json
import os

# Assuming getJsonDB is a module you've defined
import getJsonDB

def main():
    json_string = getJsonDB.main()
    # Parse the JSON string returned by getJsonDB.main()
    json_from_db = json.loads(json_string)

    # Ensure the data directory exists
    data_dir = 'data/'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Save the original JSON data to a file
    json_file_path = os.path.join(data_dir, 'sitelok.json')
    with open(json_file_path, 'w') as outfile:
        outfile.write(json_string)  # Write the original JSON string directly
        
    # Initialize an empty list to hold cleaned customer data
    cleaned_customers = []

    # Assuming json_from_db is a list of dictionaries
    for customer in json_from_db:
        # Extract and clean relevant fields for each customer
        cleaned_customer = {
            'Name': customer.get('Name'),
            'Email': customer.get('Email'),
            'Usergroups': customer.get('Usergroups'),
        }
        address = customer.get('Custom5', '')
        # Clean up 'Address' by replacing non-alphabetical characters with spaces
        cleaned_address = ''.join(c if c.isalpha() or c.isspace() else ' ' for c in address)
        cleaned_customer['Address'] = cleaned_address
        
        cleaned_customers.append(cleaned_customer)
        
    # TODO:If user DORMANT (i.e "Custom11") is not empty(''), remove this customer in customer_links.json (or other logic)

    # Save the cleaned customer data
    cleaned_file_path = os.path.join(data_dir, 'customer_links.json')
    with open(cleaned_file_path, 'w') as outfile:
        json.dump(cleaned_customers, outfile, indent=4)

if __name__ == "__main__":
    main()
