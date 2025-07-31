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

## 🔄 HTML Content Scraper (PLANNED)

A scraper that extracts the raw HTML for every title, chapter, and section and saves the output to the `data/raw_html/` folder. This feature will be implemented in a future phase, building upon the registry system to:

- Download complete HTML content for all URLs captured in registries
- Organize files by legal code type and hierarchical structure
- Include disposition data for titles
- Implement content change detection and versioning