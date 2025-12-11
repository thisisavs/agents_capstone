import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from google.adk.agents import LlmAgent
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.news_collector import news_collector
from .sub_agents.mna_report import mna_report_pipeline
from .sub_agents.infographic_gen import infographic_agent

from .config import MODEL_NEWS_ORCHESTRATOR
from .tools import save_outputs
from .prompt import NEWS_DIGEST_PROMPT


news_orchestrator = LlmAgent(
    name="CompetitorNewsDigest",
    model=MODEL_NEWS_ORCHESTRATOR,    
    instruction=NEWS_DIGEST_PROMPT,    
    sub_agents=[mna_report_pipeline, infographic_agent],
    tools = [
        AgentTool(agent=news_collector),
        FunctionTool(save_outputs)
    ]
)

"""
news_orchestrator = LlmAgent(
    name="CompetitorNewsDigest",
    model=MODEL_NEWS_ORCHESTRATOR,    
    instruction=NEWS_DIGEST_PROMPT,    
    tools = [
        AgentTool(agent=news_collector),
        AgentTool(agent=mna_report_writer),
        AgentTool(agent=infographic_agent),
        FunctionTool(save_outputs)
    ]
)

"""

root_agent = news_orchestrator