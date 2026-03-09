import json
from typing import List
from dtos.skin_info import skin
from dtos.search_inputs import collection_input, search_input, skin_input, weapon_finish_input

class skin_repository:
	def __init__(self, skin_data_filepath: str):
		self.skin_data_filepath = skin_data_filepath
		self.skin_data = self._get_skin_data()

	def get_skins_from_input(self, search_filter: search_input) -> List[skin]:
		if isinstance(search_filter, weapon_finish_input):
			return self._get_skins_by_weapon_finish(search_filter)
		elif isinstance(search_filter, skin_input):
			return self._get_skins_by_skin(search_filter)
		elif isinstance(search_filter, collection_input):
			return self._get_skins_by_collection(search_filter)
		else:
			raise ValueError(f"Unsupported search filter type: {type(search_filter)}")

	def _get_skins_by_weapon_finish(self, search_filter: weapon_finish_input) -> List[skin]:
		return [
			s for s in self.skin_data
			if s.weapon_type == search_filter.weapon_type 
			and s.finish_name == search_filter.finish_name
			and s.category == search_filter.category
		]

	def _get_skins_by_skin(self, search_filter: skin_input) -> List[skin]:
		return [
			s for s in self.skin_data
			if s.skin_name == search_filter.skin_name
			and s.category == search_filter.category
		]

	def _get_skins_by_collection(self, search_filter: collection_input) -> List[skin]:
		return [
			s for s in self.skin_data
			if s.collection_name == search_filter.collection_name 
			and s.rarity == search_filter.rarity
			and s.category == search_filter.category
		]

	def _parse_skin_item(self, item: dict) -> skin | None:
		if "skin_name" in item:
			parts = item["skin_name"].split(" | ")
			if len(parts) != 2:
				return None
			item = {**item, "weapon_type": parts[0], "finish_name": parts[1]}
			item.pop("skin_name")
		return skin(**item)

	def _get_skin_data(self) -> List[skin]:
		with open(self.skin_data_filepath, "r", encoding="utf-8") as f:
			data = json.load(f)
		return [s for item in data if (s := self._parse_skin_item(item)) is not None]

