from dtos.marketplace_config import marketplace_config

class config_service:
	def __init__(self, config_file: str):
		self.config_file = config_file
		self.marketplace_configs = self.load_marketplace_configs()

	def load_marketplace_configs(self) -> dict[str, marketplace_config]:
		import json
		with open(self.config_file, "r", encoding="utf-8") as f:
			data = json.load(f)
			configs = {}
			for marketplace_name, config in data.items():
				configs[marketplace_name] = marketplace_config(**config)
			return configs

	def get_marketplace_config(self, marketplace_name: str) -> marketplace_config:
		return self.marketplace_configs.get(marketplace_name)