"""Data models for WAC and RCW legal document structure."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Section:
    """Represents a legal section within a chapter."""
    name: str
    url: str
    section_number: str
    parent_chapter_number: str
    parent_title_number: str

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        return {
            'name': self.name,
            'url': self.url,
            'section_number': self.section_number,
            'parent_chapter_number': self.parent_chapter_number,
            'parent_title_number': self.parent_title_number
        }


@dataclass
class Chapter:
    """Represents a legal chapter within a title."""
    name: str
    url: str
    chapter_number: str
    parent_title_number: str
    sections: List[Section] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        return {
            'name': self.name,
            'url': self.url,
            'chapter_number': self.chapter_number,
            'parent_title_number': self.parent_title_number,
            'sections': [section.to_dict() for section in self.sections]
        }


@dataclass
class Title:
    """Represents a legal title containing chapters."""
    name: str
    url: str
    title_number: str
    disposition_url: Optional[str] = None
    chapters: List[Chapter] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        result = {
            'name': self.name,
            'url': self.url,
            'title_number': self.title_number,
            'chapters': [chapter.to_dict() for chapter in self.chapters]
        }
        if self.disposition_url:
            result['disposition_url'] = self.disposition_url
        return result


@dataclass
class LegalCodeRegistry:
    """Registry containing all legal code structure for WAC or RCW."""
    code_type: str  # 'WAC' or 'RCW'
    created_at: datetime
    base_url: str
    titles: List[Title] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        return {
            'code_type': self.code_type,
            'created_at': self.created_at.isoformat(),
            'base_url': self.base_url,
            'titles': [title.to_dict() for title in self.titles]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'LegalCodeRegistry':
        """Create registry from dictionary (for loading from YAML)."""
        titles = []
        for title_data in data.get('titles', []):
            chapters = []
            for chapter_data in title_data.get('chapters', []):
                sections = []
                for section_data in chapter_data.get('sections', []):
                    sections.append(Section(
                        name=section_data['name'],
                        url=section_data['url'],
                        section_number=section_data['section_number'],
                        parent_chapter_number=section_data['parent_chapter_number'],
                        parent_title_number=section_data['parent_title_number']
                    ))
                chapters.append(Chapter(
                    name=chapter_data['name'],
                    url=chapter_data['url'],
                    chapter_number=chapter_data['chapter_number'],
                    parent_title_number=chapter_data['parent_title_number'],
                    sections=sections
                ))
            titles.append(Title(
                name=title_data['name'],
                url=title_data['url'],
                title_number=title_data['title_number'],
                disposition_url=title_data.get('disposition_url'),
                chapters=chapters
            ))
        
        return cls(
            code_type=data['code_type'],
            created_at=datetime.fromisoformat(data['created_at']),
            base_url=data['base_url'],
            titles=titles
        )