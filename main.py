from services.marketplaces.config_service import config_service
from services.search_service import search_service
from services.input_analyser_service import input_analyser_service
from services.skin_repository import skin_repository
from services.marketplaces.csfloat.csfloat_marketplace import csfloat_marketplace
from services.skin_selector_service import skin_selector_service

search_file = "config/search.json"
config_file = "config/marketplace-config.json"
skins_file = "data/skins.json"

def main():
	config_svc = config_service(config_file)
	csfloat_config = config_svc.get_marketplace_config("csfloat")
	search_svc = search_service(search_file)
	skin_repo = skin_repository(skins_file)
	input_analyser_svc = input_analyser_service(skin_repo)
	csfloat_marketplace_svc = csfloat_marketplace(csfloat_config.api_key, csfloat_config.base_url)
	skin_selector_svc = skin_selector_service()

	search_settings = search_svc.get_search_settings()
	inputs = input_analyser_svc.analyse_input(search_settings)

	listing_inputs = {}
	for count, skins in inputs.items():
		total_listings = []
		for skin in skins:
			listings = csfloat_marketplace_svc.find_listings(skin)
			total_listings.extend(listings)

		listing_inputs[count] = total_listings
	
	selected_listings = skin_selector_svc.select_skins_for_tradeup(listing_inputs, search_settings.target_float)

	for listing in selected_listings:
		print(f"Selected: {listing.skin.skin_name} | Price: ${listing.price:.2f}, Float: {listing.skin.float_value:.4f}, Link: {listing.url}")

if __name__ == "__main__":
	main()