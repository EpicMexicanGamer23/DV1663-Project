start: 
	py main.py

lint: 
	py -m ruff check ./*.py && py -m ruff check ./src/*.py