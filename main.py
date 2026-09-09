import os
from flask import Flask, request, jsonify

# Your actual import paths (since they are in the same folder or root src)
from addition import add
from subtraction import subtract
from multiplication import multiply
from division import divide

app = Flask(__name__)

# Read the OPERATION variable assigned to this specific container instance
# If nothing is provided, it defaults to 'add'
OPERATION = os.getenv("OPERATION", "add").lower()

@app.route("/calculate", methods=["POST"])
def calculate():
    # 1. Parse incoming JSON data safely
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON request body"}), 400
        
    # Get values and safely cast them to floats
    try:
        a = float(data.get("a"))
        b = float(data.get("b"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing inputs 'a' and 'b'. Must be numbers."}), 400

    # 2. Execute ONLY the logic this container is dedicated to perform
    try:
        if OPERATION == "add":
            result = add(a, b)
        elif OPERATION == "sub" or OPERATION == "subtract":
            result = subtract(a, b)
        elif OPERATION == "mul" or OPERATION == "multiply":
            result = multiply(a, b)
        elif OPERATION == "div" or OPERATION == "divide":
            result = divide(a, b)
        else:
            return jsonify({"error": f"Operation '{OPERATION}' is unrecognized"}), 400

        # 3. Return a clean API JSON response
        return jsonify({
            "status": "success",
            "container_operation": OPERATION,
            "inputs": {"a": a, "b": b},
            "result": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Internal port inside the container is set cleanly to 5000
    app.run(host="0.0.0.0", port=5000)

