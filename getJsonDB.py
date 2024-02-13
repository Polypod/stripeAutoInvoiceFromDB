import mysql.connector
import json
import os
import config

def main():
    # Establish connection
    conn = mysql.connector.connect(
        host=config.my_server,
        user=config.my_username, 
        password=config.my_password,
        database=config.my_database
    )

    # Create a cursor object
    cursor = conn.cursor(dictionary=True)

    # Execute the SQL query
    query = "SELECT * FROM sitelok"
    cursor.execute(query)

    # Fetch all rows as a list of dictionaries
    result = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    # Convert the list of dictionaries to JSON
    json_result = json.dumps(result, indent=4)
    return json_result

if __name__ == '__main__':
    json_from_db = main()

    # Save json_from_db to a file in the data directory
    data_dir = 'data/'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    json_file_path = os.path.join(data_dir, 'sitelok.json')
    with open(json_file_path, 'w') as outfile:
        outfile.write(json_from_db)
