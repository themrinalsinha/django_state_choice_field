default: dist

.PHONY: dist
dist: ## builds source and wheel package
	@pip install -r requirements_dev.txt
	@python -m build

.PHONY: clean
clean: ## removes build files
	@rm -rf dist/ dj_enum.egg-info/ .eggs/ build/

.PHONY: install
install: ## installs package
	@python -m pip install -e .
	@$(MAKE) clean

uninstall:
	@python -m pip uninstall dj_enum -y

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
