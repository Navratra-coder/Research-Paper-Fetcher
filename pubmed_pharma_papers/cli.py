"""Command-line interface for the PubMed pharmaceutical papers fetcher."""

import click
import logging
import sys
from typing import Optional
from pathlib import Path

from .pubmed_client import PubMedClient, PubMedAPIError
from .paper_filter import PaperFilter
from .csv_writer import CSVWriter


def setup_logging(debug: bool = False) -> None:
    """Set up logging configuration.

    Args:
        debug: Whether to enable debug logging
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )


@click.command()
@click.argument("query", type=str, required=True)
@click.option(
    "-f",
    "--file",
    type=click.Path(path_type=Path),
    help="Specify the filename to save the results. "
    "If not provided, print to console.",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Print debug information during execution.",
)
@click.option(
    "--max-results",
    type=int,
    default=100,
    help="Maximum number of results to fetch (default: 100).",
)
@click.option(
    "--email",
    type=str,
    help="Email address for NCBI API identification (recommended).",
)
@click.option(
    "--api-key", type=str, help="NCBI API key for increased rate limits."
)
@click.version_option(version="0.1.0")
def main(
    query: str,
    file: Optional[Path] = None,
    debug: bool = False,
    max_results: int = 100,
    email: Optional[str] = None,
    api_key: Optional[str] = None,
) -> None:
    """Fetch research papers from PubMed with pharma/biotech affiliations.

    QUERY: PubMed search query (supports full PubMed syntax)

    Examples:
        get-papers-list "cancer AND drug discovery"
        get-papers-list "covid-19 AND vaccine" -f results.csv
        get-papers-list "diabetes AND insulin" --debug --max-results 50
    """
    setup_logging(debug)
    logger = logging.getLogger(__name__)

    logger.info(f"Starting PubMed search for query: {query}")

    try:
        # Initialize components
        client = PubMedClient(email=email, api_key=api_key)
        paper_filter = PaperFilter()
        csv_writer = CSVWriter()

        # Search for papers
        logger.info("Fetching papers from PubMed...")
        all_papers = client.search_papers(query, max_results=max_results)

        if not all_papers:
            logger.warning("No papers found for the given query.")
            click.echo("No papers found for the given query.", err=True)
            sys.exit(1)

        logger.info(f"Found {len(all_papers)} total papers")

        # Filter papers with pharmaceutical/biotech affiliations
        logger.info(
            "Filtering papers with pharmaceutical/biotech affiliations..."
        )
        filtered_papers = paper_filter.filter_papers_with_pharma_affiliations(
            all_papers
        )

        if not filtered_papers:
            logger.warning(
                "No papers found with pharmaceutical/biotech affiliations."
            )
            click.echo(
                "No papers found with pharmaceutical/biotech affiliations.",
                err=True,
            )
            sys.exit(1)

        logger.info(
            f"Found {len(filtered_papers)} papers with "
            f"pharmaceutical/biotech affiliations"
        )

        # Generate statistics if debug mode is enabled
        if debug:
            stats = paper_filter.get_paper_statistics(filtered_papers)
            logger.debug(f"Paper statistics: {stats}")

        # Output results
        if file:
            logger.info(f"Writing results to file: {file}")
            with open(file, "w", newline="", encoding="utf-8") as f:
                csv_writer.write_papers_to_csv(filtered_papers, f)
            click.echo(f"Results saved to {file}")
        else:
            logger.info("Writing results to console")
            csv_string = csv_writer.papers_to_csv_string(filtered_papers)
            click.echo(csv_string)

        logger.info("Process completed successfully")

    except PubMedAPIError as e:
        logger.error(f"PubMed API error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if debug:
            import traceback

            traceback.print_exc()
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
