from flask import Flask, request, jsonify
import traceback
import pyodbc
import pandas as pd
from config import servers, column_

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})


# Establishing the database connection
def create_connection():
    server_config = servers["server1"]
    return pyodbc.connect(
        "DRIVER="
        + server_config["driver"]
        + ";SERVER="
        + server_config["server"]
        + ";DATABASE="
        + server_config["database"]
        + ";UID="
        + server_config["username"]
        + ";PWD="
        + server_config["password"]
    )



# Select operation
@app.route("/select", methods=["GET"])
def select_data():
    key1 = request.args.get("SampleCode")
    key2 = request.args.get("Instrument")
    key3 = request.args.get("RemarkNo")

    conn = create_connection()
    cursor = conn.cursor()

    if key1 and not key2 and not key3:
        # Build the SQL query with only the first key
        query = f"SELECT TOP 100 * FROM [SAR].[dbo].[Routine_RequestLab] WHERE ItemStatus = 'LIST NORMAL' AND SampleCode = '{key1}' ORDER BY id DESC"
    elif key1 and key2 and not key3:
        # Build the SQL query with the first and second keys
        query = f"SELECT TOP 100 * FROM [SAR].[dbo].[Routine_RequestLab] WHERE ItemStatus = 'LIST NORMAL' AND SampleCode = '{key1}' AND InstrumentName = '{key2}' ORDER BY id DESC"
    elif key1 and not key2 and key3:
        # Build the SQL query with the first and third keys
        query = f"SELECT TOP 100 * FROM [SAR].[dbo].[Routine_RequestLab] WHERE ItemStatus = 'LIST NORMAL' AND SampleCode = '{key1}' AND RemarkNo = '{key3}' ORDER BY id DESC"
    elif not key1 and key2 and key3:
        # Build the SQL query with the second and third keys
        query = f"SELECT TOP 100 * FROM [SAR].[dbo].[Routine_RequestLab] WHERE ItemStatus = 'LIST NORMAL' AND InstrumentName = '{key2}' AND RemarkNo = '{key3}' ORDER BY id DESC"
    elif key1 and key2 and key3:
        # Build the SQL query with all three keys
        query = f"SELECT TOP 100  * FROM [SAR].[dbo].[Routine_RequestLab] WHERE ItemStatus = 'LIST NORMAL' AND SampleCode = '{key1}' AND InstrumentName = '{key2}' AND RemarkNo = '{key3}' ORDER BY id DESC"
    else:
        # Build the SQL query without any filtering
        query = f"SELECT TOP 100 * FROM [SAR].[dbo].[Routine_RequestLab] WHERE ItemStatus = 'LIST NORMAL' ORDER BY id DESC"

    print("Query:", query)
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert result set to a list of dictionaries
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    return jsonify(results)


# Insert operation
@app.route("/requestbalance", methods=["POST"])
def insert_data():
    conn = create_connection()
    cursor = conn.cursor()
    print(request.json)
    input = request.json
    name = (input['name'])
    query = f"SELECT TOP 100 {column_['query1']} FROM [SAR].[dbo].[Routine_RequestLab] WHERE ItemStatus = 'LIST NORMAL' AND UserListAnalysis = '{name}' AND InstrumentName IN ('ICP', 'Sludge', 'Acid Number(Nox Rust)', 'CO32-', 'Cwt', 'Cwt.3 layers', 'Cwt. PULS', 'Solid Content(Nox Rust)', 'SSM',%NV(WAX),%NV(Nox Rust),%NV) ORDER BY id DESC"

    cursor.execute(query) 
    rows = cursor.fetchall()
    #
    # Convert result set to a list of dictionaries
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    return jsonify(results)


# Delete operation
@app.route("/delete/<int:record_id>", methods=["DELETE"])
def delete_data(record_id):
    cursor = conn.cursor()
    query = "DELETE FROM your_table WHERE id = ?"
    cursor.execute(query, (record_id,))
    conn.commit()

    return "Data deleted successfully"


# Update operation
@app.route("/update/<int:record_id>", methods=["PUT"])
def update_data(record_id):
    data = request.get_json()
    cursor = conn.cursor()
    query = "UPDATE your_table SET column1 = ?, column2 = ? WHERE id = ?"
    cursor.execute(query, (data["value1"], data["value2"], record_id))
    conn.commit()

    return "Data updated successfully"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
