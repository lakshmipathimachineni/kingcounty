import sqlite3

# Connect to the database
conn = sqlite3.connect('bus_transport.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a SQL query to select all the rows from the stops table
cursor.execute('SELECT * FROM stops')

# Fetch all the rows and print them
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the database connection
conn.close()
