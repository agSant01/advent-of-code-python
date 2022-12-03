check:
	@echo "\n> Black formatter:"
	black --diff --color --preview --line-length 89 .
	@echo "" 
	@echo "\n> autoflake: remove unused vars and imports"
	autoflake --exclude */venv/* --recursive --remove-unused-variables --remove-all-unused-imports .
	@echo ""

	@echo "\n> isort: ordering imports"
	isort --profile=black --check --diff .
	@echo ""


lint:
	black --preview --line-length 89 .
	autoflake --exclude */venv/* --recursive --in-place --remove-unused-variables --remove-all-unused-imports .
	isort --profile=black .