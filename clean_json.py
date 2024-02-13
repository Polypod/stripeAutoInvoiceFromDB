import json
import os
import re

# Assuming getJsonDB is a module you've defined
import getJsonDB

def clean_custom5_field(json_from_db):
    cleaned_customers = []
    for customer in json_from_db:
        # Skip customers marked as DORMANT
        if customer.get('Custom11', '') != '':
            continue  # Skip the rest of the loop for this customer

        # Initialize cleaned_customer with already clean fields
        cleaned_customer = {
            'Name': customer.get('Name'),
            'Email': customer.get('Email'),
            'Usergroups': customer.get('Usergroups'),
        }

        if 'Custom5' in customer:
            cleaned_address = customer['Custom5']
            # Replace multiple spaces with a single space
            cleaned_address = re.sub(r'\s+', ' ', cleaned_address)
            # Assign cleaned address to the 'Address' field
            cleaned_customer['Address'] = cleaned_address

        cleaned_customers.append(cleaned_customer)

    return cleaned_customers

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

    cleaned_customers = clean_custom5_field(json_from_db)

    # Save the cleaned customer data, excluding DORMANT customers
    cleaned_file_path = os.path.join(data_dir, 'customer_links.json')
    with open(cleaned_file_path, 'w') as outfile:
        json.dump(cleaned_customers, outfile, indent=4)

if __name__ == "__main__":
    main()
