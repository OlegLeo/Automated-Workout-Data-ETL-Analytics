run:
	python3 main.py
scrape:
	python3 -m hevy_scraper.run
transform_data:
	python3 -m transform.transform
install:
	pip3 install -r requirements.txt
clean:
	find . -name "__pycache__" -exec rm -r {} +