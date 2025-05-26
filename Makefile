# Makefile for config_manager module
# BSD 3-Clause License

PYTHON := python3
PIP := pip3
MODULE_NAME := wl_config_manager
VERSION := $(shell cat VERSION 2>/dev/null || echo "0.1.0")

# Fedora/CentOS package manager
PKG_MGR := dnf

.PHONY: help clean build test install uninstall upload-test upload-prod deps-dev deps increment-version

help:
	@echo "Available targets:"
	@echo "  clean        - Remove build artifacts"
	@echo "  build        - Build the package (auto increments version)"
	@echo "  test         - Run tests"
	@echo "  install      - Install package locally"
	@echo "  uninstall    - Remove package"
	@echo "  upload-test  - Upload to PyPI test"
	@echo "  upload-prod  - Upload to PyPI production"
	@echo "  deps-dev     - Install development dependencies"
	@echo "  deps         - Install system dependencies"
	@echo "  increment-version - Bump patch version"
	@echo "  current-version  - Show current version"

# System dependencies (Fedora/CentOS)
deps:
	sudo $(PKG_MGR) install -y python3-pip python3-wheel python3-setuptools python3-build

# Development dependencies
deps-dev: deps
	$(PIP) install --user twine pytest pytest-cov wl_version_manager

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Version management
increment-version:
	@if [ ! -f VERSION ]; then wl_version_manager init; fi
	wl_version_manager patch

current-version:
	@if [ ! -f VERSION ]; then echo "0.1.0"; else cat VERSION; fi

# Build the package (auto increment version)
build: clean increment-version
	$(PYTHON) setup.py sdist

# Run tests
test:
	$(PYTHON) -m pytest tests/ -v

# Test with coverage
test-cov:
	$(PYTHON) -m pytest tests/ -v --cov=$(MODULE_NAME) --cov-report=html

# Install package locally
install: build
	$(PIP) install --user dist/$(MODULE_NAME)-$(VERSION).tar.gz 

# Uninstall package
uninstall:
	$(PIP) uninstall -y $(MODULE_NAME)

# Install in development mode
install-dev:
	$(PIP) install --user -e .

# Upload to PyPI test
upload-test: build
	$(PYTHON) -m twine upload --repository testpypi dist/*

# Upload to PyPI production
upload-prod: build
	$(PYTHON) -m twine upload dist/*

# Pipenv workflow targets
pipenv-install:
	pipenv install $(MODULE_NAME)==$(VERSION)

pipenv-install-test:
	pipenv install -i https://test.pypi.org/simple/ $(MODULE_NAME)==$(VERSION)

pipenv-remove:
	pipenv uninstall $(MODULE_NAME)

pipenv-shell:
	pipenv shell

# Development workflow
dev-setup: deps-dev install-dev

# Full test workflow
test-all: test

# Release workflow
release-test: test-all upload-test

release-prod: test-all upload-prod

# Quick check
check: test

# Show package info
info:
	@echo "Package: $(MODULE_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Pip: $(shell $(PIP) --version)"