
import requests_mock
import os
from dotenv import load_dotenv
# Load environment variables from .env file
print(os.getcwd())
env_path = os.path.join(os.getcwd(), "config/.env")
if not os.path.exists(env_path):
    raise FileNotFoundError(f"Environment file {env_path} not found.")
else:
    print(f"Loading environment variables from {env_path}")
load_dotenv(dotenv_path=env_path)

from src.fetch import fetch_top_headlines


def test_fetch_and_normalize(requests_mock):
    mock_url = "https://newsapi.org/v2/top-headlines"
    requests_mock.get(mock_url, json={
        "articles": [
          {"title": "Foo News", "url": "http://a"},
          {"title": "Foo News", "url": "http://a"},
          {"title": "Bar News", "url": "http://b"},
        ]
    })
    items = fetch_top_headlines(page_size=3, keywords=["Bar"])
    assert len(items) == 1
    assert items[0]["title"] == "Bar News"