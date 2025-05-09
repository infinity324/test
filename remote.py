from flask import Flask, request, jsonify
import time

app = Flask(__name__)


@app.route("/remote", methods=["POST"])
def remote():
    data = request.get_json()
    print(data)
    time.sleep(3)
    a = data['a']
    b = data['b']
    c = a + b
    print(c)
    return jsonify({"result": c}), 200


if __name__ == "__main__":
    app.run(debug=True)
