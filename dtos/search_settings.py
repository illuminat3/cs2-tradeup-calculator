from dataclasses import dataclass
from dtos.search_inputs import search_input

@dataclass
class search_settings:
	input_filters: list[search_input]
	target_float: float
