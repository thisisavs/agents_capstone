import logging
from google.adk.agents import Agent
from google.adk.tools import google_search # pyright: ignore[reportPrivateImportUsage]

from ...config import MODEL_NEWS_COLLECTOR
from .prompt import NEWS_COLLECTOR_PROMPT_LATEST


logger = logging.getLogger(__name__)


news_collector = Agent(
    name="NewsCollectorAgent",
    model=MODEL_NEWS_COLLECTOR,
    description="An agent that finds and reports on AI agent trends.",
    instruction=NEWS_COLLECTOR_PROMPT_LATEST,
    tools=[google_search],
    output_key='news_digest'
)