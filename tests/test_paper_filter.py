"""Tests for the paper filter."""

from pubmed_pharma_papers.paper_filter import PaperFilter
from pubmed_pharma_papers.models import Paper, Author


class TestPaperFilter:
    """Test cases for the PaperFilter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.filter = PaperFilter()

    def test_filter_papers_with_pharma_affiliations(self):
        """Test filtering papers with pharmaceutical affiliations."""
        # Create test papers
        academic_paper = Paper(
            pubmed_id="111",
            title="Academic Paper",
            authors=[
                Author(
                    name="Academic Author", affiliation="University of Test"
                )
            ],
        )

        pharma_paper = Paper(
            pubmed_id="222",
            title="Pharma Paper",
            authors=[Author(name="Pharma Author", affiliation="Pfizer Inc.")],
        )

        mixed_paper = Paper(
            pubmed_id="333",
            title="Mixed Paper",
            authors=[
                Author(
                    name="Academic Author", affiliation="University of Test"
                ),
                Author(
                    name="Pharma Author",
                    affiliation="Novartis Pharmaceuticals",
                ),
            ],
        )

        papers = [academic_paper, pharma_paper, mixed_paper]
        filtered_papers = self.filter.filter_papers_with_pharma_affiliations(
            papers
        )

        assert len(filtered_papers) == 2
        assert pharma_paper in filtered_papers
        assert mixed_paper in filtered_papers
        assert academic_paper not in filtered_papers

    def test_is_pharma_biotech_affiliation(self):
        """Test pharmaceutical/biotech affiliation detection."""
        # Test known companies
        known_company_cases = [
            "Pfizer Inc.",
            "Novartis Pharmaceuticals",
            "Genentech",
            "Johnson & Johnson",
        ]

        for affiliation in known_company_cases:
            assert self.filter._is_pharma_biotech_affiliation(affiliation)

        # Test pharmaceutical keywords
        pharma_keyword_cases = [
            "ABC Pharmaceuticals",
            "XYZ Biotech",
            "Research Therapeutics Ltd.",
            "Biopharmaceutical Company",
        ]

        for affiliation in pharma_keyword_cases:
            assert self.filter._is_pharma_biotech_affiliation(affiliation)

        # Test academic institutions (should return False)
        academic_cases = [
            "University of California",
            "Harvard Medical School",
            "Stanford Research Institute",
        ]

        for affiliation in academic_cases:
            assert not self.filter._is_pharma_biotech_affiliation(affiliation)

        # Test company structures without academic keywords
        company_cases = [
            "TechCorp Inc.",
            "Innovation Ltd.",
            "BioSolutions Corporation",
        ]

        for affiliation in company_cases:
            assert self.filter._is_pharma_biotech_affiliation(affiliation)

    def test_get_paper_statistics(self):
        """Test paper statistics generation."""
        pharma_paper = Paper(
            pubmed_id="111",
            title="Pharma Paper",
            authors=[
                Author(
                    name="Pharma Author",
                    affiliation="Pfizer Inc.",
                    email="author@pfizer.com",
                    is_corresponding=True,
                )
            ],
        )

        academic_paper = Paper(
            pubmed_id="222",
            title="Academic Paper",
            authors=[
                Author(
                    name="Academic Author", affiliation="University of Test"
                )
            ],
        )

        papers = [pharma_paper, academic_paper]
        stats = self.filter.get_paper_statistics(papers)

        assert stats["total_papers"] == 2
        assert stats["papers_with_pharma_affiliations"] == 1
        assert stats["total_non_academic_authors"] == 1
        assert stats["papers_with_corresponding_mails"] == 1
        assert stats["unique_companies"] == 1
