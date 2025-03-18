## Dev Article Scraper & Analyzer

This project implements a document processing pipeline that extracts content from Dev articles, performs NLP analysis, and generates structured insights.

### Features

- Extract article titles, body content, and comments from Dev articles
- Process text using NLP techniques:

  - Article summarization
  - Topic & keyword extraction
  - Sentiment analysis on comments

- Store results in structured JSON Format

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

- Clone the repository:

```
git clone https://github.com/mehtameet12/MediumArticleScrapper.git
```

- Run the following command to make the setup file executable

```
chmod +x setup.sh
```

- Run the setup file to setup the venv and install dependencies

```
./setup.sh
```

## Running the Application

### Scrapping the data from the website

- In the terminal use the following command to scrape the predinfined dev article:

```
python scrape-article.py
```

- To scrape a specific dev article and name the output file

```
python scrape_article.py "<link to dev article>"
```

This should output a file called `raw_output.json` in the project root.
