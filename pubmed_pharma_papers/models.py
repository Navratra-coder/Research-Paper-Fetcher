"""Data models for PubMed papers and authors."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date


@dataclass
class Author:
    """Represents an author of a research paper."""

    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None
    is_corresponding: bool = False

    def __post_init__(self) -> None:
        """Validate author data after initialization."""
        if not self.name.strip():
            raise ValueError("Author name cannot be empty")


@dataclass
class Paper:
    """Represents a research paper from PubMed."""

    pubmed_id: str
    title: str
    publication_date: Optional[date] = None
    authors: List[Author] = field(default_factory=list)
    abstract: Optional[str] = None
    journal: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate paper data after initialization."""
        if not self.pubmed_id.strip():
            raise ValueError("PubMed ID cannot be empty")
        if not self.title.strip():
            raise ValueError("Paper title cannot be empty")

    def get_non_academic_authors(self) -> List[Author]:
        """Return authors affiliated with non-academic institutions."""
        return [
            author
            for author in self.authors
            if self._is_non_academic_author(author)
        ]

    def get_corresponding_author_email(self) -> Optional[str]:
        """Return the email of the corresponding author."""
        for author in self.authors:
            if author.is_corresponding and author.email:
                return author.email
        return None

    def get_company_affiliations(self) -> List[str]:
        """Return unique company affiliations from non-academic authors."""
        affiliations = set()
        for author in self.get_non_academic_authors():
            if author.affiliation:
                affiliations.add(author.affiliation)
        return sorted(list(affiliations))

    @staticmethod
    def _is_non_academic_author(author: Author) -> bool:
        """Check if author is affiliated with non-academic institution."""
        if not author.affiliation:
            return False

        affiliation_lower = author.affiliation.lower()

        # Academic keywords that suggest academic affiliation
        academic_keywords = [
            "university",
            "college",
            "school",
            "institute",
            "academy",
            "research center",
            "medical center",
            "hospital",
            "clinic",
            "laboratory",
            "dept",
            "department",
            "faculty",
            "campus",
        ]

        # Check if affiliation contains academic keywords
        for keyword in academic_keywords:
            if keyword in affiliation_lower:
                return False

        # Company/industry keywords that suggest pharma/biotech affiliation
        company_keywords = [
            "pharmaceutical",
            "pharma",
            "biotech",
            "biotechnology",
            "therapeutics",
            "biopharmaceutical",
            "inc",
            "inc.",
            "ltd",
            "ltd.",
            "corp",
            "corp.",
            "corporation",
            "company",
            "co",
            "co.",
            "ag",
            "gmbh",
            "llc",
            "plc",
        ]

        # Check if affiliation contains company keywords
        for keyword in company_keywords:
            if keyword in affiliation_lower:
                return True

        return False
