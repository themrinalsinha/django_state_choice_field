default: dist

.PHONY: dist
dist: ## builds source and wheel package
	@pip install -r requirements_dev.txt
	@python -m build

.PHONY: clean
clean: ## removes build files
	@rm -rf dist/ django_state_choice_field.egg-info/ .eggs/ build/

.PHONY: install
install: ## installs package
	@python -m pip install -e .
	@$(MAKE) clean

uninstall:
	@python -m pip uninstall django_state_choice_field -y

.PHONY: test_upload
test_upload: ## uploads package to test server
	@$(MAKE) dist
	@pip install twine -U
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: pypi_upload
pypi_upload: ## uploads package to pypi
	@$(MAKE) dist
	@pip install twine -U
	@twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
