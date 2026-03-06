from search_settings import search_settings_service

search_file = "search.json"

def main():
	search_service = search_settings_service(search_file)

	print(search_service.get_search_settings())

if __name__ == '__main__':
	main()