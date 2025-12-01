from pathlib import Path
from datetime import datetime
from google.adk.tools.tool_context import ToolContext

from .config import OUTPUT_DIR


def save_outputs(tool_context:ToolContext)->dict:
    """Tool to save the contents from state to local paths
    Args:
        none
    Returns:
        dictionary with the local paths of deliverables
    """
    
    state = tool_context.state

    news_digest = state.get('news_digest')
    mna_report = state.get('mna_report')
    infographic_path = state.get('latest_image_local_path')

    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    news_md_path = out_dir / f"news_digest_{ts}.md"
    mna_md_path = out_dir / f"mna_report_{ts}.md"

    if news_digest:
        news_md_path.write_text(news_digest, encoding="utf-8")

    if mna_report:
        mna_md_path.write_text(mna_report, encoding="utf-8")

    return {
        "news_digest_path": str(news_md_path) if news_digest else None,
        "mna_report_path": str(mna_md_path) if mna_report else None,
        "infographic_path": infographic_path,
    }