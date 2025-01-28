from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

hostname = 'localhost'
database = 'anindita'
username = 'postgres'
pwd = 'postgres'
port_id = 5432

def connect_db():
    return psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )

@app.route('/initialize', methods=['GET'])
def initialize_db():
    try:
        conn = connect_db()
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute('DROP TABLE IF EXISTS employee')
                create_script = ''' CREATE TABLE IF NOT EXISTS employee(
                                        id int PRIMARY KEY,
                                        name varchar(40) NOT NULL,
                                        salary int,
                                        dept_id varchar(30))'''
                cur.execute(create_script)
                insert_script = 'INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
                insert_values = [(1, 'James', 12000, 'D1'), (2, 'Robin', 13000, 'D2'), (3, 'Xavier', 14000, 'D3')]
                for record in insert_values:
                    cur.execute(insert_script, record)
        return jsonify({"message": "Database initialized"}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    try:
        conn = connect_db()
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                insert_script = 'INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
                cur.execute(insert_script, (data['id'], data['name'], data['salary'], data['dept_id']))
        return jsonify({"message": "Employee created"}), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        conn = connect_db()
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute('SELECT * FROM employee')
                employees = [{"id": record['id'], "name": record['name'], "salary": record['salary'], "dept_id": record['dept_id']} for record in cur.fetchall()]
        return jsonify(employees), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    try:
        conn = connect_db()
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                update_script = 'UPDATE employee SET name = %s, salary = %s, dept_id = %s WHERE id = %s'
                cur.execute(update_script, (data['name'], data['salary'], data['dept_id'], id))
        return jsonify({"message": "Employee updated"}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        conn = connect_db()
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                delete_script = 'DELETE FROM employee WHERE id = %s'
                cur.execute(delete_script, (id,))
        return jsonify({"message": "Employee deleted"}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True)
