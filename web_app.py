from flask import Flask, jsonify, render_template, Response, request
from flask_cors import CORS
import pandas as pd
from get_xrp_price import (
    get_atom_price_data,
    get_xrp_price_data,
    get_btc_price_data,
    get_eth_price_data,
)
import os

app = Flask(__name__)
CORS(app)


def merged_prices(days=20):
    atom = get_atom_price_data(days=days)
    xrp = get_xrp_price_data(days=days)
    btc = get_btc_price_data(days=days)
    eth = get_eth_price_data(days=days)
    dfs = [df for df in [atom, xrp, btc, eth] if not df.empty]
    if not dfs:
        return pd.DataFrame()
    df = dfs[0]
    for other in dfs[1:]:
        df = pd.merge(df, other, on="date", how="outer")
    df = df.sort_values("date").reset_index(drop=True)
    return df


@app.route("/api/prices")
def api_prices():
    days = int(request.args.get("days", 20))
    df = merged_prices(days=days)
    if df.empty:
        return jsonify({"error": "no data"}), 500
    df2 = df.copy()
    df2["date"] = df2["date"].dt.strftime("%Y-%m-%d")
    return jsonify(df2.to_dict(orient="records"))


@app.route("/api/prices/csv")
def api_prices_csv():
    days = int(request.args.get("days", 20))
    df = merged_prices(days=days)
    if df.empty:
        return Response("No data", status=500, mimetype="text/plain")
    df2 = df.copy()
    df2["date"] = df2["date"].dt.strftime("%Y-%m-%d")
    csv_data = df2.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=atom_xrp_prices.csv"},
    )


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)