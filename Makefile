# Define a Makefile for Python project tasks

# Running tests with coverage
test:
	pytest --cov=app --cov-report=term --cov-report=html

# Linting code with pylint
lint:
	pylint app

# Formatting code with black
format:
	black .

# Cleaning up Python cache files
clean:
	find . -name "*.pyc" -delete

# Combined target to run lint, format, and test
perfect: format lint test