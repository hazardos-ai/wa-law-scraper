# Specifications

## Goal

Extract all title, chapter, and section while maintaining knowledge connections for creating both a relational and graph database implementation. After this, APIs will be created for structuring and validating data input and output.

## State of Washington legal code information

There are 2 types of Washington State laws:
- Washington Administrative Code (WAC) are regulations of executive branch agencies are issued by authority of statutes. Like legislation and the Constitution, regulations are a source of primary law in Washington State. The WAC codifies the regulations and arranges them by subject or agency.
  - Base URL: https://app.leg.wa.gov/wac/default.aspx
- The Revised Code of Washington (RCW) is the compilation of all permanent laws now in force. It is a collection of Session Laws (enacted by the Legislature, and signed by the Governor, or enacted via the initiative process), arranged by topic, with amendments added and repealed laws removed. It does not include temporary laws such as appropriations acts.
  - Base URL: https://app.leg.wa.gov/RCW/default.aspx
The two types of legal codes have different base urls but have identical site structure

## Implementation Status

### Registry System ✅ COMPLETED
A YAML-based registry system has been implemented that catalogs Washington Administrative Code (WAC) and Revised Code of Washington (RCW) legal documents with hierarchical structure and timestamped files.

**Core Components:**
- **Data Models**: Hierarchical structure preserving Title → Chapter → Section relationships
- **Web Scraper**: Configurable scraper with error handling and rate limiting
- **Registry Manager**: YAML file management with datetime-based filenames
- **CLI Interface**: Command-line tool for registry generation and management

**File Structure:**
- Registry files saved to `data/registry/` with format: `{wac|rcw}_registry_YYYYMMDD_HHMMSS.yaml`
- Each registry captures complete hierarchical structure with URLs and metadata
- Disposition URLs included for titles to enable comprehensive data extraction

### HTML Content Scraper ✅ COMPLETED

A comprehensive HTML content scraper has been implemented that downloads and stores complete HTML content for all cataloged URLs.

**Core Components:**
- **ContentManager**: Manages organized HTML file storage in `data/raw_html/` with hierarchical structure
- **ContentScraper**: Registry-based content scraping that uses existing registries as URL sources
- **Enhanced LegalCodeScraper**: Extended with HTML content downloading capabilities
- **CLI Extensions**: New commands for content operations integrated with existing interface

**File Organization:**
- Content stored in hierarchical structure: `data/raw_html/{code_type}/{title_number}/{chapter_number}/`
- Systematic naming: `title_{number}.html`, `chapter_{number}.html`, `section_{number}.html`
- Special handling for disposition content: `title_{number}_disposition.html`
- Maintains parent-child relationships throughout legal code hierarchy

**Features:**
- Registry-based scraping using existing URL catalogs
- Content existence checking to avoid duplicate downloads  
- Rate limiting and fake user agent support (reuses existing infrastructure)
- Skip existing files option for incremental updates
- Overwrite mode for fresh content downloads
- Comprehensive error handling and logging
- Content statistics and file management utilities

**CLI Commands:**
```bash
# Content scraping
python -m wa_law_scraper.cli scrape-content {wac|rcw|both} [--rate-limit] [--overwrite]

# Content management  
python -m wa_law_scraper.cli list-content [--code-type {wac|rcw}]
python -m wa_law_scraper.cli content-info [--code-type {wac|rcw}] [--verbose]
```

**Data Schema:**
```yaml
# Registry structure remains unchanged, content files organized as:
data/raw_html/
├── wac/01/title_01.html                    # Title pages
├── wac/01/title_01_disposition.html        # Disposition pages  
├── wac/01/01-04/chapter_01-04.html         # Chapter pages
└── wac/01/01-04/section_01-04-010.html     # Section pages
```
