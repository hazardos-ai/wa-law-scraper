"""Web scraper for WAC and RCW legal documents."""

import re
import time
import logging
from typing import List, Optional, Tuple
from urllib.parse import urljoin
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from .models import Title, Chapter, Section
from ..cloudflare import Agent


logger = logging.getLogger(__name__)


class LegalCodeScraper:
    """Scraper for Washington State legal codes (WAC and RCW)."""

    def __init__(
        self,
        rate_limit_enabled: bool = False,
        delay_seconds: float = 1.0,
        use_fake_useragent: bool = True,
    ):
        """Initialize the scraper.

        Args:
            rate_limit_enabled: Whether to enable rate limiting between requests
            delay_seconds: Delay in seconds between requests when rate limiting is enabled
            use_fake_useragent: Whether to use fake user agent to bypass Cloudflare protection
        """
        self.rate_limit_enabled = rate_limit_enabled
        self.delay_seconds = delay_seconds
        self.use_fake_useragent = use_fake_useragent
        self.session = requests.Session()

        # Configure user agent based on settings
        if self.use_fake_useragent:
            try:
                agent = Agent()
                user_agent = agent.generate["User-Agent"]
                logger.info(f"Using fake user agent: {user_agent}")
            except Exception as e:
                logger.warning(
                    f"Failed to generate fake user agent, falling back to default: {e}"
                )
                user_agent = "WA-Law-Scraper/1.0 (Educational/Research Purpose)"
        else:
            user_agent = "WA-Law-Scraper/1.0 (Educational/Research Purpose)"

        self.session.headers.update({"User-Agent": user_agent})

    def _extract_title_name(self, link) -> str:
        """Extract the descriptive name for a title from the table structure.

        The HTML structure is typically:
        <td><a href="...?cite=X">Title X</a></td><td>Descriptive Name</td>

        Args:
            link: BeautifulSoup link element

        Returns:
            Descriptive title name or fallback to link text
        """
        try:
            # Find the parent <td> of the link
            td_parent = link.find_parent("td")
            if td_parent:
                # Find the next sibling <td> which contains the description
                next_td = td_parent.find_next_sibling("td")
                if next_td:
                    description = next_td.get_text(strip=True)
                    if description:
                        return description
        except Exception as e:
            logger.debug(f"Failed to extract title description: {e}")

        # Fallback to the link text if we can't find the description
        return link.get_text(strip=True)

    def _extract_chapter_name(self, link) -> str:
        """Extract the descriptive name for a chapter from the table structure.

        The HTML structure is typically:
        <td><a href="...?cite=X.YY">X.YY</a></td><td>Chapter Description</td>

        Args:
            link: BeautifulSoup link element

        Returns:
            Descriptive chapter name or fallback to link text
        """
        try:
            # Find the parent <td> of the link
            td_parent = link.find_parent("td")
            if td_parent:
                # Find the next sibling <td> which contains the description
                next_td = td_parent.find_next_sibling("td")
                if next_td:
                    description = next_td.get_text(strip=True)
                    if description:
                        return description
        except Exception as e:
            logger.debug(f"Failed to extract chapter description: {e}")

        # Fallback to the link text if we can't find the description
        return link.get_text(strip=True)

    def _extract_section_name(self, link) -> str:
        """Extract the descriptive name for a section from the table structure.

        The HTML structure varies but typically:
        <td><a href="...?cite=X.YY.ZZZ">X.YY.ZZZ</a></td><td>Section Description</td>

        Args:
            link: BeautifulSoup link element

        Returns:
            Descriptive section name or fallback to link text
        """
        try:
            # Find the parent <td> of the link
            td_parent = link.find_parent("td")
            if td_parent:
                # Find the next sibling <td> which contains the description
                next_td = td_parent.find_next_sibling("td")
                if next_td:
                    description = next_td.get_text(strip=True)
                    if description:
                        return description
        except Exception as e:
            logger.debug(f"Failed to extract section description: {e}")

        # Fallback to the link text if we can't find the description
        return link.get_text(strip=True)

    def _make_request(self, url: str) -> Optional[BeautifulSoup]:
        """Make a HTTP request with error handling and optional rate limiting.

        Args:
            url: URL to request

        Returns:
            BeautifulSoup object of the page content, or None if request failed
        """
        if self.rate_limit_enabled:
            time.sleep(self.delay_seconds)

        try:
            logger.info(f"Requesting: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def _extract_titles(
        self, soup: BeautifulSoup, base_url: str, code_type: str
    ) -> List[Title]:
        """Extract all titles from the main index page.

        Args:
            soup: BeautifulSoup object of the main index page
            base_url: Base URL for the legal code
            code_type: Type of legal code ('WAC' or 'RCW')

        Returns:
            List of Title objects
        """
        titles = []

        # Find title links - they typically contain "cite=" or "Cite=" parameter
        # Use case-insensitive matching and support alphanumeric title numbers
        title_links = soup.find_all(
            "a", href=re.compile(r"[Cc]ite=\d+[A-Z]*", re.IGNORECASE)
        )

        for link in title_links:
            href = link.get("href")
            if not href:
                continue

            # Extract title number from URL (case-insensitive, alphanumeric)
            title_match = re.search(r"[Cc]ite=(\d+[A-Z]*)", href, re.IGNORECASE)
            if not title_match:
                continue

            title_number = title_match.group(1)

            # Get the descriptive name from the adjacent table cell
            # The structure is: <td><a>Title X</a></td><td>Description</td>
            title_name = self._extract_title_name(link)

            # Build full URL
            full_url = urljoin(base_url, href)

            # Create disposition URL for titles (adds dispo=true parameter)
            disposition_url = None
            if "?" in full_url:
                disposition_url = full_url + "&dispo=true"
            else:
                disposition_url = full_url + "?dispo=true"

            title = Title(
                name=title_name,
                url=full_url,
                title_number=title_number,
                disposition_url=disposition_url,
            )
            titles.append(title)

        logger.info(f"Found {len(titles)} titles for {code_type}")
        return titles

    def _extract_chapters(
        self, soup: BeautifulSoup, base_url: str, title_number: str
    ) -> List[Chapter]:
        """Extract all chapters from a title page.

        Args:
            soup: BeautifulSoup object of the title page
            base_url: Base URL for the legal code
            title_number: Parent title number

        Returns:
            List of Chapter objects
        """
        chapters = []

        # Find chapter links - WAC uses hyphens, RCW uses periods in cite parameter
        # Use case-insensitive matching for both formats
        # Try both patterns: title-chapter (WAC) and title.chapter (RCW)
        chapter_links_hyphen = soup.find_all(
            "a",
            href=re.compile(rf"[Cc]ite={re.escape(title_number)}-\d+", re.IGNORECASE),
        )
        chapter_links_period = soup.find_all(
            "a",
            href=re.compile(rf"[Cc]ite={re.escape(title_number)}\.\d+", re.IGNORECASE),
        )
        chapter_links = chapter_links_hyphen + chapter_links_period

        for link in chapter_links:
            href = link.get("href")
            if not href:
                continue

            # Extract chapter number from URL (case-insensitive) - try both patterns
            chapter_match = re.search(
                rf"[Cc]ite={re.escape(title_number)}[-.](\d+)", href, re.IGNORECASE
            )
            if not chapter_match:
                continue

            # For consistency, use hyphen format for chapter numbers regardless of URL format
            chapter_number = f"{title_number}-{chapter_match.group(1)}"

            # Get the descriptive name from the adjacent table cell
            chapter_name = self._extract_chapter_name(link)

            # Build full URL
            full_url = urljoin(base_url, href)

            chapter = Chapter(
                name=chapter_name,
                url=full_url,
                chapter_number=chapter_number,
                parent_title_number=title_number,
            )
            chapters.append(chapter)

        logger.info(f"Found {len(chapters)} chapters for title {title_number}")
        return chapters

    def _extract_sections(
        self, soup: BeautifulSoup, base_url: str, title_number: str, chapter_number: str
    ) -> List[Section]:
        """Extract all sections from a chapter page.

        Args:
            soup: BeautifulSoup object of the chapter page
            base_url: Base URL for the legal code
            title_number: Parent title number
            chapter_number: Parent chapter number (format: title-chapter)

        Returns:
            List of Section objects
        """
        sections = []

        # Find section links - WAC uses hyphens, RCW uses periods in cite parameter
        # Use case-insensitive matching for both formats
        # Convert chapter_number format (1-04) to match URL patterns (1.04 for RCW, 1-04 for WAC)
        chapter_for_pattern = chapter_number.replace(
            "-", "."
        )  # For RCW pattern like 1.04
        section_pattern_hyphen = (
            rf"[Cc]ite={re.escape(chapter_number)}-\d+"  # WAC pattern like 1-04-010
        )
        section_pattern_period = rf"[Cc]ite={re.escape(chapter_for_pattern)}\.\d+"  # RCW pattern like 1.04.010

        section_links_hyphen = soup.find_all(
            "a", href=re.compile(section_pattern_hyphen, re.IGNORECASE)
        )
        section_links_period = soup.find_all(
            "a", href=re.compile(section_pattern_period, re.IGNORECASE)
        )
        section_links = section_links_hyphen + section_links_period

        for link in section_links:
            href = link.get("href")
            if not href:
                continue

            # Extract section number from URL (case-insensitive) - try both patterns
            section_match = re.search(
                rf"[Cc]ite=({re.escape(chapter_number)}[-.][\d.]+)", href, re.IGNORECASE
            )
            if not section_match:
                # Also try with period format for RCW
                section_match = re.search(
                    rf"[Cc]ite=({re.escape(chapter_for_pattern)}\.[\d.]+)",
                    href,
                    re.IGNORECASE,
                )
                if section_match:
                    # Convert back to hyphen format for consistency
                    section_number = section_match.group(1).replace(".", "-")
                else:
                    continue
            else:
                section_number = section_match.group(1)

            # Get the descriptive name from the adjacent table cell
            section_name = self._extract_section_name(link)

            # Build full URL
            full_url = urljoin(base_url, href)

            section = Section(
                name=section_name,
                url=full_url,
                section_number=section_number,
                parent_chapter_number=chapter_number,
                parent_title_number=title_number,
            )
            sections.append(section)

        logger.info(f"Found {len(sections)} sections for chapter {chapter_number}")
        return sections

    def scrape_titles(self, base_url: str, code_type: str) -> List[Title]:
        """Scrape all titles from the main index page.

        Args:
            base_url: Base URL for the legal code
            code_type: Type of legal code ('WAC' or 'RCW')

        Returns:
            List of Title objects with basic information
        """
        soup = self._make_request(base_url)
        if not soup:
            logger.error(f"Failed to fetch main page for {code_type}")
            return []

        return self._extract_titles(soup, base_url, code_type)

    def scrape_title_structure(self, title: Title, base_url: str) -> Title:
        """Scrape the complete structure (chapters and sections) for a title.

        Args:
            title: Title object to populate with chapters and sections
            base_url: Base URL for the legal code

        Returns:
            Title object with populated chapters and sections
        """
        logger.info(f"Scraping structure for title {title.title_number}: {title.name}")

        # Get chapters for this title
        soup = self._make_request(title.url)
        if not soup:
            logger.error(f"Failed to fetch title page for {title.title_number}")
            return title

        chapters = self._extract_chapters(soup, base_url, title.title_number)

        # For each chapter, get its sections
        for chapter in chapters:
            soup = self._make_request(chapter.url)
            if soup:
                sections = self._extract_sections(
                    soup, base_url, title.title_number, chapter.chapter_number
                )
                chapter.sections = sections
            else:
                logger.error(
                    f"Failed to fetch chapter page for {chapter.chapter_number}"
                )

        title.chapters = chapters
        return title

    def scrape_html_content(self, url: str) -> Optional[str]:
        """Scrape the complete HTML content from a URL.

        Args:
            url: URL to scrape content from

        Returns:
            Complete HTML content as string, or None if request failed
        """
        if self.rate_limit_enabled:
            time.sleep(self.delay_seconds)

        try:
            logger.info(f"Scraping HTML content from: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch HTML content from {url}: {e}")
            return None
