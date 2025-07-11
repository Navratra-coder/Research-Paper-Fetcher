"""CSV writer for exporting paper data."""

import csv
from typing import List, TextIO
from .models import Paper


class CSVWriter:
    """Writer for exporting paper data to CSV format."""

    HEADERS = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email",
    ]

    def __init__(self) -> None:
        """Initialize the CSV writer."""
        pass

    def write_papers_to_csv(
        self, papers: List[Paper], output_file: TextIO
    ) -> None:
        """Write papers to CSV format.

        Args:
            papers: List of Paper objects to write
            output_file: File-like object to write to
        """
        writer = csv.writer(output_file)
        writer.writerow(self.HEADERS)

        for paper in papers:
            row = self._paper_to_csv_row(paper)
            writer.writerow(row)

    def _paper_to_csv_row(self, paper: Paper) -> List[str]:
        """Convert a Paper object to a CSV row.

        Args:
            paper: Paper object to convert

        Returns:
            List of strings representing CSV row
        """
        # Get non-academic authors
        non_academic_authors = paper.get_non_academic_authors()
        non_academic_author_names = "; ".join(
            [author.name for author in non_academic_authors]
        )

        # Get company affiliations
        company_affiliations = paper.get_company_affiliations()
        company_affiliations_str = "; ".join(company_affiliations)

        # Get corresponding author email
        corresponding_email = paper.get_corresponding_author_email() or ""

        # Format publication date
        pub_date_str = (
            paper.publication_date.strftime("%Y-%m-%d")
            if paper.publication_date
            else ""
        )

        return [
            paper.pubmed_id,
            paper.title,
            pub_date_str,
            non_academic_author_names,
            company_affiliations_str,
            corresponding_email,
        ]

    def papers_to_csv_string(self, papers: List[Paper]) -> str:
        """Convert papers to CSV string format.

        Args:
            papers: List of Paper objects to convert

        Returns:
            CSV formatted string
        """
        import io

        output = io.StringIO()
        self.write_papers_to_csv(papers, output)
        csv_string = output.getvalue()
        output.close()

        return csv_string
