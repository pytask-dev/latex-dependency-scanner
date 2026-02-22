# Install all dependencies.
install:
    uv sync --all-groups

# Run tests.
test *FLAGS:
    uv run --group test pytest {{FLAGS}}

# Run unit tests and doctests with coverage.
test-unit *FLAGS:
    uv run --group test pytest src tests -m "unit or (not integration and not end_to_end)" --cov=./ --cov-report=xml {{FLAGS}}

# Run end-to-end tests with coverage.
test-end-to-end *FLAGS:
    uv run --group test pytest src tests -m end_to_end --cov=./ --cov-report=xml {{FLAGS}}

# Run type checking.
typing:
    uv run --group typing --group test --isolated ty check src/ tests/

# Run linting.
lint:
    uvx pre-commit run -a

# Run all checks.
check: lint typing test-unit test-end-to-end
