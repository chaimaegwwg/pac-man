run:
	python pac_man.py
debug:
	python -m pdb main.py

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . 
	mypy . --strict
clean:
	rm -rf __pycache__
