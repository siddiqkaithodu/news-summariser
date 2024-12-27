import os
import traceback
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from .nytimes_client import get_top_stories
from .story_formatter import format_stories_to_string
from .summariser import summarise_news_stories

path = os.getenv("PATH", str(Path(__file__).parent / "summer-ui"))
origin = os.getenv("ORIGIN", "localhost")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/summer-ui/static/"), name="static")
templates = Jinja2Templates(directory="app/summer-ui/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/news")
def news():
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
    return JSONResponse({"summary": summary, "images": images})
