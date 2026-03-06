from dataclasses import dataclass
from dtos.counter_strike_enums import collection, rarity, weapon_type

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