import os
import psycopg2
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lấy thông tin kết nối từ biến môi trường
database_url = os.getenv('DATABASE_URL')

# Thử kết nối đến PostgreSQL với logic chờ
def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(database_url)
            return conn
        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL to be ready...")
            time.sleep(5)

# Khởi tạo cơ sở dữ liệu
def init_db():
    conn = wait_for_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS myuser (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT
    );
    """)
    # Xóa và chèn dữ liệu mẫu
    cur.execute("DELETE FROM myuser")
    cur.execute("INSERT INTO myuser (name, age) VALUES (%s, %s)", ('John Doe', 30))
    cur.execute("INSERT INTO myuser (name, age) VALUES (%s, %s)", ('Jane Smith', 25))
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = wait_for_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM myuser")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    
    conn = wait_for_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO myuser (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "User added successfully"}), 201

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = wait_for_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM myuser WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)