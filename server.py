from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище подтвержденных платежей
payments = []

@app.route("/cloudtips_webhook", methods=["POST"])
def cloudtips_webhook():
    data = request.json

    # Унифицированный формат
    payment = {
        "id": data.get("id"),
        "status": data.get("status") or data.get("payment_status"),
        "amount": data.get("amount") or data.get("sum"),
        "payload": None
    }

    # Ищем payload везде, где он может жить
    if "payload" in data:
        payment["payload"] = data["payload"]
    elif "data" in data and isinstance(data["data"], dict):
        payment["payload"] = data["data"].get("payload")

    # Сохраняем только если есть payload
    if payment["payload"]:
        payments.append(payment)
        print("Saved:", payment)
    else:
        print("Ignored payment — no payload:", data)

    return "ok"

@app.route("/payments", methods=["GET"])
def get_payments():
    # Возвращаем только платежи, у которых есть payload
    return jsonify(payments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
