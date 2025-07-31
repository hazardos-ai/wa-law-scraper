# D3 Project Template Documentation

Welcome to the D3 Project Template documentation. This project provides a foundational structure for data-driven development projects.

## Overview

This template includes:

- Modern Python project structure with `pyproject.toml`
- Pixi-based dependency management
- Comprehensive documentation setup
- Testing framework integration
- Development best practices

## Quick Start

```bash
# Clone the repository
git clone https://github.com/hazardos-ai/d3-project-template.git
cd d3-project-template

# Install dependencies with pixi
pixi install

# Run the project
pixi run python -m d3_project_template
```

## Documentation

This documentation is built with both MkDocs and JupyterBook to provide flexibility in documentation workflows:

- **MkDocs**: Great for traditional documentation websites with markdown
- **JupyterBook**: Perfect for documentation that includes executable notebooks and scientific content

## Project Structure

```
d3-project-template/
├── src/
│   └── d3_project_template/
├── tests/
├── docs/
│   ├── mkdocs/          # MkDocs specific files
│   ├── jupyter-book/    # JupyterBook specific files
│   └── shared/          # Shared content between both systems
├── context_eng/
└── pyproject.toml
```

## Navigation

- [Getting Started](getting-started.md)
- [API Reference](api/index.md)
- [Examples](examples/index.md)
- [Contributing](contributing.md)
