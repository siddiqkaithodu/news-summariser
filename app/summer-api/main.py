import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from .nytimes_client import get_top_stories
from .story_formatter import format_stories_to_string
from .summariser import summarise_news_stories

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
def index():
    return {"msg": "Welcome to the News App"}


@app.get("/news")
def news():
    summary = ""
    images = []
    print("here")
    try:
        # print("here")
        stories = get_top_stories()
        print("recievd")
        for story in stories:
            if story["multimedia"]:
                tmp = story["multimedia"]
                images.extend(tmp)
        summary = summarise_news_stories(format_stories_to_string(stories))
        images = list(
            filter(lambda image: image["format"] == "Large Thumbnail", images)
        )
    except Exception as e:
        import traceback;traceback.print_exc()
        raise HTTPException(
            status_code=500, detail="Apologies, something bad happened :("
        )
    return {"summary": summary, "images": images}