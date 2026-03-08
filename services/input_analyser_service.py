from dtos.search_settings import search_settings
from dtos.search_inputs import search_input
from dtos.skin_info import skin
from services.skin_repository import skin_repository

class input_analyser_service:
	def __init__(self, skin_repository: skin_repository):
		self.skin_repository = skin_repository

	def analyse_input(self, search_settings: search_settings) -> dict[int, list[skin]]:
		inputs = {}

		for input_filter in search_settings.input_filters:
			eligible_skins = self.skin_repository.get_skins_from_input(input_filter)
			
			for skin in eligible_skins:
				target_skin_float = self.get_target_float(skin, search_settings.target_float)
				skin.float_value = target_skin_float
				print(f"Skin: {skin.skin_name}, Target Float: {target_skin_float:.4f}")

			inputs[input_filter.count] = eligible_skins
		
		return inputs
	
	def get_target_float(self, skin: skin, target: float) -> float:
		float_range = skin.max_float - skin.min_float
		return skin.min_float + (target * float_range)
