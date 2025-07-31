# Plan

## Plan 1: Registry System for WAC and RCW Data
### Overview
Create a YAML-based registry system that catalogues Washington Administrative Code (WAC) and Revised Code of Washington (RCW) legal documents with hierarchical structure and timestamped files.

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

### Step-by-Step Instructions for AI Assistant
1. Project Structure Setup
   1. Create the directory structure: registry
   2. Ensure the workspace has the necessary Python dependencies (PyYAML, requests, beautifulsoup4)
2. Registry Data Model Design
   1. Design a YAML schema that captures:
      1. Titles: name, url, title_number
      2. Disposition: 
      3. Chapters: name, url, chapter_number, parent_title_number
      4. Sections: name, url, section_number, parent_chapter_number, parent_title_number
   2. Create separate schemas for WAC and RCW data structures
3. Web Scraping Logic for Metadata
   1. Implement scrapers to extract the hierarchical structure from:
   2. WAC main index page to get all titles
   3. Each title page to get chapters
   4. Each chapter page to get sections
   5. Do the same for RCW structure
   6. Focus on extracting metadata only (names, URLs, numbers) - not full content
4. YAML File Generation
   1. Create functions to convert scraped metadata into YAML format
   2. Implement datetime-based filename generation:
   3. Format: wac_registry_YYYYMMDD_HHMMSS.yaml
   4. Format: rcw_registry_YYYYMMDD_HHMMSS.yaml
   5. Save files to registry folder
5. Registry Management
   1. Implement functionality to:
      1. Check for existing registries
      2. Compare current structure with previous registries
      3. Only create new registry if structure has changed
   2. Add validation to ensure data integrity
6. Error Handling and Logging
   1. Add robust error handling for network requests
   2. Implement retry logic for failed requests
   3. Add comprehensive logging for debugging and monitoring

## Plan 2: HTML Content Scraper
### Overview
Create a scraper that downloads and saves the complete raw HTML content for every title (with dispositions embedded), chapter, and section identified in the registry, organizing files by legal code type and hierarchical structure.

### Step-by-Step Instructions for AI Assistant
1. Project Structure Setup
   1. Create directory structure: data/raw_html/wac/ and data/raw_html/rcw/
   2. Organize subdirectories by content type:
      1. data/raw_html/wac/titles/ (includes embedded dispositions)
      2. data/raw_html/wac/chapters/
      3. data/raw_html/wac/sections/
   3. Same structure for RCW
2. Registry Integration
   1. Build functionality to read the most recent registry YAML files
   2. Parse the registry to extract URLs that need to be scraped:
      1. Title URLs (with dispo=True parameter to include dispositions)
      2. Chapter URLs
      3. Section URLs
   3. Create categorized queues/lists for each content type
3. HTML Download Engine
   1. Implement robust HTTP client with:
      1. User-agent headers to identify as a legitimate scraper
      2. Rate limiting to avoid overwhelming the server (respect robots.txt)
         1. Should be a parameter that can be turned on and off
         2. Default is off
      3. Retry logic for failed requests
      4. Timeout handling
4. File Naming and Organization
   1. Create consistent naming convention for HTML files by type:
      1. Titles (with embedded dispositions): title_{title_number}_with_disposition.html
         1. Example: wac/titles/title_01_with_disposition.html
      2. Chapters: title_{title_number}_chapter_{chapter_number}.html
         1. Example: wac/chapters/title_01_chapter_001.html
      3. Sections: title_{title_number}_{chapter_number}_{section_number}.html
         1. Example: wac/sections/title_01_001_010.html
   2. Ensure file paths are valid and handle special characters in names
5. Title URL Modification for Disposition Inclusion
   1. For each title URL in the registry, modify to include disposition parameter:
      1. Original: https://app.leg.wa.gov/wac/default.aspx?cite=1
      2. Modified: https://app.leg.wa.gov/wac/default.aspx?cite=1&dispo=True
   2. This ensures the downloaded HTML includes both title content and embedded disposition information
6. Content Processing and Storage
   1. Download raw HTML for each URL by content type:
      1. Process titles first (with embedded dispositions)
      2. Then chapters (mid-level)
      3. Finally sections (most granular)
   2. Save complete HTML content (including headers, navigation, etc.)
   3. Implement checksum/hash verification to detect content changes
   4. Add metadata headers to files (download timestamp, source URL, content type)
7. Progress Tracking and Resume Capability
   1. Implement progress tracking to show download status by content type:
      1. Track titles (with dispositions), chapters, and sections separately
      2. Show overall progress and per-category progress
   2. Create checkpoint system to resume interrupted downloads
   3. Track failed downloads for retry attempts by category
   4. Generate summary reports of scraping results with breakdown by content type
8. Duplicate Detection and Updates
   1. Check for existing HTML files before downloading (across all content types)
   2. Compare file modification dates and content hashes
   3. Only re-download if content has changed or file is missing
   4. Maintain version history if needed for all content types
9. Error Handling and Monitoring
   1.  Handle various HTTP error codes appropriately
   2.  Log all download attempts and results with content type classification
   3.  Create alerts for systematic failures
   4.  Implement graceful degradation for partial failures
   5.  Track success/failure rates by content type (titles vs chapters vs sections)
10. Content Type Specific Handling
    1.  Titles with Dispositions: Handle title pages with dispo=True parameter to capture both title content and embedded disposition tables
    2.  Chapters: Download chapter-level content including chapter summaries
    3.  Sections: Download individual section content (the most granular level)
    4.  Ensure each content type is properly categorized and stored in the correct directory structure
11. Registry Schema Update
Update the YAML registry to reflect the simplified structure:
```
titles:
  - title_number: "01"
    name: "Administrative Procedures"
    url: "https://app.leg.wa.gov/wac/default.aspx?cite=1"
    disposition_url: "https://app.leg.wa.gov/wac/default.aspx?cite=1&dispo=True"
    chapters: [
      sections: []
    ]
```