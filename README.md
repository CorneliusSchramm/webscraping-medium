# Webscraping Medium Articles

## Setup Instructions

1. **Create a virtual environment**:
```bash
python3 -m venv .venv
```

2. **Activate the virtual environment**:
```bash
source .venv/bin/activate
```

3. **Install the requirements**:
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file**  similar to the provided `.env-example` file.
## Description
- The `.env` file is used to store environment variables.
- The `requirements.txt` file contains all the dependencies required to run the project.
- The `src` directory contains the main source code for the project.
    - **[`src/get_article_content.py`](src/get_article_content.py)**: Contains the function `update_markdown_in_supabase` which updates the `article_markdown` field in Supabase for a given article ID.
    - **[`src/medium_scraper_metadata.py`](src/medium_scraper_metadata.py)**: Contains functions to fetch data from the Medium API and insert metadata into Supabase. It uses environment variables for configuration and includes a list of tags to scrape.
- To run the project, execute the following command:
```bash
python3 src/get_article_content.py
```