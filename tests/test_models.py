"""Tests for the data models."""

import pytest
from datetime import date
from pubmed_pharma_papers.models import Paper, Author


class TestAuthor:
    """Test cases for the Author class."""

    def test_author_creation(self):
        """Test basic author creation."""
        author = Author(
            name="John Doe",
            affiliation="Example Pharmaceutical Inc.",
            email="john.doe@example.com",
            is_corresponding=True,
        )

        assert author.name == "John Doe"
        assert author.affiliation == "Example Pharmaceutical Inc."
        assert author.email == "john.doe@example.com"
        assert author.is_corresponding is True

    def test_author_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Author name cannot be empty"):
            Author(name="")

    def test_author_whitespace_name_raises_error(self):
        """Test that whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="Author name cannot be empty"):
            Author(name="   ")


class TestPaper:
    """Test cases for the Paper class."""

    def test_paper_creation(self):
        """Test basic paper creation."""
        author = Author(name="Jane Smith", affiliation="Biotech Corp.")
        paper = Paper(
            pubmed_id="12345678",
            title="A Study on Drug Discovery",
            publication_date=date(2023, 1, 15),
            authors=[author],
        )

        assert paper.pubmed_id == "12345678"
        assert paper.title == "A Study on Drug Discovery"
        assert paper.publication_date == date(2023, 1, 15)
        assert len(paper.authors) == 1
        assert paper.authors[0].name == "Jane Smith"

    def test_paper_empty_pubmed_id_raises_error(self):
        """Test that empty PubMed ID raises ValueError."""
        with pytest.raises(ValueError, match="PubMed ID cannot be empty"):
            Paper(pubmed_id="", title="Test Title")

    def test_paper_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Paper title cannot be empty"):
            Paper(pubmed_id="12345678", title="")

    def test_get_non_academic_authors(self):
        """Test filtering non-academic authors."""
        academic_author = Author(
            name="Dr. Academic",
            affiliation="University of Science, Department of Biology",
        )
        pharma_author = Author(
            name="Dr. Pharma", affiliation="Big Pharma Inc."
        )

        paper = Paper(
            pubmed_id="12345678",
            title="Test Paper",
            authors=[academic_author, pharma_author],
        )

        non_academic_authors = paper.get_non_academic_authors()
        assert len(non_academic_authors) == 1
        assert non_academic_authors[0].name == "Dr. Pharma"

    def test_get_corresponding_author_email(self):
        """Test getting corresponding author email."""
        author1 = Author(
            name="Author 1",
            email="author1@example.com",
            is_corresponding=False,
        )
        author2 = Author(
            name="Author 2", email="author2@example.com", is_corresponding=True
        )

        paper = Paper(
            pubmed_id="12345678",
            title="Test Paper",
            authors=[author1, author2],
        )

        email = paper.get_corresponding_author_email()
        assert email == "author2@example.com"

    def test_get_company_affiliations(self):
        """Test getting unique company affiliations."""
        author1 = Author(name="Author 1", affiliation="Company A Inc.")
        author2 = Author(name="Author 2", affiliation="Company B Corp.")
        author3 = Author(name="Author 3", affiliation="Company A Inc.")

        paper = Paper(
            pubmed_id="12345678",
            title="Test Paper",
            authors=[author1, author2, author3],
        )

        affiliations = paper.get_company_affiliations()
        assert len(affiliations) == 2
        assert "Company A Inc." in affiliations
        assert "Company B Corp." in affiliations

    def test_is_non_academic_author(self):
        """Test the non-academic author detection."""
        # Academic cases
        academic_cases = [
            "University of California, Department of Chemistry",
            "Harvard Medical School",
            "Stanford Research Institute",
            "Memorial Sloan Kettering Cancer Center",
        ]

        for affiliation in academic_cases:
            author = Author(name="Test Author", affiliation=affiliation)
            assert not Paper._is_non_academic_author(author)

        # Non-academic cases
        non_academic_cases = [
            "Pfizer Inc.",
            "Novartis Pharmaceuticals",
            "Genentech Biotechnology",
            "Merck & Co.",
        ]

        for affiliation in non_academic_cases:
            author = Author(name="Test Author", affiliation=affiliation)
            assert Paper._is_non_academic_author(author)
