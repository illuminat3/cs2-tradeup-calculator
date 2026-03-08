import urllib.request
import urllib.parse
import json
from dtos.skin_info import skin
from dtos.listing import listing
from services.marketplaces.csfloat.csfloat_mapping import csfloat_mapping

class csfloat_marketplace:
    def __init__(self, csfloat_mapping: csfloat_mapping, api_key: str, base_url: str):
        self.csfloat_mapping = csfloat_mapping
        self.api_key = api_key
        self.base_url = base_url

    def find_listings(self, skin: skin) -> list[listing]:
        max_search_float = skin.float_value + 0.1
        min_search_float = skin.min_float
        bucket_count = 5
        increment = (max_search_float - min_search_float) / bucket_count
        paint_index = self.csfloat_mapping.get_paint_index(skin)
        for i in range(bucket_count):
            min_float = min_search_float + i * increment
            max_float = min_search_float + (i + 1) * increment
            print(f"Searching for listings with float between {min_float:.4f} and {max_float:.4f}")
            listings = self.fetch_skins_for_float_range(min_float, max_float, paint_index, skin)
            if listings:
                return listings
        return []

    def fetch_skins_for_float_range(self, min_float: float, max_float: float, paint_index: int, input_skin: skin) -> list[listing]:
        params = {
            "min_float": min_float,
            "max_float": max_float,
            "limit": 50,
            "type": "buy_now",
            "category": 1,
            "paint_index": paint_index
        }
        listings = []
        cursor = None
        while True:
            page_params = params.copy()
            if cursor:
                page_params["cursor"] = cursor
            url = f"{self.base_url}?{urllib.parse.urlencode(page_params)}"
            req = urllib.request.Request(url, headers={"Authorization": self.api_key})
            try:
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode())
            except urllib.error.HTTPError:
                print(f"Failed to fetch listings for float range {min_float}-{max_float}")
                break
            for item in data.get("data", []):
                price = item.get("price") / 100
                float_value = float(item["item"]["float_value"])
                listing_id = item.get("id")
                csfloat_link = f"https://csfloat.com/item/{listing_id}"

                marketplace_skin = skin(
                    finish_name=input_skin.finish_name,
                    weapon_type=input_skin.weapon_type,
                    collection_name=input_skin.collection_name,
                    min_float=min_float,
                    max_float=max_float,
                    float_value=float_value,
                    rarity=input_skin.rarity
                )
                listings.append(listing(price=price, skin=marketplace_skin, url=csfloat_link))
            cursor = data.get("cursor")
            if not cursor or not data.get("data"):
                break
        return listings