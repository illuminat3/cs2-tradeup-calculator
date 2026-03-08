from dataclasses import dataclass
from dtos.skin_info import skin

@dataclass
class listing:
	price: float
	skin: skin
	url: str