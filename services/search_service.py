import json
from dtos.search_settings import search_settings
from dtos.search_inputs import skin_input, weapon_finish_input, collection_input
from dtos.counter_strike_enums import collection, rarity, weapon_type

class search_service:
	def __init__(self, filepath: str):
		self.filepath = filepath 

	def get_search_settings(self) -> search_settings:
		with open(self.filepath, "r") as f:
			data = json.load(f)

		filters = []
		for item in data["input_filters"]:
			count = item["count"]

			if "skin_name" in item:
				filters.append(skin_input(
					count=count,
					skin_name=item["skin_name"]
				))

			elif "weapon_type" in item and "finish_name" in item:
				filters.append(weapon_finish_input(
					count=count,
					finish_name=item["finish_name"],
					weapon_type=weapon_type[item["weapon_type"]]
				))

			elif "collection_name" in item and "rarity" in item:
				filters.append(collection_input(
					count=count,
					collection_name=collection[item["collection_name"]],
					rarity=rarity[item["rarity"]]
				))

			else:
				raise ValueError(f"Unknown filter format: {item}")

		return search_settings(
			input_filters=filters,
			target_float=data["target_float"]
		)