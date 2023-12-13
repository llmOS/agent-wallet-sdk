import json
import os
from random import randrange
from typing import Dict
from typing import List
from typing import Optional

import requests

API_URL: str = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?start=1&limit=5000&sort=cmc_rank"
API_KEY: str = os.getenv("COINMARKETCAP_API_KEY")

CACHE_FILE_NAME: str = "data/coins.json"


def execute() -> Dict:
    coins = _get_cache()
    if not coins:
        coins = _get_coins()
    if not coins:
        raise Exception("Failed to get coins")
    eth_coins = _get_eth_coins(coins)
    print(f"Got {len(eth_coins)} crypto currencies")
    coin_index = randrange(2, 50)
    coin = eth_coins[coin_index]
    print(f"Coin: {coin}")
    return coin


def _get_cache() -> Optional[List[Dict]]:
    try:
        with open(CACHE_FILE_NAME, "r", encoding="utf-8") as f:
            return json.loads(f.read())["data"]
    except Exception as e:
        print(f"Failed to get coins from cache {e}")
        return None


def _get_coins() -> Optional[List[Dict]]:
    res = requests.get(
        API_URL,
        headers={
            "Accept": "application/json",
            "X-CMC_PRO_API_KEY": API_KEY
        }
    )
    coins = res.json()
    os.makedirs(os.path.dirname(CACHE_FILE_NAME), exist_ok=True)
    with open(CACHE_FILE_NAME, "w", encoding="utf-8") as f:
        f.write(json.dumps(coins, indent=2))
    return coins["data"]


def _get_eth_coins(coins: List[Dict]) -> List[Dict]:
    filtered = []
    for c in coins:
        if (c.get("platform") or {}).get("symbol", "") == "ETH":
            filtered.append(c)
    return filtered


if __name__ == '__main__':
    execute()
