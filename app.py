from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import traceback
from stock import StockTracker
from ai import AIInsightGenerator
app = Flask(__name__)
CORS(app)

tracker = StockTracker()
ai_generator = AIInsightGenerator()

@app.before_request
def log_request():
    print(f"→ {request.method} {request.path}")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")
@app.route('/favicon.ico')
def favicon():
    return '', 204
@app.errorhandler(400)
def bad_request(e):
    print("Bad Request:", e)
    return jsonify({"error": "Bad request"}), 400


@app.route('/stock/<symbol>', methods=["GET"])
def get_stock(symbol):
    try:
        stock = tracker.get_stock(symbol)
        if not stock.history or len(stock.history) == 0:
            return jsonify({"error": "No price history available."}), 404
        if stock.price is None:
            return jsonify({"error": "No price available."}), 404

        if len(stock.history) >= 5:
            recent_prices = [p["price"] for p in stock.history[-5:]]
            stock.prediction = tracker.model.predict(recent_prices)
        else:
            stock.prediction = None
        return jsonify({
            "symbol": stock.symbol,
            "price": stock.price,
            "history": stock.history[-20:],
            "prediction": stock.prediction,
        })
    except Exception as e:
        print("Error in get_stock:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400

"""
@app.route('/stock/<symbol>/insight', methods=["GET"])
def get_insight(symbol):
    try:
        stock = tracker.get_stock(symbol)
        if stock is None:
            return jsonify({"error": f"Stock symbol '{symbol}' not found."}), 404
        recent_prices = [p["price"] for p in stock.history[-5:]]
        insight = ai_generator.generate_insight(symbol, recent_prices)
        return jsonify({"insight": insight})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        

@app.route("/stock/<symbol>/prediction", methods=["GET"])
def get_prediction(symbol):
    try:
        stock = tracker.get_stock(symbol)
        return jsonify({"prediction": stock.prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
"""

if __name__ == "__main__":
    app.run(debug=True)
