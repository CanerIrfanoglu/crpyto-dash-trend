import pandas as pd

df_crypto_universe = pd.read_csv("data/cryptodash_universe.csv")

df_crypto_universe.sort_values("coingecko_name", inplace=True)

# UI Selector Dict Keys
df_crypto_universe["label"] = (
    df_crypto_universe["coingecko_name"]
    + " ("
    + df_crypto_universe["cryptocompare_symbol"]
    + ")"
)

# UI Selector Dict Vals
df_crypto_universe["value"] = df_crypto_universe["cryptocompare_symbol"]


# UI Selector
crypto_dict = df_crypto_universe[["label", "value"]].to_dict("records")


target_map_iterator = list(
    zip(
        df_crypto_universe["cryptocompare_symbol"],
        df_crypto_universe["coingecko_id"],
    )
)
