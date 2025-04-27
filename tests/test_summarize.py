import pytest
import os, sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables from .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to the project root, then into config/.env
env_path = os.path.join(current_dir, "..", "config", ".env")
if not os.path.exists(env_path):
    raise FileNotFoundError(f"Environment file {env_path} not found.")
else:
    print(f"Loading environment variables from {env_path}")
load_dotenv(dotenv_path=env_path)

from src.summarize import summarize_article


class DummyLlama:
    def __call__(self, prompt, max_tokens=None, echo=None):
        return {
            "choices": [
                {
                    "text": "This is a dummy summary of the article."
                }
            ]
        }

@pytest.fixture(autouse=True)
def patch_llm(monkeypatch):
    """
    Patch the Llama class to use a dummy implementation for testing.
    """
    import src.summarize
    monkeypatch.setattr(src.summarize, "llm", DummyLlama())
    yield

def test_summarize_article():
    """
    Test the summarize_article function.
    """
    text = "This is a test article content that needs to be summarized."
    summary = summarize_article(text)
    assert summary == "This is a dummy summary of the article."
    