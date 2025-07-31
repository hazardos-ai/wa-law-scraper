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

## 🔄 Plan 2: HTML Content Scraper

### Overview
Create a scraper that downloads and saves the complete raw HTML content for every title (with dispositions embedded), chapter, and section identified in the registry, organizing files by legal code type and hierarchical structure.

This plan will be implemented in a future phase, building upon the completed registry system. The registry provides the foundation by cataloging all URLs and maintaining the hierarchical structure needed for organized content extraction.

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