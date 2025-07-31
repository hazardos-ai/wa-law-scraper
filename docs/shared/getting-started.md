# Getting Started

## Installation

### Prerequisites

- Python >= 3.11
- [Pixi](https://pixi.sh/) package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hazardos-ai/d3-project-template.git
   cd d3-project-template
   ```

2. **Install dependencies:**
   ```bash
   pixi install
   ```

3. **Verify installation:**
   ```bash
   pixi run python -c "import d3_project_template; print('Installation successful!')"
   ```

## Development Environment

### Setting up for development

1. **Install development dependencies:**
   ```bash
   pixi install --all-features
   ```

2. **Run tests:**
   ```bash
   pixi run pytest
   ```

3. **Build documentation:**
   
   For MkDocs:
   ```bash
   pixi run mkdocs serve
   ```
   
   For JupyterBook:
   ```bash
   pixi run jupyter-book build docs/jupyter-book/
   ```

## Next Steps

- Explore the [API Reference](api/index.md)
- Check out [Examples](examples/index.md)
- Read the [Contributing Guide](contributing.md)
