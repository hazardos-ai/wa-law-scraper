# Plan

## ✅ Plan 1: Registry System for WAC and RCW Data (COMPLETED)

### Overview
Create a YAML-based registry system that catalogues Washington Administrative Code (WAC) and Revised Code of Washington (RCW) legal documents with hierarchical structure and timestamped files.

### Implementation Status: COMPLETED ✅

The registry system has been successfully implemented with all planned features:

1. **Project Structure Setup** ✅
   - Created directory structure: `data/registry/`
   - Workspace has the necessary Python dependencies (PyYAML, requests, beautifulsoup4)

2. **Registry Data Model Design** ✅
   - Designed YAML schema that captures:
     - Titles: name, url, title_number, disposition_url
     - Chapters: name, url, chapter_number, parent_title_number
     - Sections: name, url, section_number, parent_chapter_number, parent_title_number
   - Created unified schema for both WAC and RCW data structures

3. **Web Scraping Logic for Metadata** ✅
   - Implemented scrapers to extract hierarchical structure from:
     - WAC/RCW main index pages to get all titles
     - Each title page to get chapters
     - Each chapter page to get sections
   - Focus on extracting metadata only (names, URLs, numbers) - not full content

4. **YAML File Generation** ✅
   - Created functions to convert scraped metadata into YAML format
   - Implemented datetime-based filename generation:
     - Format: `wac_registry_YYYYMMDD_HHMMSS.yaml`
     - Format: `rcw_registry_YYYYMMDD_HHMMSS.yaml`
   - Save files to registry folder

5. **Registry Management** ✅
   - Implemented functionality to:
     - Check for existing registries
     - Compare current structure with previous registries
     - Load and save registry files
   - Added validation to ensure data integrity

6. **Error Handling and Logging** ✅
   - Added robust error handling for network requests
   - Implemented retry logic for failed requests
   - Added comprehensive logging for debugging and monitoring

7. **Command-Line Interface** ✅
   - Generate registries: `python -m wa_law_scraper.cli generate {wac|rcw|both}`
   - List registries: `python -m wa_law_scraper.cli list`
   - Show registry info: `python -m wa_law_scraper.cli info`
   - Optional rate limiting and verbose logging

### Examples
Below is an example of real urls that can help you with understanding HTML structure:
1. Main site: https://app.leg.wa.gov/wac/default.aspx
2. Title:
   1. name: Code Reviser, Office of the
   2. title_number: 1
   3. url: https://app.leg.wa.gov/wac/default.aspx?dispo=true&cite=1
      1. Note: `dispo=true` shows dispositions about the title. You may need to parse this parameter into the url, so we can retrieve all the necessary information later.
3. Chapters
   1. Example 1
      1. name: General provisions.
      2. chapter_number: 1-04
      3. url: http://app.leg.wa.gov/WAC/default.aspx?cite=1-04
      4. Sections
         1. name: State Environmental Policy Act.
         2. section_number: 1-04-010
         3. url: https://app.leg.wa.gov/WAC/default.aspx?cite=1-04-010
   2. Example 2
      1. name: Public records.
      2. chapter_number: 1-06
      3. url: http://app.leg.wa.gov/WAC/default.aspx?cite=1-06
   3. Example 3
      1. name: Rule making.
      2. chapter_number: 1-21
      3. url: http://app.leg.wa.gov/WAC/default.aspx?cite=1-21

## ✅ Plan 2: HTML Content Scraper (COMPLETED)

### Overview
Create a scraper that downloads and saves the complete raw HTML content for every title (with dispositions embedded), chapter, and section identified in the registry, organizing files by legal code type and hierarchical structure.

### Implementation Status: COMPLETED ✅

The HTML Content Scraper has been successfully implemented with all planned features:

1. **Content Storage Architecture** ✅
   - Created organized directory structure: `data/raw_html/{code_type}/{title_number}/{chapter_number}/`
   - Implemented systematic file naming conventions
   - Added support for disposition content storage

2. **Content Management System** ✅
   - Implemented `ContentManager` class for file organization and management
   - Added content existence checking and statistics gathering
   - Created content listing and filtering capabilities

3. **Registry-Based Scraping** ✅
   - Implemented `ContentScraper` class that uses existing registries as URL sources
   - Added complete content scraping for titles, chapters, and sections
   - Integrated disposition URL handling for comprehensive title content

4. **Enhanced Web Scraping** ✅
   - Extended `LegalCodeScraper` with `scrape_html_content()` method
   - Reused existing rate limiting and error handling infrastructure
   - Maintained fake user agent support for Cloudflare bypass

5. **Command-Line Interface Extensions** ✅
   - Added `scrape-content` command for initiating content downloads
   - Added `list-content` command for content file management
   - Added `content-info` command for scraping statistics
   - Integrated all features with existing CLI architecture

6. **Configuration and Flexibility** ✅
   - Added skip existing files option for incremental updates
   - Added overwrite mode for fresh content downloads
   - Maintained all existing rate limiting and user agent options
   - Added comprehensive error handling and logging

### Examples
Content scraping can be performed using the registry data:
```bash
# Scrape all content for WAC using latest registry
python -m wa_law_scraper.cli scrape-content wac --rate-limit --verbose

# Scrape both WAC and RCW content with overwrite
python -m wa_law_scraper.cli scrape-content both --overwrite

# List all scraped content files
python -m wa_law_scraper.cli list-content

# Show content statistics
python -m wa_law_scraper.cli content-info --verbose
```

### Content Organization Schema (IMPLEMENTED)
The content is organized in a hierarchical structure that mirrors the legal code organization:
```
data/raw_html/
├── wac/                                   # Washington Administrative Code
│   ├── 01/                               # Title 01
│   │   ├── title_01.html                 # Title main page
│   │   ├── title_01_disposition.html     # Title disposition page
│   │   ├── 01-04/                        # Chapter 01-04
│   │   │   ├── chapter_01-04.html        # Chapter main page
│   │   │   ├── section_01-04-010.html    # Individual sections
│   │   │   └── section_01-04-020.html
│   │   └── 01-06/                        # Chapter 01-06
│   │       └── ...
│   └── 02/                               # Title 02
│       └── ...
└── rcw/                                   # Revised Code of Washington
    └── ... (similar structure)
```

### Registry Schema (IMPLEMENTED)
The registry system uses the following structure:
```yaml
code_type: "WAC" | "RCW"
created_at: ISO datetime
base_url: string
titles:
  - title_number: "01"
    name: "Administrative Procedures"
    url: "https://app.leg.wa.gov/wac/default.aspx?cite=1"
    disposition_url: "https://app.leg.wa.gov/wac/default.aspx?cite=1&dispo=True"
    chapters:
      - chapter_number: "1-04"
        name: "General provisions"
        url: "http://app.leg.wa.gov/WAC/default.aspx?cite=1-04"
        parent_title_number: "1"
        sections:
          - section_number: "1-04-010"
            name: "State Environmental Policy Act"
            url: "https://app.leg.wa.gov/WAC/default.aspx?cite=1-04-010"
            parent_chapter_number: "1-04"
            parent_title_number: "1"
```