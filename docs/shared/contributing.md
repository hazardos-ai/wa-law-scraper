# Contributing

We welcome contributions to the D3 Project Template! This guide will help you get started.

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/d3-project-template.git
   cd d3-project-template
   ```

2. **Install development dependencies:**
   ```bash
   pixi install --all-features
   ```

3. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Standards

### Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use type hints where possible

### Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting
- Aim for high test coverage

```bash
# Run tests
pixi run pytest

# Run tests with coverage
pixi run pytest --cov=d3_project_template
```

### Documentation

- Update documentation for any new features
- Include docstrings for all public functions and classes
- Add examples where appropriate

## Submitting Changes

1. **Ensure your code passes all checks:**
   ```bash
   pixi run pytest
   pixi run black --check .
   pixi run isort --check-only .
   ```

2. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

3. **Push to your fork and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Review Process

1. All submissions require review
2. Maintainers will review your pull request
3. Address any feedback promptly
4. Once approved, your changes will be merged

## Reporting Issues

- Use the GitHub issue tracker
- Provide detailed reproduction steps
- Include system information and error messages
- Check existing issues before creating new ones

## Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Focus on constructive feedback
- Follow our code of conduct
