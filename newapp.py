from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Database connection parameters
db_params = {
    'dbname': 'anindita',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}


def create_connection():
    """ Create a database connection """
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
    except Exception as e:
        print(f"Error connecting to database: {e}")
    return conn


def create_table():
    """ Create a table """
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS amnex.users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()


def insert_user(name, email, contact):
    """ Insert a new user into the users table """
    conn = create_connection()
    cursor = conn.cursor()  
    try:
        cursor.execute("""
            INSERT INTO amnex.users (name, email, contact) VALUES (%s, %s, %s) RETURNING id;
        """, (Anindita, anindita23@gmail.com, 7982404341)) #
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        print(f"Error inserting user: {e}")
    finally:
        cursor.close()
        conn.close()


def get_users():
    """ Query all rows in the users table """
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM amnex.users;")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error fetching users: {e}")
    finally:
        cursor.close()
        conn.close()


def update_user(user_id, name, email):
    """ Update a user by user id """
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE amnex.users SET name = %s, email = %s WHERE id = %s;
        """, (name, email, user_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating user: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_user(user_id):
    """ Delete a user by user id """
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM amnex.users WHERE id = %s;", (user_id,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting user: {e}")
    finally:
        cursor.close()
        conn.close()


@app.route('/users', methods=['POST'])
def api_insert_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    user_id = insert_user(name, email)
    return jsonify({'id': user_id}), 201

@app.route('/users', methods=['GET'])
def api_get_users():
    users = get_users()
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    update_user(user_id, name, email)
    return jsonify({'status': 'success'}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    delete_user(user_id)
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    create_table()  # Ensure the table is created before starting the app
    app.run(host='localhost', port=8889, debug=True)