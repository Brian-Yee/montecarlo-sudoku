all:
	python main.py data/sudoku/test.txt

test:
	pylint *.py

clean:
	black .
