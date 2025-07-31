"""Registry system for storing WAC and RCW legal document structure in YAML format."""

import os
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from .models import LegalCodeRegistry, Title
from .scraper import LegalCodeScraper


logger = logging.getLogger(__name__)


class RegistryManager:
    """Manages YAML-based registry files for legal code structure."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the registry manager.
        
        Args:
            data_dir: Root directory for data storage
        """
        self.data_dir = Path(data_dir)
        self.registry_dir = self.data_dir / "registry"
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Registry directory: {self.registry_dir}")

    def _generate_filename(self, code_type: str, timestamp: Optional[datetime] = None) -> str:
        """Generate timestamped filename for registry.
        
        Args:
            code_type: Type of legal code ('WAC' or 'RCW')
            timestamp: Optional timestamp, defaults to current time
            
        Returns:
            Filename in format: {code_type}_registry_YYYYMMDD_HHMMSS.yaml
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        return f"{code_type.lower()}_registry_{timestamp_str}.yaml"

    def save_registry(self, registry: LegalCodeRegistry) -> Path:
        """Save registry to YAML file.
        
        Args:
            registry: LegalCodeRegistry object to save
            
        Returns:
            Path to the saved file
        """
        filename = self._generate_filename(registry.code_type, registry.created_at)
        filepath = self.registry_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(registry.to_dict(), f, default_flow_style=False, 
                         sort_keys=False, allow_unicode=True, indent=2)
            
            logger.info(f"Registry saved to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save registry to {filepath}: {e}")
            raise

    def load_registry(self, filepath: Path) -> Optional[LegalCodeRegistry]:
        """Load registry from YAML file.
        
        Args:
            filepath: Path to the YAML file
            
        Returns:
            LegalCodeRegistry object or None if loading failed
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            registry = LegalCodeRegistry.from_dict(data)
            logger.info(f"Registry loaded from: {filepath}")
            return registry
            
        except Exception as e:
            logger.error(f"Failed to load registry from {filepath}: {e}")
            return None

    def list_registries(self, code_type: Optional[str] = None) -> List[Path]:
        """List all registry files, optionally filtered by code type.
        
        Args:
            code_type: Optional filter by code type ('WAC' or 'RCW')
            
        Returns:
            List of registry file paths, sorted by modification time (newest first)
        """
        pattern = "*_registry_*.yaml"
        if code_type:
            pattern = f"{code_type.lower()}_registry_*.yaml"
            
        registry_files = list(self.registry_dir.glob(pattern))
        # Sort by modification time, newest first
        registry_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        return registry_files

    def get_latest_registry(self, code_type: str) -> Optional[LegalCodeRegistry]:
        """Get the most recent registry for a given code type.
        
        Args:
            code_type: Type of legal code ('WAC' or 'RCW')
            
        Returns:
            Most recent LegalCodeRegistry or None if none found
        """
        registries = self.list_registries(code_type)
        if not registries:
            logger.info(f"No registries found for {code_type}")
            return None
            
        latest_file = registries[0]
        return self.load_registry(latest_file)


class RegistryGenerator:
    """Generates new registries by scraping legal code websites."""
    
    def __init__(self, registry_manager: RegistryManager, rate_limit_enabled: bool = False, use_fake_useragent: bool = True):
        """Initialize the registry generator.
        
        Args:
            registry_manager: RegistryManager instance for saving registries
            rate_limit_enabled: Whether to enable rate limiting for web requests
            use_fake_useragent: Whether to use fake user agent to bypass Cloudflare protection
        """
        self.registry_manager = registry_manager
        self.scraper = LegalCodeScraper(rate_limit_enabled=rate_limit_enabled, use_fake_useragent=use_fake_useragent)

    def generate_wac_registry(self) -> Optional[LegalCodeRegistry]:
        """Generate a new WAC registry by scraping the website.
        
        Returns:
            LegalCodeRegistry for WAC or None if generation failed
        """
        base_url = "https://app.leg.wa.gov/wac/default.aspx"
        code_type = "WAC"
        
        logger.info(f"Generating {code_type} registry from {base_url}")
        
        # Scrape titles
        titles = self.scraper.scrape_titles(base_url, code_type)
        if not titles:
            logger.error(f"Failed to scrape titles for {code_type}")
            return None
        
        # For each title, scrape its complete structure
        # Note: This can be time-consuming, so we might want to limit or make it optional
        logger.info(f"Scraping detailed structure for {len(titles)} titles...")
        
        for i, title in enumerate(titles, 1):
            logger.info(f"Processing title {i}/{len(titles)}: {title.title_number}")
            self.scraper.scrape_title_structure(title, base_url)
        
        # Create registry
        registry = LegalCodeRegistry(
            code_type=code_type,
            created_at=datetime.now(),
            base_url=base_url,
            titles=titles
        )
        
        # Save registry
        filepath = self.registry_manager.save_registry(registry)
        logger.info(f"WAC registry generated and saved to: {filepath}")
        
        return registry

    def generate_rcw_registry(self) -> Optional[LegalCodeRegistry]:
        """Generate a new RCW registry by scraping the website.
        
        Returns:
            LegalCodeRegistry for RCW or None if generation failed
        """
        base_url = "https://app.leg.wa.gov/RCW/default.aspx"
        code_type = "RCW"
        
        logger.info(f"Generating {code_type} registry from {base_url}")
        
        # Scrape titles
        titles = self.scraper.scrape_titles(base_url, code_type)
        if not titles:
            logger.error(f"Failed to scrape titles for {code_type}")
            return None
        
        # For each title, scrape its complete structure
        logger.info(f"Scraping detailed structure for {len(titles)} titles...")
        
        for i, title in enumerate(titles, 1):
            logger.info(f"Processing title {i}/{len(titles)}: {title.title_number}")
            self.scraper.scrape_title_structure(title, base_url)
        
        # Create registry
        registry = LegalCodeRegistry(
            code_type=code_type,
            created_at=datetime.now(),
            base_url=base_url,
            titles=titles
        )
        
        # Save registry
        filepath = self.registry_manager.save_registry(registry)
        logger.info(f"RCW registry generated and saved to: {filepath}")
        
        return registry

    def generate_both_registries(self) -> tuple[Optional[LegalCodeRegistry], Optional[LegalCodeRegistry]]:
        """Generate both WAC and RCW registries.
        
        Returns:
            Tuple of (WAC registry, RCW registry), either may be None if generation failed
        """
        logger.info("Generating both WAC and RCW registries")
        
        wac_registry = self.generate_wac_registry()
        rcw_registry = self.generate_rcw_registry()
        
        return wac_registry, rcw_registry


