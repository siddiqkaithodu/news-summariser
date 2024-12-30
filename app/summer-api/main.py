import os
import traceback
from redis import StrictRedis, Redis
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from logging import getLogger
from .nytimes_client import get_top_stories
from .story_formatter import format_stories_to_string
from .summariser import summarise_news_stories

BASE_PATH = os.getenv("BASE_PATH", str(Path(__file__).parent / "summer-ui"))
ORIGIN_URL = os.getenv("ORIGIN_URL", "localhost")
REDIS_URL = os.getenv("REDIS_URL", "localhost")
DB = os.getenv("DB", 0)

logger = getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ORIGIN_URL],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=f"{BASE_PATH}/static/"), name="static")
templates = Jinja2Templates(directory=f"{BASE_PATH}/templates")

redis = Redis.from_url(url=REDIS_URL, db=DB, decode_responses=True)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/news")
def news():
    return get_cached() or refresh_news_summary()


def refresh_news_summary():
    logger.info("Refreshing News Summary")
    summary = ""
    images = []
    try:
        stories = get_top_stories()
        for story in stories:
            if story["multimedia"]:
                tmp = story["multimedia"]
                images.extend(tmp)
        summary = summarise_news_stories(format_stories_to_string(stories))
        images = list(
            filter(lambda image: image["format"] == "Large Thumbnail", images)
        )
    except Exception as e:
        error_type = type(e).__name__
        error_message = (
            f"An error occurred while processing the news feed: {error_type}"
        )
        # Log the full error for internal debugging (should go to proper logging system)
        print(f"Error in /news endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=error_message) from e
    json_response = {"summary": summary, "images": images}
    cache_response(json_response)
    return JSONResponse()


def get_cached():
    today = f"{datetime.now():%d%m%y}"
    if today == redis.get("today_date"):
        logger.info(f"Returning Cached Version : {today}")
        return json.loads(redis.get("today_news_summary"))


def cache_response(json_response):
    redis.set("today_news_summary", json.dumps(json_response))
    redis.set("today_date", today)
