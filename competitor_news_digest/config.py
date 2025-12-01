from google.genai import types
from google.adk.models.google_llm import Gemini


retry_config=types.HttpRetryOptions(
    attempts=5,
    exp_base=5,
    initial_delay=1,
    http_status_codes=[429,500,503,504]
)

# ------------------------------------------------------------------------------
# MODELS CONFIGURATION
# ------------------------------------------------------------------------------
MODEL_NEWS_ORCHESTRATOR= Gemini(
    model='gemini-2.5-pro-preview-06-05', # [ 'gemini-3-pro-preview' , 'gemini-2.5-pro-preview-06-05' , 'gemini-2.5-flash']
    retry_options=retry_config
)

MODEL_NEWS_COLLECTOR= Gemini(
    model='gemini-2.5-pro-preview-06-05', # [ 'gemini-3-pro-preview' , 'gemini-2.5-pro-preview-06-05' , 'gemini-2.5-flash']
    retry_options=retry_config
)

MODEL_MNA_WRITER= Gemini(
    model='gemini-3-pro-preview', # [ 'gemini-3-pro-preview' , 'gemini-2.5-pro-preview-06-05' , 'gemini-2.5-flash']
    retry_options=retry_config
)

MODEL_CRITIC= Gemini(
    model='gemini-2.5-pro-preview-06-05', # [ 'gemini-3-pro-preview' , 'gemini-2.5-pro-preview-06-05' , 'gemini-2.5-flash']
    retry_options=retry_config
)

MODEL_REFINER= Gemini(
    model='gemini-2.5-pro-preview-06-05', # [ 'gemini-3-pro-preview' , 'gemini-2.5-pro-preview-06-05' , 'gemini-2.5-flash']
    retry_options=retry_config
)

MODEL_IMAGE_PROMPTER= Gemini(
    model='gemini-2.5-pro-preview-06-05', # [ 'gemini-3-pro-preview' , 'gemini-2.5-pro-preview-06-05' , 'gemini-2.5-flash']
    retry_options=retry_config
)

MODEL_EMAIL= Gemini(
    model='gemini-2.5-pro-preview-06-05', # [ 'gemini-3-pro-preview' , 'gemini-2.5-pro-preview-06-05' , 'gemini-2.5-flash']
    retry_options=retry_config
)

# ------------------------------------------------------------------------------
# State Variable Keys
# ------------------------------------------------------------------------------

'news_digest' # The output of news_collector agent. This contains the news summary 
'mna_report' # Detailed M&A Report
'criticism' # Criticism of the M&A Report
'latest_image_local_path' #latest infographic path


# ------------------------------------------------------------------------------
# Deliverables Folder
# ------------------------------------------------------------------------------

OUTPUT_DIR="Deliverables"