from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# Thông tin kết nối
import os

server = os.getenv('DB_HOST', 'DESKTOP-6CTP857\\SQLEXPRESS')
database = os.getenv('DB_NAME', 'mydb')
conn_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Lấy danh sách items
@app.route('/items', methods=['GET'])
def get_items():
    try:
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        return jsonify([{'id': row[0], 'name': row[1]} for row in items])
    except Exception as e:
        print("Lỗi:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

# Thêm item mới
@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    try:
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name) VALUES (?)", (new_item['name'],))
        conn.commit()
        return jsonify({'message': 'Item added successfully!'}), 201
    except Exception as e:
        print("Lỗi:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

# Cập nhật item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_item = request.json
    try:
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET name = ? WHERE id = ?", (updated_item['name'], item_id))
        conn.commit()
        return jsonify({'message': 'Item updated successfully!'}), 200
    except Exception as e:
        print("Lỗi:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

# Xóa item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return jsonify({'message': 'Item deleted successfully!'}), 200
    except Exception as e:
        print("Lỗi:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(port=5000)