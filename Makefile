run:
	python3 main.py
scrape:
	python3 -m hevy_scraper.run
transform_data:
	python3 -m transform.transform
ingest_data:
	python3 -m ingest.google_sheets_ingest
install:
	pip3 install -r requirements.txt
clean:
	find . -name "__pycache__" -exec rm -r {} +