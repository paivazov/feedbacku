.DEFAULT_GOAL := start


YAML_FILES := -f ./docker-compose.yml

ifneq ($(wildcard $(THIS_DIR)/.env.local), )
	EXTRA_ENV_FILE := --env-file='$(THIS_DIR)/.env.local'
endif

CELERY=celery -A FeedbackU
CELERY_FLAG :=
ifeq ($(OS),Windows_NT)
	CELERY_FLAG:= -P gevent
endif

DOCKER=docker-compose $(YAML_FILES) $(EXTRA_ENV_FILE)

RUNNER=
BLACK=black --skip-string-normalization --line-length 79 --target-version py310

.PHONY: up format typecheck format_check flake8 check format start

start:
	make -j 2 up celery

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
	 python manage.py check

format:
	$(RUNNER) python -m isort . --only-sections
	$(RUNNER) $(BLACK) .


.PHONY: celery celery-worker celery-beat

celery:
	make -j 2 celery-worker celery-beat

celery-worker:
	$(RUNNER) $(CELERY) worker --loglevel=INFO $(CELERY_FLAG)

# Note. You must run celery-beat concurrently with celery-worker
celery-beat:
	$(RUNNER) $(CELERY) beat -l INFO -s ./var/celerybeat-scedule
