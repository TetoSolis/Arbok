from flask import Flask, jsonify
import os

app = Flask(__name__)
COUNTER_FILE = "counter.txt"

def get_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip())

def update_counter(value):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(value))

@app.route("/increment", methods=["GET"])
def increment():
    counter = get_counter() + 1
    update_counter(counter)
    return jsonify({"count": counter})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
