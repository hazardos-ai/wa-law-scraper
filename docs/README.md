# Documentation Setup

This directory is configured to work with both **MkDocs** and **JupyterBook** documentation systems, providing flexibility for different documentation workflows.

## Directory Structure

```
docs/
├── README.md                    # This file
├── index.md                     # Main documentation index (symlinked to shared)
├── getting-started.md          # Getting started guide (includes shared content)
├── shared/                     # Shared content between both systems
│   ├── getting-started.md      # Main getting started content
│   ├── api/
│   │   └── index.md           # API reference
│   ├── examples/
│   │   └── index.md           # Examples and tutorials
│   ├── notebooks/             # Jupyter notebooks
│   │   ├── tutorial.ipynb     # Basic tutorial
│   │   ├── advanced.ipynb     # Advanced features
│   │   └── workflow.ipynb     # Data analysis workflow
│   └── contributing.md        # Contributing guidelines
├── mkdocs/                     # MkDocs-specific configuration
│   └── mkdocs.yml             # MkDocs configuration
└── jupyter-book/              # JupyterBook-specific configuration
    ├── _config.yml            # JupyterBook configuration
    └── _toc.yml               # Table of contents
```

## Using MkDocs

MkDocs is great for traditional documentation websites with Markdown content.

### Install Dependencies

```bash
pixi install --feature docs
```

### Serve Documentation Locally

```bash
pixi run docs-mkdocs-serve
```

### Build Documentation

```bash
pixi run docs-mkdocs-build
```

The built site will be available in `docs/site/`.

## Using JupyterBook

JupyterBook is perfect for documentation that includes executable notebooks and scientific content.

### Build Documentation

```bash
pixi run docs-jupyter-book-build
```

### Serve and Open Documentation

```bash
pixi run docs-jupyter-book-serve
```

The built documentation will be available in `docs/jupyter-book/_build/`.

## Shared Content Strategy

Both documentation systems use the content in the `shared/` directory:

- **MkDocs**: References shared content using relative paths and include directives
- **JupyterBook**: Uses the shared content directly via the table of contents configuration

### Adding New Content

1. **Markdown files**: Add to `shared/` directory
2. **Jupyter notebooks**: Add to `shared/notebooks/` directory
3. **Update configurations**:
   - Add to `mkdocs/mkdocs.yml` navigation
   - Add to `jupyter-book/_toc.yml` chapters/sections

### Content Guidelines

- Use relative links within the shared content
- Ensure notebook outputs are cleared before committing
- Test content with both documentation systems
- Use consistent heading levels across documents

## Available Commands

| Command | Description |
|---------|-------------|
| `pixi run docs-mkdocs-serve` | Serve MkDocs documentation locally |
| `pixi run docs-mkdocs-build` | Build MkDocs documentation |
| `pixi run docs-jupyter-book-build` | Build JupyterBook documentation |
| `pixi run docs-jupyter-book-serve` | Build and open JupyterBook documentation |
| `pixi run docs-clean` | Clean all built documentation |

## Features

### MkDocs Features
- Material theme with dark/light mode toggle
- Search functionality
- Code syntax highlighting
- API documentation with mkdocstrings
- GitHub integration

### JupyterBook Features
- Executable notebooks
- Interactive content
- Scientific publishing features
- Sphinx-based extensibility
- Multiple output formats (HTML, PDF, etc.)

## CI/CD Integration

Both documentation systems can be integrated into CI/CD pipelines:

- **GitHub Pages**: Both MkDocs and JupyterBook can deploy to GitHub Pages
- **Netlify/Vercel**: Both systems generate static sites compatible with these platforms
- **Documentation hosting**: Services like Read the Docs support both systems

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Run `pixi install --feature docs`
2. **Build errors**: Check that all referenced files exist in the shared directory
3. **Notebook execution errors**: Ensure notebooks run successfully before building
4. **Link errors**: Use relative paths and test with both systems

### Getting Help

- Check the [MkDocs documentation](https://www.mkdocs.org/)
- Review the [JupyterBook documentation](https://jupyterbook.org/)
- Open an issue in the project repository
