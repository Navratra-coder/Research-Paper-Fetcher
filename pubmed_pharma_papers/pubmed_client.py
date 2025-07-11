"""PubMed API client for fetching research papers."""

import requests
import xmltodict
from typing import Dict, List, Optional, Any
from datetime import date
import logging
import time
from .models import Paper, Author


class PubMedAPIError(Exception):
    """Custom exception for PubMed API errors."""

    pass


class PubMedClient:
    """Client for interacting with the PubMed API."""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(
        self, email: Optional[str] = None, api_key: Optional[str] = None
    ) -> None:
        """Initialize the PubMed client.

        Args:
            email: Email address for NCBI API identification
            api_key: API key for increased rate limits
        """
        self.email = email
        self.api_key = api_key
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

        # Rate limiting parameters
        self.last_request_time = 0.0
        self.min_request_interval = 0.34  # ~3 requests per second

    def search_papers(self, query: str, max_results: int = 100) -> List[Paper]:
        """Search for papers using PubMed API.

        Args:
            query: Search query in PubMed format
            max_results: Maximum number of results to return

        Returns:
            List of Paper objects

        Raises:
            PubMedAPIError: If API request fails
        """
        try:
            # First, search for PMIDs
            pmids = self._search_pmids(query, max_results)

            if not pmids:
                self.logger.info("No papers found for query: %s", query)
                return []

            # Then fetch detailed information for each paper
            papers = self._fetch_paper_details(pmids)

            self.logger.info(
                "Found %d papers for query: %s", len(papers), query
            )
            return papers

        except requests.RequestException as e:
            raise PubMedAPIError(f"Failed to search papers: {str(e)}") from e

    def _search_pmids(self, query: str, max_results: int) -> List[str]:
        """Search for PubMed IDs using the eSearch API.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of PubMed IDs
        """
        self._rate_limit()

        params = {
            "db": "pubmed",
            "term": query,
            "retmax": str(max_results),
            "retmode": "json",
            "sort": "relevance",
        }

        if self.email:
            params["email"] = self.email
        if self.api_key:
            params["api_key"] = self.api_key

        url = f"{self.BASE_URL}/esearch.fcgi"
        response = self.session.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        # Check for API errors
        if "error" in data:
            raise PubMedAPIError(f"PubMed API error: {data['error']}")

        # Extract PMIDs from response
        id_list = data.get("esearchresult", {}).get("idlist", [])
        return list(id_list) if id_list else []

    def _fetch_paper_details(self, pmids: List[str]) -> List[Paper]:
        """Fetch detailed information for papers using eFetch API.

        Args:
            pmids: List of PubMed IDs

        Returns:
            List of Paper objects
        """
        if not pmids:
            return []

        self._rate_limit()

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "rettype": "abstract",
        }

        if self.email:
            params["email"] = self.email
        if self.api_key:
            params["api_key"] = self.api_key

        url = f"{self.BASE_URL}/efetch.fcgi"
        response = self.session.get(url, params=params)
        response.raise_for_status()

        # Parse XML response
        data = xmltodict.parse(response.text)

        papers = []
        pubmed_articles = data.get("PubmedArticleSet", {}).get(
            "PubmedArticle", []
        )

        # Handle single article case
        if isinstance(pubmed_articles, dict):
            pubmed_articles = [pubmed_articles]

        for article_data in pubmed_articles:
            try:
                paper = self._parse_paper_data(article_data)
                if paper:
                    papers.append(paper)
            except Exception as e:
                self.logger.warning("Failed to parse paper data: %s", str(e))
                continue

        return papers

    def _parse_paper_data(
        self, article_data: Dict[str, Any]
    ) -> Optional[Paper]:
        """Parse paper data from XML response.

        Args:
            article_data: Dictionary containing paper data from XML

        Returns:
            Paper object or None if parsing fails
        """
        try:
            medline_citation = article_data.get("MedlineCitation", {})
            article = medline_citation.get("Article", {})

            # Extract basic paper information
            pmid = medline_citation.get("PMID", {}).get("#text", "")
            title = article.get("ArticleTitle", "")

            # Handle title as dict or string
            if isinstance(title, dict):
                title = title.get("#text", "")

            # Extract publication date
            pub_date = self._parse_publication_date(
                article.get("Journal", {}).get("JournalIssue", {})
            )

            # Extract journal name
            journal = article.get("Journal", {}).get("Title", "")

            # Extract abstract
            abstract = self._parse_abstract(article.get("Abstract", {}))

            # Extract authors
            authors = self._parse_authors(article.get("AuthorList", {}))

            return Paper(
                pubmed_id=pmid,
                title=title,
                publication_date=pub_date,
                authors=authors,
                abstract=abstract,
                journal=journal,
            )

        except Exception as e:
            self.logger.error("Error parsing paper data: %s", str(e))
            return None

    def _parse_publication_date(
        self, journal_issue: Dict[str, Any]
    ) -> Optional[date]:
        """Parse publication date from journal issue data.

        Args:
            journal_issue: Journal issue data

        Returns:
            Publication date or None if not found
        """
        try:
            pub_date = journal_issue.get("PubDate", {})

            year = pub_date.get("Year", "")
            month = pub_date.get("Month", "1")
            day = pub_date.get("Day", "1")

            # Handle month names
            month_map = {
                "Jan": "1",
                "Feb": "2",
                "Mar": "3",
                "Apr": "4",
                "May": "5",
                "Jun": "6",
                "Jul": "7",
                "Aug": "8",
                "Sep": "9",
                "Oct": "10",
                "Nov": "11",
                "Dec": "12",
            }

            if month in month_map:
                month = month_map[month]

            if year:
                return date(int(year), int(month), int(day))

        except (ValueError, TypeError):
            pass

        return None

    def _parse_abstract(self, abstract_data: Dict[str, Any]) -> Optional[str]:
        """Parse abstract text from abstract data.

        Args:
            abstract_data: Abstract data from XML

        Returns:
            Abstract text or None if not found
        """
        if not abstract_data:
            return None

        abstract_text = abstract_data.get("AbstractText", "")

        if isinstance(abstract_text, dict):
            abstract_text = abstract_text.get("#text", "")
        elif isinstance(abstract_text, list):
            # Handle multiple abstract sections
            text_parts = []
            for part in abstract_text:
                if isinstance(part, dict):
                    text_parts.append(part.get("#text", ""))
                else:
                    text_parts.append(str(part))
            abstract_text = " ".join(text_parts)

        return abstract_text if abstract_text else None

    def _parse_authors(self, author_list: Dict[str, Any]) -> List[Author]:
        """Parse authors from author list data.

        Args:
            author_list: Author list data from XML

        Returns:
            List of Author objects
        """
        authors: List[Author] = []

        if not author_list:
            return authors

        author_data = author_list.get("Author", [])

        # Handle single author case
        if isinstance(author_data, dict):
            author_data = [author_data]

        for author_info in author_data:
            try:
                # Extract author name
                last_name = author_info.get("LastName", "")
                first_name = author_info.get("ForeName", "")
                initials = author_info.get("Initials", "")

                if last_name:
                    if first_name:
                        name = f"{first_name} {last_name}"
                    elif initials:
                        name = f"{initials} {last_name}"
                    else:
                        name = last_name
                else:
                    # Handle collective names
                    name = author_info.get("CollectiveName", "")

                if not name:
                    continue

                # Extract affiliation
                affiliation = None
                affiliation_info = author_info.get("AffiliationInfo", {})
                if isinstance(affiliation_info, list):
                    affiliation_info = (
                        affiliation_info[0] if affiliation_info else {}
                    )

                if affiliation_info:
                    affiliation = affiliation_info.get("Affiliation", "")

                # Extract email (usually embedded in affiliation)
                email = (
                    self._extract_email_from_affiliation(affiliation)
                    if affiliation
                    else None
                )

                # Note: PubMed XML doesn't reliably indicate authors
                # This would need additional processing

                authors.append(
                    Author(
                        name=name,
                        affiliation=affiliation,
                        email=email,
                        is_corresponding=False,
                    )
                )

            except Exception as e:
                self.logger.warning("Failed to parse author: %s", str(e))
                continue

        return authors

    def _extract_email_from_affiliation(
        self, affiliation: str
    ) -> Optional[str]:
        """Extract email address from affiliation string.

        Args:
            affiliation: Affiliation string

        Returns:
            Email address or None if not found
        """
        import re

        # Simple regex to find email addresses
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        matches = re.findall(email_pattern, affiliation)

        return matches[0] if matches else None

    def _rate_limit(self) -> None:
        """Implement rate limiting for API requests."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)

        self.last_request_time = time.time()