class ContentManager:
    """Manages HTML content storage and organization for legal codes."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the content manager.
        
        Args:
            data_dir: Root directory for data storage
        """
        self.data_dir = Path(data_dir)
        self.content_dir = self.data_dir / "raw_html"
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.content_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Content directory: {self.content_dir}")

    def _get_content_path(self, code_type: str, title_number: str, 
                         chapter_number: Optional[str] = None,
                         section_number: Optional[str] = None,
                         is_disposition: bool = False) -> Path:
        """Generate the appropriate file path for content storage.
        
        Args:
            code_type: Type of legal code ('WAC' or 'RCW')
            title_number: Title number
            chapter_number: Optional chapter number
            section_number: Optional section number  
            is_disposition: Whether this is disposition content
            
        Returns:
            Path object for the content file
        """
        # Start with code type directory
        path = self.content_dir / code_type.lower()
        
        # Add title directory
        title_dir = path / title_number
        title_dir.mkdir(parents=True, exist_ok=True)
        
        if section_number:
            # This is a section file
            if chapter_number:
                chapter_dir = title_dir / chapter_number
                chapter_dir.mkdir(parents=True, exist_ok=True)
                return chapter_dir / f"section_{section_number}.html"
            else:
                return title_dir / f"section_{section_number}.html"
        elif chapter_number:
            # This is a chapter file
            chapter_dir = title_dir / chapter_number
            chapter_dir.mkdir(parents=True, exist_ok=True)
            return chapter_dir / f"chapter_{chapter_number}.html"
        else:
            # This is a title file
            if is_disposition:
                return title_dir / f"title_{title_number}_disposition.html"
            else:
                return title_dir / f"title_{title_number}.html"

    def save_content(self, content: str, code_type: str, title_number: str,
                    chapter_number: Optional[str] = None,
                    section_number: Optional[str] = None,
                    is_disposition: bool = False) -> Path:
        """Save HTML content to appropriate file location.
        
        Args:
            content: HTML content to save
            code_type: Type of legal code ('WAC' or 'RCW')
            title_number: Title number
            chapter_number: Optional chapter number
            section_number: Optional section number
            is_disposition: Whether this is disposition content
            
        Returns:
            Path to the saved file
        """
        filepath = self._get_content_path(
            code_type, title_number, chapter_number, section_number, is_disposition
        )
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Content saved to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save content to {filepath}: {e}")
            raise

    def content_exists(self, code_type: str, title_number: str,
                      chapter_number: Optional[str] = None,
                      section_number: Optional[str] = None,
                      is_disposition: bool = False) -> bool:
        """Check if content already exists for the given parameters.
        
        Args:
            code_type: Type of legal code ('WAC' or 'RCW')
            title_number: Title number
            chapter_number: Optional chapter number
            section_number: Optional section number
            is_disposition: Whether this is disposition content
            
        Returns:
            True if content file exists, False otherwise
        """
        filepath = self._get_content_path(
            code_type, title_number, chapter_number, section_number, is_disposition
        )
        return filepath.exists()

    def list_content(self, code_type: Optional[str] = None) -> List[Path]:
        """List all content files, optionally filtered by code type.
        
        Args:
            code_type: Optional filter by code type ('WAC' or 'RCW')
            
        Returns:
            List of content file paths
        """
        if code_type:
            pattern = f"{code_type.lower()}/**/*.html"
        else:
            pattern = "**/*.html"
            
        content_files = list(self.content_dir.glob(pattern))
        content_files.sort()
        
        return content_files

    def get_content_stats(self) -> dict:
        """Get statistics about stored content.
        
        Returns:
            Dictionary with content statistics
        """
        stats = {
            'total_files': 0,
            'wac_files': 0,
            'rcw_files': 0,
            'title_files': 0,
            'chapter_files': 0,
            'section_files': 0,
            'disposition_files': 0
        }
        
        for filepath in self.list_content():
            stats['total_files'] += 1
            
            # Check code type
            if '/wac/' in str(filepath):
                stats['wac_files'] += 1
            elif '/rcw/' in str(filepath):
                stats['rcw_files'] += 1
            
            # Check content type
            filename = filepath.name
            if filename.startswith('title_'):
                stats['title_files'] += 1
                if 'disposition' in filename:
                    stats['disposition_files'] += 1
            elif filename.startswith('chapter_'):
                stats['chapter_files'] += 1
            elif filename.startswith('section_'):
                stats['section_files'] += 1
        
        return stats


