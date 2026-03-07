from dataclasses import asdict, fields
import json
from typing import List
from dtos.skin_info import skin
from dtos.search_inputs import search_input

_EXCLUDED_FILTER_FIELDS = {f.name for f in fields(search_input)}

class skin_repository:
	def __init__(self, skin_data_filepath: str):
		self.skin_data_filepath = skin_data_filepath

	def _parse_skin_item(self, item: dict) -> skin | None:
		if "skin_name" in item:
			parts = item["skin_name"].split(" | ")
			if len(parts) != 2:
				return None
			item = {**item, "weapon_type": parts[0], "finish_name": parts[1]}
			item.pop("skin_name")
		return skin(**item)

	def get_skin_data(self) -> List[skin]:
		with open(self.skin_data_filepath, "r", encoding="utf-8") as f:
			data = json.load(f)
		return [s for item in data if (s := self._parse_skin_item(item)) is not None]

	def get_skins_from_input(self, search_input) -> List[skin]:
		filters = {
			k: v for k, v in asdict(search_input).items()
			if v is not None and k not in _EXCLUDED_FILTER_FIELDS
		}
		return [
			s for s in self.get_skin_data()
			if all(getattr(s, key, None) == value for key, value in filters.items())
		]