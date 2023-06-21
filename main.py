from flask import Flask, request, jsonify
import pyodbc
import pandas as pd
from config import servers

app = Flask(__name__)

# Establishing the database connection
def create_connection():
    server_config = servers['server1']
    return pyodbc.connect('DRIVER=' + server_config['driver'] + ';SERVER=' + server_config['server'] + ';DATABASE=' + server_config['database'] + ';UID=' + server_config['username'] + ';PWD=' + server_config['password'])

# Select operation
@app.route('/select', methods=['GET'])
def select_data():
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT TOP 100 * FROM [SAR].[dbo].[Routine_RequestLab] order by id desc"
    cursor.execute(query)
    rows = cursor.fetchall()
    # Convert result set to a list of dictionaries
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    return jsonify(results)

# Insert operation
@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    cursor = conn.cursor()
    query = "INSERT INTO your_table (column1, column2) VALUES (?, ?)"
    cursor.execute(query, (data['value1'], data['value2']))
    conn.commit()

    return 'Data inserted successfully'

# Delete operation
@app.route('/delete/<int:record_id>', methods=['DELETE'])
def delete_data(record_id):
    cursor = conn.cursor()
    query = "DELETE FROM your_table WHERE id = ?"
    cursor.execute(query, (record_id,))
    conn.commit()

    return 'Data deleted successfully'

# Update operation
@app.route('/update/<int:record_id>', methods=['PUT'])
def update_data(record_id):
    data = request.get_json()
    cursor = conn.cursor()
    query = "UPDATE your_table SET column1 = ?, column2 = ? WHERE id = ?"
    cursor.execute(query, (data['value1'], data['value2'], record_id))
    conn.commit()

    return 'Data updated successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)