class ContentScraper:
    """Scrapes and stores HTML content for legal codes using existing registries."""
    
    def __init__(self, registry_manager: RegistryManager, content_manager: ContentManager,
                 rate_limit_enabled: bool = False, use_fake_useragent: bool = True):
        """Initialize the content scraper.
        
        Args:
            registry_manager: RegistryManager instance for loading registries
            content_manager: ContentManager instance for saving content
            rate_limit_enabled: Whether to enable rate limiting for web requests
            use_fake_useragent: Whether to use fake user agent to bypass Cloudflare protection
        """
        self.registry_manager = registry_manager
        self.content_manager = content_manager
        self.scraper = LegalCodeScraper(rate_limit_enabled=rate_limit_enabled, use_fake_useragent=use_fake_useragent)

    def scrape_title_content(self, title: Title, code_type: str, skip_existing: bool = True) -> bool:
        """Scrape content for a title and all its chapters/sections.
        
        Args:
            title: Title object with populated structure
            code_type: Type of legal code ('WAC' or 'RCW')
            skip_existing: Whether to skip files that already exist
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Scraping content for title {title.title_number}: {title.name}")
        
        try:
            # Scrape main title page
            if not skip_existing or not self.content_manager.content_exists(code_type, title.title_number):
                content = self.scraper.scrape_html_content(title.url)
                if content:
                    self.content_manager.save_content(content, code_type, title.title_number)
                else:
                    logger.error(f"Failed to scrape title content for {title.title_number}")
                    return False
            
            # Scrape disposition page if available
            if title.disposition_url:
                if not skip_existing or not self.content_manager.content_exists(
                    code_type, title.title_number, is_disposition=True
                ):
                    content = self.scraper.scrape_html_content(title.disposition_url)
                    if content:
                        self.content_manager.save_content(
                            content, code_type, title.title_number, is_disposition=True
                        )
                    else:
                        logger.warning(f"Failed to scrape disposition content for {title.title_number}")
            
            # Scrape chapters and sections
            for chapter in title.chapters:
                # Scrape chapter page
                if not skip_existing or not self.content_manager.content_exists(
                    code_type, title.title_number, chapter.chapter_number
                ):
                    content = self.scraper.scrape_html_content(chapter.url)
                    if content:
                        self.content_manager.save_content(
                            content, code_type, title.title_number, chapter.chapter_number
                        )
                    else:
                        logger.error(f"Failed to scrape chapter content for {chapter.chapter_number}")
                        continue
                
                # Scrape sections
                for section in chapter.sections:
                    if not skip_existing or not self.content_manager.content_exists(
                        code_type, title.title_number, chapter.chapter_number, section.section_number
                    ):
                        content = self.scraper.scrape_html_content(section.url)
                        if content:
                            self.content_manager.save_content(
                                content, code_type, title.title_number,
                                chapter.chapter_number, section.section_number
                            )
                        else:
                            logger.error(f"Failed to scrape section content for {section.section_number}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to scrape content for title {title.title_number}: {e}")
            return False

    def scrape_registry_content(self, code_type: str, skip_existing: bool = True) -> bool:
        """Scrape content for all items in the latest registry of the given type.
        
        Args:
            code_type: Type of legal code ('WAC' or 'RCW')
            skip_existing: Whether to skip files that already exist
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Starting content scrape for {code_type} registry")
        
        # Load latest registry
        registry = self.registry_manager.get_latest_registry(code_type)
        if not registry:
            logger.error(f"No registry found for {code_type}")
            return False
        
        logger.info(f"Found {len(registry.titles)} titles in {code_type} registry")
        
        # Scrape content for each title
        success_count = 0
        for i, title in enumerate(registry.titles, 1):
            logger.info(f"Processing title {i}/{len(registry.titles)}: {title.title_number}")
            
            if self.scrape_title_content(title, code_type, skip_existing):
                success_count += 1
            else:
                logger.error(f"Failed to scrape content for title {title.title_number}")
        
        logger.info(f"Content scraping completed: {success_count}/{len(registry.titles)} titles successful")
        return success_count == len(registry.titles)