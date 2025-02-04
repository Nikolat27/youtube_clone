from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from routers import studio, users, videos, channel, playlist
from fastapi_pagination import add_pagination

websiteUrl = "http://10.202.8.215:8000/"

app = FastAPI()
origins = ["http://localhost", "http://localhost:5000", "http://localhost:8000"]

app.add_middleware(  # Cors middleware
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(studio.router)
app.include_router(videos.router)
app.include_router(channel.router)
app.include_router(playlist.router)

add_pagination(app)
app.mount(
    "/static", StaticFiles(directory="C:/Users/Sam/Desktop/youtube_clone/backend")
)

if __name__ == "__main__":
    uvicorn.run("main:app")
