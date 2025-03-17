## Medium Article Scraper & Analyzer
This project implements a document processing pipeline that extracts content from Medium articles, performs NLP analysis, and generates structured insights.

### Features
- Extract article titles, body content, and comments from Medium articles
- Process text using NLP techniques:
    -  Article summarization
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

- Create and activate virtual environment
```
python -m venv mediumArticle
source mediumArticle/bin/activate
```

- Install the requirements file
``` 
pip install -r requirements.txt
```

## Running the Application

- In the terminal use the following command to scrape the predinfined medium article:

```
python scrape-article.py
```

- To scrape a specific medium article and name the output file
```
python scrape_article.py "<link to medium article>" "<output-file-name.json>"
```
