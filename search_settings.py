import json
from dataclasses import dataclass
from skin_info import rarity, collection, weapon_type

@dataclass
class search_settings:
	input_filters: list[search_input]
	target_float: float

@dataclass
class search_input:
	count: int

@dataclass
class skin_input(search_input):
	skin_name: str

@dataclass
class weapon_finish_input(search_input):
	finish_name: str
	weapon_type: weapon_type

@dataclass
class collection_input(search_input):
	collection_name: collection
	rarity: rarity

class search_settings_service:
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