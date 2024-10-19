from dotenv import load_dotenv
import os
from supabase import create_client, Client
import time
from firecrawl import FirecrawlApp
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Access the variables
MEDIUM_COOKIE = os.getenv('MEDIUM_COOKIE')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')

# Initialize the clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# Create a session with retry logic
session = requests.Session()
retry = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_articles_with_missing_markdown():
    """
    Fetch articles from Supabase where the article_markdown is missing.
    """
    try:
        response = (
            supabase.table('articles')
            .select('medium_url,article_markdown')
            .is_('article_markdown', 'null')
            .eq('to_scrape_md', True)
            .limit(1000)
            .execute()
        )
        return response.data
    except Exception as exception:
        print(f"Error fetching data from Supabase: {exception}")
        return []

def get_markdown_from_url(url: str, cookie: str) -> str:
    params = {
        "headers": {
            "Cookie": cookie
        },
        "onlyMainContent": True,
        "excludeTags": ["#ad", "#footer"],
    }
    try:
        crawl_result = app.scrape_url(url, params=params)
        return crawl_result['markdown']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching markdown for {url}: {e}")
        return None

def update_markdown_in_supabase(medium_url: int, markdown: str):
    """
    Update the article_markdown field in Supabase for a given article ID.
    """
    try:
        response = supabase.table('articles').update({'article_markdown': markdown}).eq('medium_url', medium_url).execute()
        return response
    except Exception as exception:
        print(f"Error updating data in Supabase: {exception}")
        return None

url_list = get_articles_with_missing_markdown()

number_of_articles = len(url_list)
print("number_of_articles :", number_of_articles)

consecutive_failures = 0
max_failures = 6
number_of_articles_scraped = 0

for url in url_list:
    if consecutive_failures >= max_failures:
        print(Fore.RED + "Maximum consecutive failures reached. Aborting.")
        break

    medium_url = url['medium_url']

    # print("scraping:", medium_url)
    markdown = get_markdown_from_url(medium_url, MEDIUM_COOKIE)
    if markdown:
        update_markdown_in_supabase(medium_url, markdown)
        print(Fore.GREEN + f"Updated markdown for article: {medium_url}")
        print(f"#: {number_of_articles_scraped}/{number_of_articles}: %: {number_of_articles_scraped/number_of_articles*100:.2f}")
        consecutive_failures = 0  # Reset the failure counter on success
        number_of_articles_scraped += 1
    else:
        print(Fore.RED + f"Failed to fetch markdown for article: {medium_url}")
        print()
        consecutive_failures += 1
    time.sleep(5)