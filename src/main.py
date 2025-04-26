# Main logic for the application
import os
import argparse






from dotenv import load_dotenv
# Load environment variables from .env file
print(os.getcwd())
env_path = os.path.join(os.getcwd(), "config/.env")
if not os.path.exists(env_path):
    raise FileNotFoundError(f"Environment file {env_path} not found.")
else:
    print(f"Loading environment variables from {env_path}")
load_dotenv(dotenv_path=env_path)

from fetch import fetch_top_headlines



def main(country:str, category:str, page_size:int, keywords: list[str] | None):
    items = fetch_top_headlines(
        category=category,
        country=country, 
        page_size=page_size,
        keywords=keywords
        )

    for i, art in enumerate(items):
        print(art)
        print(f"{i+1}, {art['title']} - {art['url']} \n\n")

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Fetch and summarize news articles.")
    parser.add_argument("--category", type=str, default="technology", help="Category of news articles to fetch.")
    parser.add_argument("--country", type=str, default="us", help="Country code for news articles.")
    parser.add_argument("--page_size", type=int, default=10, help="Number of articles to fetch.")
    parser.add_argument("--keywords", type=lambda s: s.split(","), default=None, help="keywords to filter articles.")
    args = parser.parse_args()

    main(
        country=args.country, 
        category=args.category, 
        page_size=args.page_size,
        keywords=args.keywords
    )
