DIR=.

check:
	@echo "\n> Black formatter:"
	black --diff --color --preview --line-length 89 $(DIR)
	@echo "" 
	@echo "\n> autoflake: remove unused vars and imports"
	autoflake --exclude */venv/* --recursive --remove-unused-variables --remove-all-unused-imports $(DIR)
	@echo ""

	@echo "\n> isort: ordering imports"
	isort --profile=black --check --diff $(DIR)
	@echo ""


lint:
	black --preview --line-length 89 $(DIR)
	autoflake --exclude */venv/* --recursive --in-place --remove-unused-variables --remove-all-unused-imports $(DIR)
	isort --profile=black $(DIR)