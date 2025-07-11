# 🧬 PubMed Pharmaceutical Papers Fetcher 🔬

A Python project to fetch research papers from PubMed that have at least one author affiliated with a pharmaceutical or biotech company. The program returns results as a **CSV file** with detailed information about non-academic authors and their company affiliations.

-----

## ✨ Features ✨

  - **PubMed API Integration**: 🔗 Fetch papers using the official PubMed API with full query syntax support.
  - **Smart Filtering**: 🧠 Identify pharmaceutical/biotech company affiliations using comprehensive keyword matching.
  - **CSV Export**: 📊 Export results with required columns (PubMed ID, Title, Publication Date, Non-academic Authors, Company Affiliations, Corresponding Author Email).
  - **Command-line Interface**: 💻 Easy-to-use CLI with helpful options and debug mode.
  - **Modular Design**: 🧩 Clean separation of concerns with reusable components.
  - **Type Safety**: ✅ Fully typed Python code with `mypy` compatibility.
  - **Error Handling**: 🚧 Robust error handling for API failures and invalid queries.

-----

## ⬇️ Installation ⬇️

### Using Poetry (Recommended) 🚀

```bash
# Clone the repository
git clone https://github.com/navratra/pubmed-pharma-papers.git
cd pubmed-pharma-papers

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Using pip 🐍

```bash
# Clone the repository
git clone https://github.com/navratra/pubmed-pharma-papers.git
cd pubmed-pharma-papers

# Install in development mode
pip install -e .
```

-----

## 💡 Usage 💡

### Command Line Interface 🚀

The program provides a command-line tool called `get-papers-list`:

```bash
# Basic usage
get-papers-list "cancer AND drug discovery"

# Save results to a file
get-papers-list "covid-19 AND vaccine" -f results.csv

# Enable debug mode for detailed logging
get-papers-list "diabetes AND insulin" --debug

# Limit the number of results
get-papers-list "alzheimer AND treatment" --max-results 50

# Use with email for better API rate limits
get-papers-list "heart disease AND therapy" --email your.email@example.com
```

### Command Line Options ⚙️

  - `QUERY`: PubMed search query (required) - supports full PubMed syntax
  - `-f, --file`: Specify filename to save results (optional, prints to console if not provided) 📄
  - `-d, --debug`: Enable debug logging 🐛
  - `--max-results`: Maximum number of results to fetch (default: 100) 🔢
  - `--email`: Email address for NCBI API identification (recommended) 📧
  - `--api-key`: NCBI API key for increased rate limits 🔑
  - `-h, --help`: Show help message ❓
  - `--version`: Show version information ℹ️

### Python Module Usage 📖

You can also use the components as a Python module:

```python
from pubmed_pharma_papers import PubMedClient, PaperFilter, CSVWriter

# Initialize components
client = PubMedClient(email="your.email@example.com")
paper_filter = PaperFilter()
csv_writer = CSVWriter()

# Search for papers
papers = client.search_papers("cancer AND immunotherapy", max_results=50)

# Filter papers with pharmaceutical affiliations
filtered_papers = paper_filter.filter_papers_with_pharma_affiliations(papers)

# Export to CSV
with open("results.csv", "w") as f:
    csv_writer.write_papers_to_csv(filtered_papers, f)
