from datetime import datetime

from flasgger import Swagger
from flask import Flask, jsonify
from flask import request
from flask_basicauth import BasicAuth
from flask_cors import CORS
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1999'
app.config['MYSQL_DATABASE_DB'] = 'task_manager_db'
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

mysql = MySQL()
mysql.init_app(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

swagger = Swagger(app)

basic_auth = BasicAuth(app)


@app.route('/')
def hello():
    """
    Hello World endpoint
    ---
    responses:
      200:
        description: A simple hello message
    """
    return 'Hello, World!'


@app.route('/tasks', methods=['GET'])
@basic_auth.required
def get_tasks():
    """
    Get all tasks
    ---
    responses:
      200:
        description: Returns a list of tasks
    """
    conn = mysql.connect()
    cur = conn.cursor()
    try:

        cur.execute("SELECT * FROM tasks")

        rows = cur.fetchall()

        tasks = []
        for row in rows:
            task = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'due_date': row[3]
            }
            tasks.append(task)

        return jsonify(tasks)

    except Exception as e:

        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>', methods=['GET'])
@basic_auth.required
def get_task(task_id):
    """
    Get a specific task by ID
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task
    responses:
      200:
        description: Returns the task details
      404:
        description: Task not found
    """
    conn = mysql.connect()
    cur = conn.cursor()
    try:

        cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))

        row = cur.fetchone()

        if row:

            task = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'due_date': row[3]
            }

            return jsonify(task)
        else:

            return jsonify({'error': 'Task not found'}), 404

    except Exception as e:

        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks', methods=['POST'])
@basic_auth.required
def add_task():
    """
    Add a new task
    ---
    parameters:
      - name: task_data
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Title of the task
            description:
              type: string
              description: Description of the task
            due_date:
              type: string
              format: date
              description: Due date of the task (YYYY-MM-DD)
    responses:
      200:
        description: Task added successfully
      400:
        description: Bad Request (invalid JSON data or missing fields)
    """
    conn = mysql.connect()
    cur = conn.cursor()
    try:

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        required_fields = ['title', 'description', 'due_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        title = data['title']
        description = data['description']
        due_date_str = data['due_date']

        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid due_date format. Format should be YYYY-MM-DD'}), 400

        cur.execute("INSERT INTO tasks (title, description, due_date) VALUES (%s, %s, %s)",
                    (title, description, due_date_str))

        conn.commit()

        return jsonify({'message': 'Task added successfully'})

    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@basic_auth.required
def update_task(task_id):
    """
    Update a task by ID
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task to update
      - name: task_data
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: New title of the task
            description:
              type: string
              description: New description of the task
            due_date:
              type: string
              format: date
              description: New due date of the task (YYYY-MM-DD)
    responses:
      200:
        description: Task updated successfully
      400:
        description: Bad Request (invalid JSON data or missing fields)
      404:
        description: Task not found
      500:
        description: Internal Server Error
    """
    conn = mysql.connect()
    cur = conn.cursor()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        required_fields = ['title', 'description', 'due_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        title = data['title']
        description = data['description']
        due_date = data['due_date']

        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid due_date format. Format should be YYYY-MM-DD'}), 400

        cur.execute("UPDATE tasks SET title = %s, description = %s, due_date = %s WHERE id = %s",
                    (title, description, due_date, task_id))

        conn.commit()

        return jsonify({'message': 'Task updated successfully'})

    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@basic_auth.required
def delete_task(task_id):
    """
    Delete a task by ID
    ---
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task to delete
    responses:
      200:
        description: Task deleted successfully
      404:
        description: Task not found
      500:
        description: Internal Server Error
    """
    conn = mysql.connect()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))

        conn.commit()

        return jsonify({'message': 'Task deleted successfully'})

    except Exception as e:

        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
