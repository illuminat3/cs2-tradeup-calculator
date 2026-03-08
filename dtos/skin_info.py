from dataclasses import dataclass
from dtos.counter_strike_enums import collection, rarity, weapon_type

@dataclass
class skin:
	finish_name: str
	weapon_type: weapon_type
	collection_name: collection
	min_float: float
	max_float: float
	float_value: float
	rarity: rarity

	def __post_init__(self):
		if isinstance(self.weapon_type, str):
			try:
				self.weapon_type = weapon_type(self.weapon_type)
			except ValueError:
				self.weapon_type = weapon_type[self.weapon_type]

		if isinstance(self.collection_name, str):
			try:
				self.collection_name = collection(self.collection_name)
			except ValueError:
				self.collection_name = collection[self.collection_name]

		if isinstance(self.rarity, str):
			try:
				self.rarity = rarity(self.rarity)
			except ValueError:
				self.rarity = rarity[self.rarity]

	@property
	def skin_name(self) -> str:
		return f"{self.weapon_type.name} | {self.finish_name}"