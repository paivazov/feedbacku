.PHONY: up format typecheck format_check flake8 check format


YAML_FILES := -f ./docker-compose.yml


ifneq ($(wildcard $(THIS_DIR)/.env.local), )
	EXTRA_ENV_FILE := --env-file='$(THIS_DIR)/.env.local'
endif

DOCKER=docker-compose $(YAML_FILES) $(EXTRA_ENV_FILE)

RUNNER=
BLACK=black --skip-string-normalization --line-length 79 --target-version py310

env:
	cp .env.local.sample .env.local

up:
	$(DOCKER) up

typecheck:
	python -m mypy --pretty --show-error-codes .

format_check:
	$(RUNNER) python -m isort . --only-sections --quiet --check-only --diff \
              --line-length 79
	$(RUNNER) $(BLACK) --fast --check .

flake8:
	$(RUNNER) flake8 .

check: flake8 typecheck format_check


format:
	$(RUNNER) python -m isort . --only-sections
	$(RUNNER) $(BLACK) .
