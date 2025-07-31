#!/usr/bin/env python3
"""
Test script to verify the HTML content scraper implementation.
This script tests the new content scraping functionality with minimal data.
"""

import sys
import logging
from pathlib import Path

# Add src to path to import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from wa_law_scraper import ContentManager, ContentScraper, RegistryManager
from wa_law_scraper.scripts.models import LegalCodeRegistry, Title, Chapter, Section
from datetime import datetime

def test_content_manager():
    """Test basic content manager functionality."""
    print("Testing ContentManager...")
    
    content_manager = ContentManager("test_data")
    
    # Test content path generation
    test_content = "<html><body>Test content</body></html>"
    
    # Test saving title content
    filepath = content_manager.save_content(
        test_content, "TEST", "1", is_disposition=False
    )
    print(f"✓ Saved title content to: {filepath}")
    
    # Test saving disposition content
    filepath = content_manager.save_content(
        test_content, "TEST", "1", is_disposition=True
    )
    print(f"✓ Saved disposition content to: {filepath}")
    
    # Test saving chapter content
    filepath = content_manager.save_content(
        test_content, "TEST", "1", "1-04"
    )
    print(f"✓ Saved chapter content to: {filepath}")
    
    # Test saving section content
    filepath = content_manager.save_content(
        test_content, "TEST", "1", "1-04", "1-04-010"
    )
    print(f"✓ Saved section content to: {filepath}")
    
    # Test existence check
    exists = content_manager.content_exists("TEST", "1")
    print(f"✓ Content exists check: {exists}")
    
    # Test listing content
    files = content_manager.list_content()
    print(f"✓ Found {len(files)} content files")
    
    # Test stats
    stats = content_manager.get_content_stats()
    print(f"✓ Content stats: {stats}")
    
    # Clean up test files
    import shutil
    test_data_dir = Path("test_data")
    if test_data_dir.exists():
        shutil.rmtree(test_data_dir)
    
    return True

def test_content_scraper_with_mock_registry():
    """Test content scraper with a mock registry."""
    print("\nTesting ContentScraper with mock registry...")
    
    try:
        # Create test registry
        test_section = Section(
            name="Test section",
            url="https://httpbin.org/html",  # Use httpbin for testing
            section_number="1-04-010",
            parent_chapter_number="1-04",
            parent_title_number="1"
        )
        
        test_chapter = Chapter(
            name="Test chapter",
            url="https://httpbin.org/html",
            chapter_number="1-04",
            parent_title_number="1",
            sections=[test_section]
        )
        
        test_title = Title(
            name="Test title",
            url="https://httpbin.org/html",
            title_number="1",
            disposition_url="https://httpbin.org/html",
            chapters=[test_chapter]
        )
        
        test_registry = LegalCodeRegistry(
            code_type="TEST",
            created_at=datetime.now(),
            base_url="https://httpbin.org",
            titles=[test_title]
        )
        
        # Set up managers
        registry_manager = RegistryManager("test_data")
        content_manager = ContentManager("test_data")
        
        # Save test registry
        registry_filepath = registry_manager.save_registry(test_registry)
        print(f"✓ Saved test registry to: {registry_filepath}")
        
        # Create content scraper
        content_scraper = ContentScraper(
            registry_manager, content_manager, 
            rate_limit_enabled=False, use_fake_useragent=False
        )
        
        # Test scraping title content
        success = content_scraper.scrape_title_content(test_title, "TEST", skip_existing=False)
        if success:
            print("✓ Successfully scraped title content")
        else:
            print("✗ Failed to scrape title content")
            return False
        
        # Check that files were created
        stats = content_manager.get_content_stats()
        print(f"✓ Content files created: {stats}")
        
        if stats['total_files'] > 0:
            print("✓ Content scraping test passed")
        else:
            print("✗ No content files were created")
            return False
        
        # Clean up test files
        import shutil
        test_data_dir = Path("test_data")
        if test_data_dir.exists():
            shutil.rmtree(test_data_dir)
        
        return True
        
    except Exception as e:
        print(f"✗ Content scraper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_integration():
    """Test CLI integration."""
    print("\nTesting CLI integration...")
    
    try:
        import subprocess
        import sys
        
        # Test help command
        result = subprocess.run([
            sys.executable, "-m", "wa_law_scraper.cli", "--help"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0 and "scrape-content" in result.stdout:
            print("✓ CLI help shows scrape-content command")
        else:
            print("✗ CLI help doesn't show scrape-content command")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
            return False
        
        # Test content info command  
        result = subprocess.run([
            sys.executable, "-m", "wa_law_scraper.cli", "content-info"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0 and "Total files:" in result.stdout:
            print("✓ CLI content-info command works")
        else:
            print("✗ CLI content-info command failed")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ CLI integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    logging.basicConfig(level=logging.WARNING)  # Reduce noise for testing
    
    print("WA Law Scraper - HTML Content Scraper Test")
    print("=" * 50)
    
    tests = [
        ("Content Manager", test_content_manager),
        ("Content Scraper", test_content_scraper_with_mock_registry),
        ("CLI Integration", test_cli_integration),
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