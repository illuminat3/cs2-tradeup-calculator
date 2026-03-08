from services.search_service import search_service
from services.input_analyser_service import input_analyser_service
from services.skin_repository import skin_repository

search_file = "config/search.json"
skins_file = "data/skins.json"

def main():
	search_svc = search_service(search_file)
	skin_repo = skin_repository(skins_file)
	input_analyser_svc = input_analyser_service(skin_repo)

	search_settings = search_svc.get_search_settings()
	input_analyser_svc.analyse_input(search_settings)

if __name__ == "__main__":
	main()