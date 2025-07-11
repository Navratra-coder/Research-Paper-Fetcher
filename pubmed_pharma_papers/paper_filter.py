"""Filter papers based on pharmaceutical/biotech company affiliations."""

from typing import List, Dict, Any, Set
import logging
from .models import Paper


class PaperFilter:
    """Filter papers to identify those with pharma/biotech affiliations."""

    def __init__(self) -> None:
        """Initialize the paper filter."""
        self.logger = logging.getLogger(__name__)

        # Common pharmaceutical/biotech company keywords
        self.pharma_keywords = [
            "pharmaceutical",
            "pharma",
            "biotech",
            "biotechnology",
            "therapeutics",
            "biopharmaceutical",
            "biopharma",
            "medicines",
            "drug",
            "drugs",
            "biologics",
        ]

        # Company structure keywords
        self.company_keywords = [
            "inc",
            "inc.",
            "incorporated",
            "ltd",
            "ltd.",
            "limited",
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
            "sa",
            "nv",
            "bv",
            "group",
            "holdings",
            "enterprises",
        ]

        # Academic institution keywords (to exclude)
        self.academic_keywords = [
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
            "division",
            "section",
            "unit",
            "center for",
            "centre for",
        ]

        # Known pharmaceutical/biotech companies (partial list)
        self.known_companies = [
            "pfizer",
            "novartis",
            "roche",
            "johnson & johnson",
            "merck",
            "glaxosmithkline",
            "gsk",
            "sanofi",
            "abbvie",
            "bristol myers squibb",
            "astrazeneca",
            "eli lilly",
            "boehringer ingelheim",
            "bayer",
            "takeda",
            "gilead",
            "biogen",
            "regeneron",
            "vertex",
            "moderna",
            "biontech",
            "amgen",
            "genentech",
            "celgene",
            "illumina",
            "danaher",
            "thermo fisher",
            "agilent",
            "waters",
            "perkinelmer",
        ]

    def filter_papers_with_pharma_affiliations(
        self, papers: List[Paper]
    ) -> List[Paper]:
        """Filter papers to include those with pharma/biotech affiliations.

        Args:
            papers: List of Paper objects to filter

        Returns:
            List of Paper objects with at least one non-academic author
        """
        filtered_papers = []

        for paper in papers:
            if self._has_pharma_affiliation(paper):
                filtered_papers.append(paper)

        self.logger.info(
            f"Filtered {len(filtered_papers)} papers from "
            f"{len(papers)} total papers"
        )
        return filtered_papers

    def _has_pharma_affiliation(self, paper: Paper) -> bool:
        """Check if paper has author with pharmaceutical/biotech affiliation.

        Args:
            paper: Paper object to check

        Returns:
            True if paper has pharmaceutical/biotech affiliation
        """
        non_academic_authors = paper.get_non_academic_authors()

        if not non_academic_authors:
            return False

        # Check if any non-academic author has pharma/biotech affiliation
        for author in non_academic_authors:
            if author.affiliation and self._is_pharma_biotech_affiliation(
                author.affiliation
            ):
                return True

        return False

    def _is_pharma_biotech_affiliation(self, affiliation: str) -> bool:
        """Check if affiliation is pharma/biotech industry related.

        Args:
            affiliation: Affiliation string to check

        Returns:
            True if affiliation is pharmaceutical/biotech related
        """
        if not affiliation:
            return False

        affiliation_lower = affiliation.lower()

        # Check for known pharmaceutical/biotech companies
        for company in self.known_companies:
            if company.lower() in affiliation_lower:
                return True

        # Check for pharmaceutical/biotech keywords
        for keyword in self.pharma_keywords:
            if keyword in affiliation_lower:
                return True

        # Check if it's a company structure and not academic
        has_company_keyword = any(
            keyword in affiliation_lower for keyword in self.company_keywords
        )
        has_academic_keyword = any(
            keyword in affiliation_lower for keyword in self.academic_keywords
        )

        # If it has company keywords but no academic keywords, it's likely one
        if has_company_keyword and not has_academic_keyword:
            return True

        return False

    def get_paper_statistics(self, papers: List[Paper]) -> Dict[str, Any]:
        """Get statistics about filtered papers.

        Args:
            papers: List of Paper objects

        Returns:
            Dictionary with statistics
        """
        unique_companies: Set[str] = set()
        papers_with_pharma_affiliations = 0
        total_non_academic_authors = 0
        papers_with_corresponding_mails = 0

        for paper in papers:
            non_academic_authors = paper.get_non_academic_authors()

            if non_academic_authors:
                papers_with_pharma_affiliations += 1
                total_non_academic_authors += len(non_academic_authors)

                # Collect unique company affiliations
                for author in non_academic_authors:
                    if author.affiliation:
                        unique_companies.add(author.affiliation)

            if paper.get_corresponding_author_email():
                papers_with_corresponding_mails += 1

        stats = {
            "total_papers": len(papers),
            "papers_with_pharma_affiliations": papers_with_pharma_affiliations,
            "unique_companies": len(unique_companies),
            "total_non_academic_authors": total_non_academic_authors,
            "papers_with_corresponding_mails": papers_with_corresponding_mails,
        }

        return stats