```

-----

## 📈 Output Format 📊

The program outputs a CSV file with the following columns:

1.  **PubmedID**: Unique identifier for the paper 🆔
2.  **Title**: Title of the paper 📝
3.  **Publication Date**: Date the paper was published (YYYY-MM-DD format) 🗓️
4.  **Non-academic Author(s)**: Names of authors affiliated with non-academic institutions (semicolon-separated) 🧑‍🔬
5.  **Company Affiliation(s)**: Names of pharmaceutical/biotech companies (semicolon-separated) 🏢
6.  **Corresponding Author Email**: Email address of the corresponding author ✉️

-----

## 📂 Code Organization 📂

```
pubmed-pharma-papers/
├── pubmed_pharma_papers/             # Main package
│   ├── __init__.py                   # Package initialization
│   ├── models.py                     # Data models (Paper, Author)
│   ├── pubmed_client.py              # PubMed API client
│   ├── paper_filter.py               # Filtering logic
│   ├── csv_writer.py                 # CSV output handling
│   └── cli.py                        # Command-line interface
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── test_models.py
│   └── test_paper_filter.py
├── pyproject.toml                    # Poetry configuration
└── README.md                         # This file
```

### Key Components 🛠️

  - **`PubMedClient`**: Handles API communication with PubMed 📡
  - **`PaperFilter`**: Identifies pharmaceutical/biotech company affiliations 🔍
  - **`CSVWriter`**: Formats and exports results to CSV ✍️
  - **`Paper` & `Author`**: Data models with validation and utility methods 🧑‍💻
  - **`CLI`**: Command-line interface built with Click 🚀

-----

## 🧠 Algorithm for Identifying Non-Academic Authors 🔬

The program uses a comprehensive approach to identify pharmaceutical/biotech company affiliations:

1.  **Known Company Names**: Matches against a curated list of major pharmaceutical and biotech companies 📜
2.  **Industry Keywords**: Identifies affiliations containing terms like "pharmaceutical", "biotech", "therapeutics" 🔬
3.  **Company Structure Keywords**: Looks for corporate indicators like "Inc.", "Corp.", "Ltd." 🏢
4.  **Academic Exclusion**: Excludes affiliations with academic terms like "university", "college", "institute" 🚫

-----

## 🧪 Testing 🧪

Run the test suite using `pytest`:

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=pubmed_pharma_papers

# Run specific test file
poetry run pytest tests/test_models.py
```

-----

## 🧑‍💻 Development 🧑‍💻

### Code Quality ✨

The project uses several tools for code quality:

```bash
# Format code with black
poetry run black pubmed_pharma_papers/ tests/

# Lint with flake8
poetry run flake8 pubmed_pharma_papers/ tests/

# Type checking with mypy
poetry run mypy pubmed_pharma_papers/
```

### Dependencies 📦

  - **requests**: HTTP client for API calls 🌐
  - **xmltodict**: XML parsing for PubMed responses 🧩
  - **click**: Command-line interface framework ⚡
  - **pandas**: Data manipulation (CSV handling) 🐼
  - **email-validator**: Email validation ✅

-----

## 🚦 API Rate Limits 🚦

The program implements rate limiting to comply with NCBI's usage policies:

  - Maximum 3 requests per second without API key ⏱️
  - Recommends providing an email address for identification 📧
  - Supports API keys for increased rate limits 🚀

-----

## ⚠️ Error Handling ⚠️

The program includes robust error handling for:

  - Invalid PubMed queries ❌
  - API failures and timeouts ⏳
  - Network connectivity issues 🌐
  - Malformed XML responses 🐛
  - Missing or invalid data fields 🚫

-----

## 🤝 External Tools Used 🤝

This project was developed with assistance from:

  - **Claude AI**: Code generation and architecture design 🤖
  - **GitHub Copilot**: Code completion and suggestions 🧑‍✈️
  - **Poetry**: Dependency management and packaging 📦
  - **pytest**: Testing framework 🧪
  - **Black**: Code formatting ⚫
  - **mypy**: Type checking 🐍

-----

## 💖 Contributing 💖

1.  Fork the repository 🍴
2.  Create a feature branch 🌱
3.  Make your changes ✍️
4.  Add tests for new functionality 🧪
5.  Ensure all tests pass ✅
6.  Format code with black ⚫
7.  Submit a pull request 🚀

-----

## 📄 License 📄

MIT License - see LICENSE file for details.

-----

## ❓ Support ❓

For issues and questions:

1.  Check the existing GitHub issues 🔍
2.  Create a new issue with detailed description ➕
3.  Include debug output when reporting bugs 🐛

-----

## 📜 Changelog 📜

### Version 0.1.0 - 🚀 Initial Release

  - PubMed API integration
  - Pharmaceutical/biotech company filtering
  - CSV export functionality
  - Command-line interface
  - Comprehensive test suite

-----
