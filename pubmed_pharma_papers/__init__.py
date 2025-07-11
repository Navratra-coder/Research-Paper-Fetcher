"""PubMed Pharmaceutical Papers Fetcher.

A Python package to fetch research papers from PubMed with
pharmaceutical/biotech company affiliations.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .pubmed_client import PubMedClient, PubMedAPIError
from .paper_filter import PaperFilter
from .csv_writer import CSVWriter
from .models import Paper, Author

__all__ = [
    "PubMedClient",
    "PubMedAPIError",
    "PaperFilter",
    "CSVWriter",
    "Paper",
    "Author",
]
