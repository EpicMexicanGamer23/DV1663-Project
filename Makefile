start: 
	py main.py

lint: 
	py -m ruff check ./*.py && py -m ruff check ./src/*.py

lint_fix: 
	py -m ruff check ./*.py --fix && py -m ruff check ./src/*.py --fix