from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')

    # Example logic for processing the task
    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    try:
        # Here, you can call a function that processes the task, for example, using an LLM
        result = execute_task(task_description)  # Replace with actual task logic
        return jsonify({"message": "Task executed successfully", "result": result}), 200
    except Exception as e:
        return jsonify({"error": f"Agent failed to execute task: {str(e)}"}), 500

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path')

    # Check if the file exists
    if not file_path or not os.path.exists(file_path):
        return '', 404

    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content, 200
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500

def execute_task(task_description):
    # Simulate task execution, potentially calling an LLM or processing logic here
    if task_description.lower() == "example task":
        return "Task executed successfully"
    else:
        raise ValueError("Invalid task description")

if __name__ == '__main__':
    app.run(debug=True)
