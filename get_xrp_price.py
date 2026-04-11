import requests
import pandas as pd


def get_price_data(coin_id='cosmos', column_name=None, vs_currency='usd', days=20):
    """
    Fetch coin market chart data and return a DataFrame with date and a column named column_name.
    column_name defaults to coin_id + '_price' if not provided.
    """
    if column_name is None:
        column_name = f"{coin_id}_price"

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": str(days),
        "interval": "daily",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        prices = data.get("prices")

        if prices:
            df = pd.DataFrame(prices, columns=["timestamp", "price"])
            df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.normalize()
            df = df[["date", "price"]]
            df.rename(columns={"price": column_name}, inplace=True)
            return df

        print("No price data found in the response for", coin_id)
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {coin_id}: {e}")
        return pd.DataFrame()


def get_atom_price_data(days=20):
    return get_price_data(coin_id="cosmos", column_name="atom_price", days=days)


def get_xrp_price_data(days=20):
    return get_price_data(coin_id="ripple", column_name="xrp_price", days=days)


def get_btc_price_data(days=20):
    return get_price_data(coin_id="bitcoin", column_name="btc_price", days=days)


def get_eth_price_data(days=20):
    return get_price_data(coin_id="ethereum", column_name="eth_price", days=days)


if __name__ == "__main__":
    atom_df = get_atom_price_data(days=20)
    xrp_df = get_xrp_price_data(days=20)
    btc_df = get_btc_price_data(days=20)
    eth_df = get_eth_price_data(days=20)
    if not atom_df.empty and not xrp_df.empty and not btc_df.empty and not eth_df.empty:
        df = atom_df
        for other in [xrp_df, btc_df, eth_df]:
            df = pd.merge(df, other, on="date", how="outer")
        print("ATOM, XRP, BTC & ETH Price Data (last 20 days):")
        print(df)
    else:
        print("Could not retrieve the full set of ATOM, XRP, BTC, and ETH data.")