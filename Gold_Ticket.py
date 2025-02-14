import sqlite3

def calculate_gold_ticket_sales(db_file, output_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Execute the SQL query to calculate total sales for Gold tickets
    query = "SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"
    cursor.execute(query)

    # Fetch the result
    total_sales = cursor.fetchone()[0]

    # Close the database connection
    conn.close()

    # Write the result to the output file
    with open(output_file, 'w') as f:
        f.write(str(total_sales))

    print(f'Total sales for Gold tickets: {total_sales}')
