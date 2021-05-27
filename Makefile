lint: flake8
	pipenv run black --check .

flake8:
	pipenv run flake8 --max-complexity 10 --count

format:
	pipenv run black .

run:
	pipenv run ./run.sh requests/test_checkbox.json
