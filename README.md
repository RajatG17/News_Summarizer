
# News Aggregator

A simple Python-based news aggregation agent that fetches top headlines, summarizes them using a local LLM (Gemma-3-12B via llama-cpp), and emails a daily digest. You can schedule it via cron for fully automated delivery.

### Features

* Fetch top headlines from NewsAPI.org

* Summarize each headline with a local Gemma-3-12B model using llama-cpp

* Email the daily digest via SMTP

* Schedule automatic daily runs with cron

### Prerequisites

* Python 3.8+

* Git

* A virtual environment tool (e.g. venv)

* A NewsAPI.org API key

* SMTP credentials (e.g., Gmail, SendGrid) or an HTTP email API key

* Gemma-3-12B GGUF model downloaded locally

### Installation

Clone the repo

<pre>git clone https://github.com/rajatg17/News_Summarizer.git
cd news-aggregator</pre>

### Create & activate a virtual environment

<pre>python -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\Activate.ps1  # Windows PowerShell</pre>

### Install dependencies

`pip install -r requirements.txt`

### Configuration

1. Copy the example env file

    `cp config/.env.example config/.env`

2. Edit config/.env with your keys and settings:

    <pre>
    NEWSAPI_KEY=your_newsapi_key_here
    SUMMARIZER_MODEL_PATH=/full/path/to/causal_model
    EMAIL_SMTP_HOST=smtp.yourprovider.com
    EMAIL_SMTP_PORT=587
    EMAIL_SMTP_USER=your_username
    EMAIL_SMTP_PASS=your_password
    TO_EMAIL=recipient@domain.com
    </pre>

### Usage

#### Fetch and Summarize Once

`python src/main.py --country us --category technology --page-size 10 --keywords AI,NLP`

### CLI Options

| Option | Default | Description |
|--------|---------|------------|
| `--country` | us | 2-letter country code|
| `--category` | technology | News category |
| `--page-size` | 5 | Number of headlines to fetch
| `--keywords` | None | Comma-separated keywords for filtering titles

### Testing

Run unit tests with pytest:

`pytest`

### Scheduling via Cron

1. Open your crontab:

    `crontab -e`

2. Add the following line to run at 8 AM daily:

    `0 8 * * * cd /full/path/to/news-aggregator && /full/path/to/venv/bin/python src/main.py --country us --category technology --page-size 10 >> cron.log 2>&1`