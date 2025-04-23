import feedparser
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

class FetcherAgent(LlmAgent):
    """
    fetcher Agent: fetches and parses RSS feeds.
    """
    def  __init__(self, llm, name="fetcher", feeds=None, num_entries=5):
        # llm: a LLM client (Gemini or ChatGPT)
        # feeds: list of RSS feed URLs
        # num_entries: No. of headlines to parse
        super().__init__(name=name, llm=llm)
        self.feeds = feeds or []
        self.num_entries = num_entries

    def fetch(self):
        """

        :return: a list of dicts: [{"title": ..., "link":..., "summary": ...}, ..]"
        """
        items = []
        for url in self.feeds:
            parsed = feedparser.parse(url)
            for entry in parsed.entries[:self.num_entries]:
                items.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "description": entry.get("summary", "")

                })

        return items
