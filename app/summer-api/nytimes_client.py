import os
import datetime
from pynytimes import NYTAPI
# This is the API Key we setup and added to the env earlier
API_KEY = os.getenv("NYTIMES_API_KEY", "")
nyt = NYTAPI(API_KEY, parse_dates=True)
def get_top_stories():
    return nyt.top_stories()