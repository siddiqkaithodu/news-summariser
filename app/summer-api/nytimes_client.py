import os
from pynytimes import NYTAPI

API_KEY = os.getenv("NYTIMES_API_KEY", "")
nyt = NYTAPI(API_KEY, parse_dates=True)


def get_top_stories():
    return nyt.top_stories()
