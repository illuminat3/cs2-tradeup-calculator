from dataclasses import dataclass
from dtos.counter_strike_enums import collection, rarity, weapon_type

@dataclass
class skin:
	@property
	def skin_name(self) -> str:
		return f"{self.weapon_type} | {self.finish_name}"

	finish_name: str
	weapon_type: weapon_type
	collection_name: collection
	min_float: float
	max_float: float
	float_value: float
	rarity: rarity 

