import logging
from google.adk.agents import LlmAgent,LoopAgent,SequentialAgent
from google.adk.tools import google_search, FunctionTool
from google.adk.tools.tool_context import ToolContext

from ...config import MODEL_MNA_WRITER,MODEL_CRITIC,MODEL_REFINER

from .prompt import INITIAL_DRAFT_PROMPT, CRITIC_PROMPT,REFINER_PROMPT

logger = logging.getLogger(__name__)

mna_report_writer = LlmAgent(
    name="MNAReportWriter",
    model=MODEL_MNA_WRITER,
    description="agent that drafts the inital M&A report",
    instruction=INITIAL_DRAFT_PROMPT,
    tools=[google_search],
    output_key='mna_report'
)

#TODO: Figure out cant iterate on Nonetype error and fix the pipeline


critic_agent=LlmAgent(
    name="CriticAgent",
    model=MODEL_CRITIC,
    instruction=CRITIC_PROMPT,
    description="Reviews the current M&A report draft and returns focused critique or signals completion",
    tools=[google_search],
    output_key='criticism'
)

# Exit Loop Tool 
def exit_loop(tool_context:ToolContext):
    """Call this function ONLY when the critique is 'APPROVED', indicating the report is ready and no more changes are needed."""
    #tool_context.actions.escalate=True
    tool_context.actions.transfer_to_agent = "CompetitorNewsDigest"
    return {
        "status":"APPROVED",
        'message':'Report Approved exit the refinement loop'
        }

refiner_agent=LlmAgent(
    name="RefinerAgent",
    model=MODEL_REFINER,
    instruction=REFINER_PROMPT,
    description="Refines the M&A report based on the critic's feedback, or exits the loop when no major issues remain",    
    tools=[exit_loop]
)

refinement_loop = LoopAgent(
    name="MNAReportRefinement",
    sub_agents=[critic_agent,refiner_agent],
    max_iterations=2
)

mna_report_pipeline = SequentialAgent(
    name="MNAReportPipeline",
    sub_agents=[mna_report_writer,refinement_loop],
    description="Writes inital M&A Report and then iteratively refines it with critique using exit tool"   
)