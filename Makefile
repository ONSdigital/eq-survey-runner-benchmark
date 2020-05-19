lint:
	pipenv run flake8 --max-complexity 10 --count

run:
	pipenv run ./run.sh requests/census_household_gb_eng.json
