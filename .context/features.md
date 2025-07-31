# Features

## ✅ Registry System (COMPLETED)

A YAML-based registry system that catalogs WAC and RCW legal document structure with the following features:

### Core Features
1. **YAML Registry Files**: Saves information to timestamped files (one for WAC and one for RCW) using datetime format and saved to the `data/registry/` folder:
   - Format: `wac_registry_YYYYMMDD_HHMMSS.yaml` and `rcw_registry_YYYYMMDD_HHMMSS.yaml`
   - Contains complete hierarchical structure: Title → Chapter → Section
   - Preserves all URLs and metadata for future content extraction

2. **Hierarchical Data Structure**:
   - **Titles**: name, url, title number, and disposition URL
   - **Chapters**: name, url, chapter number, and parent title reference
   - **Sections**: name, url, section number, and parent chapter/title references

3. **Web Scraping Engine**: 
   - Configurable rate limiting (can be enabled/disabled)
   - Error handling and retry logic
   - Extracts metadata structure from both WAC and RCW websites
   - Maintains URL relationships for complete document graph

4. **Registry Management**:
   - Load and save registry files
   - List existing registries with timestamps
   - Get latest registry for a code type
   - Data integrity validation

5. **Command-Line Interface**:
   - Generate new registries: `python -m wa_law_scraper.cli generate {wac|rcw|both}`
   - List existing registries: `python -m wa_law_scraper.cli list`
   - Show registry information: `python -m wa_law_scraper.cli info`
   - Optional rate limiting: `--rate-limit` flag
   - Verbose logging: `--verbose` flag

### Implementation Details
- **Package Structure**: Modular design with separate concerns
  - `models.py`: Data structures with YAML serialization
  - `scraper.py`: Web scraping functionality
  - `registry.py`: Registry management and generation
  - `cli.py`: Command-line interface
- **Dependencies**: Uses existing project dependencies (PyYAML, requests, beautifulsoup4)
- **Error Handling**: Comprehensive logging and graceful failure handling
- **Data Integrity**: Maintains parent-child relationships throughout hierarchy

## 🔄 HTML Content Scraper (COMPLETED ✅)

An HTML content scraper that downloads and saves the complete raw HTML content for every title (with dispositions embedded), chapter, and section identified in the registry, organizing files by legal code type and hierarchical structure.

### Core Features

1. **HTML Content Storage**: Downloads complete HTML content for all URLs cataloged in registries
   - Organized file structure: `data/raw_html/{code_type}/{title_number}/{chapter_number}/`
   - Systematic naming: `title_{number}.html`, `chapter_{number}.html`, `section_{number}.html`
   - Special handling for disposition content: `title_{number}_disposition.html`

2. **Registry-Based Scraping**: Uses existing registries as the source of URLs to scrape
   - Leverages the completed registry system for comprehensive coverage
   - Maintains hierarchical relationships between content files
   - Supports both WAC and RCW content types

3. **Content Management**:
   - `ContentManager` class for organized file storage and retrieval
   - Content existence checking to avoid duplicate downloads
   - File listing and statistics for monitoring scraped content
   - Structured directory creation and management

4. **Advanced Scraping Features**:
   - Rate limiting support (reuses existing scraper infrastructure)
   - Fake user agent support for Cloudflare bypass
   - Error handling and retry logic
   - Skip existing files option for incremental updates
   - Overwrite mode for fresh content downloads

5. **Command-Line Interface Extensions**:
   - `scrape-content {wac|rcw|both}`: Main content scraping command
   - `list-content`: List all scraped content files
   - `content-info`: Show statistics about scraped content
   - All commands support filtering by code type and verbose output

### Implementation Details
- **Package Structure**: Extended existing architecture with minimal changes
  - `ContentManager`: File organization and storage management  
  - `ContentScraper`: Registry-based content scraping orchestration
  - Extended `LegalCodeScraper`: Added `scrape_html_content()` method
  - Enhanced CLI: New subcommands integrated with existing interface
- **Dependencies**: Uses existing project dependencies (no new requirements)
- **Error Handling**: Comprehensive logging and graceful failure handling
- **File Organization**: Hierarchical structure preserving legal code relationships

### Usage Examples

```bash
# Scrape all WAC content
python -m wa_law_scraper.cli scrape-content wac --rate-limit --verbose

# Scrape both WAC and RCW content
python -m wa_law_scraper.cli scrape-content both --overwrite

# List scraped content
python -m wa_law_scraper.cli list-content --code-type wac

# Show content statistics  
python -m wa_law_scraper.cli content-info --verbose
```

### File Structure Example
```
data/raw_html/
├── wac/
│   ├── 01/
│   │   ├── title_01.html                    # Main title page
│   │   ├── title_01_disposition.html        # Disposition page  
│   │   ├── 01-04/
│   │   │   ├── chapter_01-04.html          # Chapter page
│   │   │   ├── section_01-04-010.html      # Section pages
│   │   │   └── section_01-04-020.html
│   │   └── 01-06/
│   │       └── ...
│   └── 02/
│       └── ...
└── rcw/
    └── ... (similar structure)
```