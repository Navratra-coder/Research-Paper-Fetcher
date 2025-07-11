#!/bin/bash
"""
Setup script for the PubMed Pharmaceutical Papers Fetcher project.

This script initializes the project, installs dependencies, and runs basic tests.
"""

echo "PubMed Pharmaceutical Papers Fetcher - Setup Script"
echo "=================================================="

# Create directories if they don't exist
mkdir -p scripts examples

# Initialize Git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: PubMed Pharmaceutical Papers Fetcher"
fi

# Install dependencies with Poetry
echo "Installing dependencies with Poetry..."
if command -v poetry &> /dev/null; then
    poetry install
    echo "Dependencies installed successfully!"
else
    echo "Poetry not found. Please install Poetry first:"
    echo "curl -sSL https://install.python-poetry.org | python3 -"
    echo ""
    echo "Alternative: Install using pip:"
    echo "pip install -e ."
fi

# Run tests
echo "Running tests..."
if command -v poetry &> /dev/null; then
    poetry run pytest tests/ -v
else
    python -m pytest tests/ -v
fi

# Display usage information
echo ""
echo "Setup complete! Here's how to use the program:"
echo ""
echo "1. Command-line usage:"
echo "   get-papers-list \"cancer AND drug discovery\" -f results.csv"
echo ""
echo "2. Python module usage:"
echo "   python examples/example_usage.py"
echo ""
echo "3. Run tests:"
echo "   poetry run pytest  # or python -m pytest"
echo ""
echo "4. Format code:"
echo "   poetry run black pubmed_pharma_papers/ tests/"
echo ""
echo "5. Type checking:"
echo "   poetry run mypy pubmed_pharma_papers/"
echo ""
echo "For more information, see README.md" 