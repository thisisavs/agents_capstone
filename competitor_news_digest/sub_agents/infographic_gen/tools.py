from google.genai import types, Client
from google.adk.tools import ToolContext
import datetime
import os
import json

from ...config import OUTPUT_DIR


# ------------------------------------------------------------------------------
# NANO BANANA PRO MODEL CONFIGURATION
# ------------------------------------------------------------------------------

MODEL_IMAGE = "gemini-3-pro-image-preview"
aspect_ratio = "9:16" # ["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"] A4 size : "1 : 1.414" not working.TODO: maybe commentout in config and ask in prompt
resolution = "2K" # "1K", "2K", "4K"


TASK = """
You are an expert infographic generator agent responsible for generating high impact clean infographics for the C-Suite audience. 
Below you will be given details about a merger which happened and Your task is to generate infographics that will help busy executives learn about this merger at a glance. 
The infographic should include textual elements that summarize key bullet points from the report along with  appropriate visuals. 
The infographic should include transaction highlights convey the strategic synergy, market impact, and future outlook. 
You can lookup for the company logos, etc but **DO NOT MAKEUP LOGOS**. Use text if you cant find logos.
**M&A REPORT:**

"""

async def generate_image(img_prompt: str, tool_context: ToolContext):
    """Generates an image based on the prompt."""
    client = Client()
    response = client.models.generate_content(
        model=MODEL_IMAGE,
        contents=[TASK+img_prompt],
        config=types.GenerateContentConfig(
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution
            ),
        ),        
    )    
    
    image_bytes=None
    mime_type=None
    
    if not response.candidates:
        return {"status": "failed",}       
    
    image_obj = response.candidates[0].content.parts[0].as_image()
    image_bytes = image_obj.image_bytes
    mime_type = image_obj.mime_type
    ext = mime_type.split("/")[1]
    
    
    filename = f"nano_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.{ext}"    
    await tool_context.save_artifact(
        filename,
        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
    )
    #TODO: save into local directory
    os.makedirs(OUTPUT_DIR,exist_ok=True)
    local_path = os.path.join(OUTPUT_DIR,filename)
    with open(local_path,"wb") as f:
        f.write(image_bytes)
    
    tool_context.state['latest_image_local_path'] = local_path # save latest path as state variable

    record = {
        'file_name':filename,
        'img_prompt':img_prompt,
        'localpath':local_path
    }
    
    qc_path = os.path.join(OUTPUT_DIR,"image_qc.jsonl")
    with open(qc_path,"a",encoding="utf-8") as f:
        f.write(json.dumps(record))
        f.write("\n")

    return {
        "status": "success",
        "detail": "Image generated successfully and stored in artifacts.",
        "fileName": filename,
        "localPath":local_path
    }