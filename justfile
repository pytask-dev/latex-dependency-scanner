# Install all dependencies.
install:
    uv sync --all-groups

# Run tests.
test *FLAGS:
    uv run --group test pytest {{FLAGS}}

# Run tests with coverage.
test-cov *FLAGS:
    uv run --group test pytest --cov=./ --cov-report=xml {{FLAGS}}

# Run type checking.
typing:
    uv run --group typing --group test --isolated ty check src/ tests/

# Run linting.
lint:
    uvx pre-commit run -a

# Run all checks.
check: lint typing test-cov
