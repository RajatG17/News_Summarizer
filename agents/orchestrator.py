import os
import asyncio
import aiosmtplib

from dotenv import load_dotenv
from google.adk.agents import SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.fetcher import FetcherAgent
from agents.summarizer import SummarizerAgent
from email.message import EmailMessage

# Load environment variables
dotenv_path= os.getenv("DOTENV_PATH", ".env")
load_dotenv(dotenv_path)

# Setting up the llm client
from google.cloud import aiplatform
aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
llm_client = aiplatform

FEEDS = [
    "https://rss.nytimes.com.services/xml/nyt/HomePage.xml",
]

async def send_email(summaries):
    msg = EmailMessage()
    msg["Subject"] = "Morning News Digest"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_USER")
    msg.set_content("\n\n".join(summaries))

    await aiosmtplib.send(
        msg,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT", 587)),
        start_tls=True,
        username=os.getenv("EMAIL_USER"),
        password=os.getenv("EMAIL_PASS")
    )

async def main():
    # Initialize agent instances
    fetcher = FetcherAgent(llm=llm_client, feeds=FEEDS)
    summarizer = SummarizerAgent(llm=llm_client)

    # Sequential workflow agent
    pipeline = SequentialAgent(
        name="news_digest_pipeline",
        sub_agents=[fetcher, summarizer]
    )

    # Runner and in-memory session
    session_service = InMemorySessionService()
    runner = Runner(agent=pipeline, session_service=session_service)

    #Execute pipeline
    result = await runner.run_async()
    # result will hold the final output from summarizer

    await send_email(result)

if __name__ == "__main__":
    asyncio.run(main())

# Next steps:
# -Configuing "llm_client" with provider
# - Testing sub-agents in REPL
# - Schedule orchestrator with 'schedule' lib or cron job