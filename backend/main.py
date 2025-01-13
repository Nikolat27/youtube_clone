from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from routers import studio, users, videos, channel, playlist
from fastapi_pagination import add_pagination

app = FastAPI()

origins = ["http://localhost", "http://localhost:5000", "http://localhost:8000"]

app.add_middleware(  # Cors middleware
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

secret_key = "m($59=%u3#8lkvi)wy!j)6-$h*h=(eir(4y#b87^0&^hj660kh"
app.add_middleware(
    SessionMiddleware, secret_key=secret_key, max_age=2 * 24 * 60 * 60  # Days
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
