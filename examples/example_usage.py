#!/usr/bin/env python3
"""
Example usage of the PubMed Pharmaceutical Papers Fetcher.

This script demonstrates how to use the pubmed_pharma_papers module
to search for papers and filter them for pharmaceutical/biotech affiliations.
"""

import logging
from pathlib import Path
from pubmed_pharma_papers import PubMedClient, PaperFilter, CSVWriter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def main():
    """Main example function."""
    print("PubMed Pharmaceutical Papers Fetcher - Example Usage")
    print("=" * 50)

    # Initialize components
    print("\n1. Initializing components...")
    client = PubMedClient(
        email="your.email@example.com"
    )  # Replace with your email
    paper_filter = PaperFilter()
    csv_writer = CSVWriter()

    # Search for papers
    print("\n2. Searching for papers...")
    query = "cancer AND immunotherapy"
    max_results = 20  # Small number for demonstration

    print(f"Query: {query}")
    print(f"Max results: {max_results}")

    try:
        all_papers = client.search_papers(query, max_results=max_results)
        print(f"Found {len(all_papers)} total papers")

        if not all_papers:
            print("No papers found. Try a different query.")
            return

        # Filter papers with pharmaceutical/biotech affiliations
        print(
            "\n3. Filtering papers with pharmaceutical/biotech affiliations..."
        )
        filtered_papers = paper_filter.filter_papers_with_pharma_affiliations(
            all_papers
        )
        print(
            f"Found {len(filtered_papers)} papers with pharmaceutical/biotech affiliations"
        )

        if not filtered_papers:
            print("No papers found with pharmaceutical/biotech affiliations.")
            return

        # Display some information about the filtered papers
        print("\n4. Sample results:")
        for i, paper in enumerate(filtered_papers[:3]):  # Show first 3 papers
            print(f"\nPaper {i+1}:")
            print(f"  PubMed ID: {paper.pubmed_id}")
            print(f"  Title: {paper.title[:80]}...")
            print(f"  Publication Date: {paper.publication_date}")

            non_academic_authors = paper.get_non_academic_authors()
            if non_academic_authors:
                print(
                    f"  Non-academic Authors: {', '.join([a.name for a in non_academic_authors])}"
                )
                print(
                    f"  Company Affiliations: {', '.join(paper.get_company_affiliations())}"
                )

        # Get statistics
        print("\n5. Statistics:")
        stats = paper_filter.get_paper_statistics(filtered_papers)
        print(f"  Total papers: {stats['total_papers']}")
        print(
            f"  Papers with pharma affiliations: {stats['papers_with_pharma_affiliations']}"
        )
        print(
            f"  Total non-academic authors: {stats['total_non_academic_authors']}"
        )
        print(f"  Unique companies: {stats['unique_companies']}")
        print(
            f"  Papers with corresponding emails: {stats['papers_with_corresponding_mails']}"
        )

        # Export to CSV
        print("\n6. Exporting results...")
        output_file = Path("example_results.csv")
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            csv_writer.write_papers_to_csv(filtered_papers, f)

        print(f"Results exported to: {output_file}")
        print(f"Total records: {len(filtered_papers)}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
