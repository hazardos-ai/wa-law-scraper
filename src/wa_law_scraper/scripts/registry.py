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