start: 
	py main.py

lint: 
	py -m ruff check . && py -m ruff check ./src/*.py