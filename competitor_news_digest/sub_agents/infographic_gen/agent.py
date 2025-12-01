import logging
from google.adk.agents import LlmAgent
from google.adk.tools import google_search,ToolContext, load_artifacts


from .tools import generate_image
from .prompt import INFOGRAPHIC_PROMPT

from ...config import MODEL_IMAGE_PROMPTER

logger = logging.getLogger(__name__)

infographic_agent = LlmAgent(
    name="InfographicGenerator",
    model= MODEL_IMAGE_PROMPTER,
    description="Agent with image generation tools",
    instruction=INFOGRAPHIC_PROMPT,
    tools=[generate_image,load_artifacts]
)