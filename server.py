from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище платежей (память)
payments = []

@app.route("/cloudtips_webhook", methods=["POST"])
def cloudtips_webhook():
    data = request.json
    payments.append(data)
    print("Received:", data)
    return "ok"

@app.route("/payments", methods=["GET"])
def get_payments():
    return jsonify(payments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
