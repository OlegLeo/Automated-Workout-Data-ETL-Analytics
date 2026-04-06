run:
	python3 main.py
scrape:
	python3 -m hevy_scraper.main
transform_data:
	python3 -m transform.transform_hevy
	python3 -m transform.transform_weight
	python3 -m transform.transform_nutrition
ingest_data:
	python3 -m ingest.google_sheets_ingest
pipeline: scrape transform_data ingest_data
	python3 main.py
install:
	pip3 install -r requirements.txt
clean:
	find . -name "__pycache__" -exec rm -r {} +