# WA Law Scraper

A Python package for scraping and cataloging Washington State legal codes (WAC and RCW) with a YAML-based registry system.

## Overview

The WA Law Scraper provides a comprehensive registry system for Washington Administrative Code (WAC) and Revised Code of Washington (RCW) legal documents. It creates timestamped YAML files that catalog the complete hierarchical structure of these legal codes, preserving relationships between titles, chapters, and sections.

## Features

### ✅ Registry System (Implemented)

- **YAML-based registries** with timestamped filenames
- **Hierarchical data structure** preservation (Title → Chapter → Section)
- **Web scraping engine** with configurable rate limiting
- **Command-line interface** for easy operation
- **Error handling and logging** for robust operation
- **Registry management** (save, load, list, compare)

### ✅ HTML Content Scraper (Implemented)

- **Complete HTML content downloading** for all cataloged URLs
- **Organized file storage** in `data/raw_html/` with hierarchical structure
- **Registry-based scraping** using existing URL catalogs
- **Content management utilities** (list, statistics, existence checking)
- **Incremental updates** with skip existing files option
- **Rate limiting and error handling** integrated with existing infrastructure

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hazardos-ai/wa-law-scraper.git
   cd wa-law-scraper
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

## Usage

### Command Line Interface

The package provides a comprehensive CLI for registry operations:

#### Generate Registries

Generate a WAC registry:
```bash
python -m wa_law_scraper.cli generate wac
```

Generate an RCW registry:
```bash
python -m wa_law_scraper.cli generate rcw
```

Generate both registries:
```bash
python -m wa_law_scraper.cli generate both
```

Options:
- `--rate-limit`: Enable rate limiting for web requests
- `--verbose`: Enable detailed logging
- `--data-dir`: Specify custom data directory (default: `data`)

#### List Existing Registries

List all registries:
```bash
python -m wa_law_scraper.cli list
```

List registries for specific code type:
```bash
python -m wa_law_scraper.cli list --code-type wac
```

#### Show Registry Information

Show info for latest WAC registry:
```bash
python -m wa_law_scraper.cli info --code-type wac
```

Show info for specific registry file:
```bash
python -m wa_law_scraper.cli info --file data/registry/wac_registry_20240131_143022.yaml
```

#### HTML Content Scraping

Scrape HTML content for WAC:
```bash
python -m wa_law_scraper.cli scrape-content wac
```

Scrape HTML content for RCW:
```bash
python -m wa_law_scraper.cli scrape-content rcw
```

Scrape both WAC and RCW content:
```bash
python -m wa_law_scraper.cli scrape-content both
```

Scrape with rate limiting and overwrite existing files:
```bash
python -m wa_law_scraper.cli scrape-content wac --rate-limit --overwrite
```

#### Content Management

List scraped content files:
```bash
python -m wa_law_scraper.cli list-content
```

List content for specific code type:
```bash
python -m wa_law_scraper.cli list-content --code-type wac
```

Show content statistics:
```bash
python -m wa_law_scraper.cli content-info --verbose
```

### Python API

```python
from wa_law_scraper import RegistryManager, RegistryGenerator, ContentManager, ContentScraper

# Registry operations
registry_manager = RegistryManager("data")
generator = RegistryGenerator(registry_manager, rate_limit_enabled=True)

# Generate WAC registry
wac_registry = generator.generate_wac_registry()
print(f"Generated WAC registry with {len(wac_registry.titles)} titles")

# Load existing registry
latest_wac = registry_manager.get_latest_registry("WAC")
if latest_wac:
    print(f"Latest WAC registry has {len(latest_wac.titles)} titles")

# Content scraping operations
content_manager = ContentManager("data")
content_scraper = ContentScraper(registry_manager, content_manager, rate_limit_enabled=True)

# Scrape content for latest WAC registry
success = content_scraper.scrape_registry_content("WAC", skip_existing=True)
print(f"Content scraping successful: {success}")

# Get content statistics
stats = content_manager.get_content_stats()
print(f"Total content files: {stats['total_files']}")
```

## Data Structure

### Registry File Format

Registry files are saved as YAML with the format: `{wac|rcw}_registry_YYYYMMDD_HHMMSS.yaml`

```yaml
code_type: "WAC"
created_at: "2024-01-31T14:30:22.123456"
base_url: "https://app.leg.wa.gov/wac/default.aspx"
titles:
  - title_number: "1"
    name: "Code Reviser, Office of the"
    url: "https://app.leg.wa.gov/wac/default.aspx?cite=1"
    disposition_url: "https://app.leg.wa.gov/wac/default.aspx?cite=1&dispo=true"
    chapters:
      - chapter_number: "1-04"
        name: "General provisions"
        url: "https://app.leg.wa.gov/WAC/default.aspx?cite=1-04"
        parent_title_number: "1"
        sections:
          - section_number: "1-04-010"
            name: "State Environmental Policy Act"
            url: "https://app.leg.wa.gov/WAC/default.aspx?cite=1-04-010"
            parent_chapter_number: "1-04"
            parent_title_number: "1"
```

### Directory Structure

```
data/
├── registry/
│   ├── wac_registry_20240131_143022.yaml
│   └── rcw_registry_20240131_143145.yaml
└── raw_html/
    ├── wac/
    │   ├── 01/
    │   │   ├── title_01.html
    │   │   ├── title_01_disposition.html
    │   │   ├── 01-04/
    │   │   │   ├── chapter_01-04.html
    │   │   │   ├── section_01-04-010.html
    │   │   │   └── section_01-04-020.html
    │   │   └── 01-06/
    │   │       └── ...
    │   └── 02/
    │       └── ...
    └── rcw/
        └── ... (similar structure)
```

## Legal Code Sources

- **WAC (Washington Administrative Code)**: https://app.leg.wa.gov/wac/default.aspx
- **RCW (Revised Code of Washington)**: https://app.leg.wa.gov/RCW/default.aspx

Both sources use identical site structures, allowing unified scraping logic.

## Environment Management

This project uses Pixi for environment management. Dependencies and build tasks are defined in `pyproject.toml`.

### Dependencies

- `pyyaml>=6.0.2`: YAML file processing
- `requests>=2.32.4`: HTTP requests for web scraping  
- `beautifulsoup4>=4.13.4`: HTML parsing and extraction

## Development

### Project Structure

```
src/wa_law_scraper/
├── __init__.py          # Package exports
├── models.py            # Data models and structures
├── scraper.py           # Web scraping functionality
├── registry.py          # Registry management
└── cli.py              # Command-line interface
```

### Documentation-Driven Development

This project follows Documentation-Driven Development principles:
- Features are documented before implementation
- Tests align with documented behavior
- Documentation and software versions are synchronized

## Contributing

1. Review the `.context/` folder for specifications and plans
2. Follow the existing code structure and patterns
3. Ensure changes align with the documented features
4. Test both Python API and CLI functionality

## License

[License information from LICENSE file]
