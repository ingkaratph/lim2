from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)

# SQL Server connection settings
server = '127.0.0.1'
database = 'auto'
username = 'sa'
password = '122345'
driver = '{ODBC Driver 17 for SQL Server}'

# Establishing the database connection
def create_connection():
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    conn = pyodbc.connect(connection_string)
    return conn

# SELECT operation
@app.route('/data', methods=['GET'])
def get_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [auto].[dbo].[data]')
    rows = cursor.fetchall()

    data = []
    for row in rows:
        # Assuming the table has three columns: id, name, and age
        item = {
            'id': row.id,
            'name': row.name,
            'age': row.age
        }
        data.append(item)

    conn.close()

    return jsonify(data)

# INSERT operation
@app.route('/data', methods=['POST'])
def add_data():
    conn = create_connection()
    cursor = conn.cursor()

    # Assuming the request data contains 'name' and 'age' fields
    name = request.json['name']
    age = request.json['age']

    # Inserting the data into the table
    cursor.execute("INSERT INTO your_table (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

    return 'Data added successfully'

# DELETE operation
@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    conn = create_connection()
    cursor = conn.cursor()

    # Deleting the data from the table based on the provided id
    cursor.execute("DELETE FROM your_table WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return 'Data deleted successfully'

# UPDATE operation
@app.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    conn = create_connection()
    cursor = conn.cursor()

    # Assuming the request data contains 'name' and 'age' fields
    name = request.json['name']
    age = request.json['age']

    # Updating the data in the table based on the provided id
    cursor.execute("UPDATE your_table SET name = ?, age = ? WHERE id = ?", (name, age, id))
    conn.commit()
    conn.close()

    return 'Data updated successfully'

if __name__ == '__main__':
    app.run()
