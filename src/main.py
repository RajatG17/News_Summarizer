# Main logic for the application
import os
import argparse

from dotenv import load_dotenv
# Load environment variables from .env file
print(os.getcwd())
# Get the directory of the current file (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to the project root, then into config/.env
env_path = os.path.join(current_dir, "..", "config", ".env")
# env_path = os.path.join(os.getcwd(), "config/.env")
if not os.path.exists(env_path):
    raise FileNotFoundError(f"Environment file {env_path} not found.")
else:
    print(f"Loading environment variables from {env_path}")
load_dotenv(dotenv_path=env_path)

from send_email import send_report
from fetch import fetch_top_headlines
from summarize import summarize_article


def main(country:str, category:str, page_size:int, keywords: list[str] | None):
    items = fetch_top_headlines(
        category=category,
        country=country, 
        page_size=page_size,
        keywords=keywords
    )

    summaries = [{"title": art["title"], "url": art["url"], "summary": summarize_article(art["title"])} for art in items]

    for i, art in enumerate(summaries):
        print(f"{i+1}, {art['title']} - {art['url']}\n {art['summary']}\n\n")

    send_report(summaries)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Fetch and summarize news articles.")
    parser.add_argument("--category", type=str, default="technology", help="Category of news articles to fetch.")
    parser.add_argument("--country", type=str, default="us", help="Country code for news articles.")
    parser.add_argument("--page_size", type=int, default=5, help="Number of articles to fetch.")
    parser.add_argument("--keywords", type=lambda s: s.split(","), default=None, help="keywords to filter articles.")
    args = parser.parse_args()

    main(
        country=args.country, 
        category=args.category, 
        page_size=args.page_size,
        keywords=args.keywords
    )
