lint: flake8
	poetry run black --check .

flake8:
	poetry run flake8 --max-complexity 10 --count

format:
	poetry run isort .
	poetry run black .

run:
	poetry run ./run.sh requests/test_checkbox.json

test:
	poetry run ./scripts/run_tests.sh
