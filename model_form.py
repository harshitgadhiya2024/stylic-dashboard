from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

COUPONS = {
    "HAGH56SD": 15,
    "WELCOME50": 10,
    "SAVE10": 10
}

@app.route("/")
def index():
    return render_template("credit-based.html")

@app.route("/api/check-coupon")
def check_coupon():
    code = request.args.get("code", "").upper()
    if code in COUPONS:
        return jsonify({"valid": True, "discount": COUPONS[code]})
    return jsonify({"valid": False, "discount": 0})

if __name__ == "__main__":
    app.run(debug=True)


# 8-10 years
