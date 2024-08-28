# Define the Python interpreter
PYTHON := python3

# Define the virtual environment directory
VENV := venv

# Define the requirements files
REQUIREMENTS := requirements.txt

# Create a virtual environment
$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)

# Install project dependencies
install: $(VENV)/bin/activate $(REQUIREMENTS)
	$(VENV)/bin/pip install -r $(REQUIREMENTS)
	$(VENV)/bin/playwright install

# Run the application
run:
	cd niffler_app/
	bash docker-compose-dev.sh


lint:
	flake8 --max-line-length=120 conftest.py tests niffler_tests

fmt:
	isort --profile black conftest.py tests niffler_tests
	black --line-length=120 conftest.py tests niffler_tests

# Run tests
test:
	pytest tests

test-ui:
	pytest tests/ui --browser chromium

test-ui-head:
	pytest tests/ui --headed --browser chromium

# Generate tests using playwright codegen
codegen:
	playwright codegen http://frontend.niffler.dc