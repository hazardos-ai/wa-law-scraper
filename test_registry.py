#!/usr/bin/env python3
"""
Manual test script to verify the registry system works with a small subset of data.
This script tests scraping a few titles to validate the implementation without 
doing a full scrape that could take a very long time.
"""

import sys
import logging
from pathlib import Path

# Add src to path to import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from wa_law_scraper import RegistryManager, RegistryGenerator, LegalCodeScraper

def test_scraper_basic():
    """Test basic scraper functionality."""
    print("Testing basic scraper functionality...")
    
    scraper = LegalCodeScraper(rate_limit_enabled=False)
    
    # Test WAC main page
    wac_base_url = "https://app.leg.wa.gov/wac/default.aspx"
    titles = scraper.scrape_titles(wac_base_url, "WAC")
    
    if titles:
        print(f"✓ Successfully scraped {len(titles)} WAC titles")
        print(f"  First few titles:")
        for title in titles[:3]:
            print(f"    {title.title_number}: {title.name}")
            print(f"      URL: {title.url}")
            print(f"      Disposition URL: {title.disposition_url}")
    else:
        print("✗ Failed to scrape WAC titles")
        return False
    
    # Test RCW main page
    rcw_base_url = "https://app.leg.wa.gov/RCW/default.aspx"
    rcw_titles = scraper.scrape_titles(rcw_base_url, "RCW")
    
    if rcw_titles:
        print(f"✓ Successfully scraped {len(rcw_titles)} RCW titles")
        print(f"  First few titles:")
        for title in rcw_titles[:3]:
            print(f"    {title.title_number}: {title.name}")
    else:
        print("✗ Failed to scrape RCW titles")
        return False
    
    return True

def test_registry_system():
    """Test the registry management system."""
    print("\nTesting registry system...")
    
    # Create a test registry with mock data
    from wa_law_scraper.scripts.models import LegalCodeRegistry, Title, Chapter, Section
    from datetime import datetime
    
    # Create test data
    test_section = Section(
        name="Test section",
        url="https://test.example.com/section",
        section_number="1-04-010",
        parent_chapter_number="1-04",
        parent_title_number="1"
    )
    
    test_chapter = Chapter(
        name="Test chapter",
        url="https://test.example.com/chapter",
        chapter_number="1-04",
        parent_title_number="1",
        sections=[test_section]
    )
    
    test_title = Title(
        name="Test title",
        url="https://test.example.com/title",
        title_number="1",
        disposition_url="https://test.example.com/title?dispo=true",
        chapters=[test_chapter]
    )
    
    test_registry = LegalCodeRegistry(
        code_type="TEST",
        created_at=datetime.now(),
        base_url="https://test.example.com",
        titles=[test_title]
    )
    
    # Test registry manager
    registry_manager = RegistryManager("test_data")
    
    try:
        # Save test registry
        filepath = registry_manager.save_registry(test_registry)
        print(f"✓ Successfully saved test registry to: {filepath}")
        
        # Load test registry
        loaded_registry = registry_manager.load_registry(filepath)
        if loaded_registry:
            print(f"✓ Successfully loaded registry")
            print(f"  Code type: {loaded_registry.code_type}")
            print(f"  Titles: {len(loaded_registry.titles)}")
            print(f"  Chapters: {len(loaded_registry.titles[0].chapters)}")
            print(f"  Sections: {len(loaded_registry.titles[0].chapters[0].sections)}")
        else:
            print("✗ Failed to load registry")
            return False
        
        # Test listing
        registries = registry_manager.list_registries()
        print(f"✓ Found {len(registries)} registry files")
        
        # Clean up test file
        filepath.unlink()
        test_data_dir = Path("test_data")
        if test_data_dir.exists():
            import shutil
            shutil.rmtree(test_data_dir)
            
        return True
        
    except Exception as e:
        print(f"✗ Registry test failed: {e}")
        return False

def test_small_scrape():
    """Test a small-scale scrape of just the first title structure."""
    print("\nTesting small-scale scrape...")
    
    try:
        scraper = LegalCodeScraper(rate_limit_enabled=True, delay_seconds=0.5)
        
        # Get first WAC title
        wac_base_url = "https://app.leg.wa.gov/wac/default.aspx"
        titles = scraper.scrape_titles(wac_base_url, "WAC")
        
        if not titles:
            print("✗ Could not get titles for small scrape test")
            return False
            
        # Take just the first title and scrape its structure
        first_title = titles[0]
        print(f"Testing structure scrape for title {first_title.title_number}: {first_title.name}")
        
        # Scrape just this title's structure
        complete_title = scraper.scrape_title_structure(first_title, wac_base_url)
        
        print(f"✓ Scraped title structure:")
        print(f"  Title: {complete_title.title_number} - {complete_title.name}")
        print(f"  Chapters: {len(complete_title.chapters)}")
        
        total_sections = sum(len(chapter.sections) for chapter in complete_title.chapters)
        print(f"  Total sections: {total_sections}")
        
        if complete_title.chapters:
            first_chapter = complete_title.chapters[0]
            print(f"  First chapter: {first_chapter.chapter_number} - {first_chapter.name}")
            print(f"    Sections: {len(first_chapter.sections)}")
            
            if first_chapter.sections:
                first_section = first_chapter.sections[0]
                print(f"    First section: {first_section.section_number} - {first_section.name}")
        
        return True
        
    except Exception as e:
        print(f"✗ Small scrape test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    logging.basicConfig(level=logging.WARNING)  # Reduce noise for testing
    
    print("WA Law Scraper Registry System - Manual Test")
    print("=" * 50)
    
    tests = [
        ("Basic Scraper", test_scraper_basic),
        ("Registry System", test_registry_system),
        ("Small Scrape", test_small_scrape),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name} Test:")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print(f"\n{'='*50}")
    print("TEST RESULTS:")
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())