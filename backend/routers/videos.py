from fastapi import APIRouter, Path, status, Query, Header
from database.models.base import session
from database.models.user import Video, User
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from sqlalchemy import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime
from pymediainfo import MediaInfo
from pathlib import Path
import speedtest
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor
import asyncio

router = APIRouter(prefix="/videos", tags=["videos"])


async def get_video_duration(file):  # Using pymediainfo (This is faster)
    media_info = MediaInfo.parse(file)
    return media_info.tracks[0].duration // 1000  # coverting Ms to S


async def time_difference(created_time):
    current_time = datetime.now()
    time_difference = current_time.date() - created_time.date()
    return time_difference.days


async def static_file(file_url):
    return f"http://127.0.0.1:8000/static/{file_url}"


@router.get("/generate/fake")
def generate_fake_data():
    title = "Hello world"
    video_type = "long_video"
    file_name = ""
    file_url = ""
    thumbnail_url = "uploaded_videos/3/thumbnail/pic1.jpg"

    for i in range(100):
        video = Video(
            title=f"{title} {i + 1}",
            user_id=3,
            video_type=video_type,
            file_name=file_name,
            file_url=file_url,
            thumbnail_url=thumbnail_url,
        )
        session.add(video)
        session.commit()


@router.get("/")
async def videos_list() -> Page:
    long_videos = paginate(
        session,
        select(
            Video.id,
            Video.title,
            Video.thumbnail_url,
            Video.created_at,
            Video.user_id,
        )
        .where(Video.video_type == "long_video")
        .order_by(Video.created_at),
    )

    short_videos = (
        Video.query.with_entities(Video.id, Video.title, Video.thumbnail_url)
        .filter_by(video_type="short_video")
        .limit(12)
        .all()
    )

    response_data = {
        "long_videos": {
            "total": long_videos.total,
            "page": long_videos.page,
            "size": long_videos.size,
            "pages": long_videos.pages,
            "items": [
                {
                    "id": video.id,
                    "title": video.title,
                    "thumbnail_url": await static_file(video.thumbnail_url),
                    "created_at": f"{await time_difference(video.created_at)} days",
                }
                for video in long_videos.items
            ],
        },
        "short_videos": [
            {
                "id": video.id,
                "title": video.title,
                "thumbnail_url": await static_file(video.thumbnail_url),
            }
            for video in short_videos
        ],
    }

    return JSONResponse({"data": response_data}, status_code=status.HTTP_200_OK)


def get_channel_name(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.channel.name or user.username


def get_channel_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    return f"http://127.0.0.1:8000/static/{user.channel.profile_picture_url}"


@router.get("/load-more")
async def load_more_videos() -> Page:
    long_videos = paginate(
        session,
        select(
            Video.id,
            Video.title,
            Video.thumbnail_url,
            Video.created_at,
            Video.user_id,
        )
        .where(Video.video_type == "long_video")
        .order_by(Video.created_at),
    )
    response_data = {
        "long_videos": {
            "total": long_videos.total,
            "page": long_videos.page,
            "size": long_videos.size,
            "pages": long_videos.pages,
            "items": [
                {
                    "id": video.id,
                    "title": video.title,
                    "thumbnail_url": await static_file(video.thumbnail_url),
                    "created_at": f"{await time_difference(video.created_at)} days",
                    "channel_name": get_channel_name(video.user_id),
                    "channel_profile": get_channel_profile(video.user_id),
                }
                for video in long_videos.items
            ],
        }
    }

    return JSONResponse({"data": response_data}, status_code=status.HTTP_200_OK)


@router.get("/detail/{video_id}")
async def video_detail(video_id: int = Path()):
    video = (
        Video.query.with_entities(
            Video.id,
            Video.user_id,
            Video.title,
            Video.description,
            Video.file_url,
            Video.thumbnail_url,
            Video.created_at,
        )
        .filter_by(id=video_id)
        .first()
    )

    serializer = {
        "id": video.id,
        "title": video.title,
        "user_id": video.user_id,
        "description": video.description or "asdfasdfasdf",
        "file_url": await static_file(video.file_url),
        "thumbnail_url": await static_file(video.thumbnail_url),
        "duration": await get_video_duration(video.file_url),
        "created_at": f"{await time_difference(video.created_at)} days ",
    }

    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/internet-speed")
async def get_internet_speed():
    users_speed = speedtest.Speedtest().download()
    return round(users_speed / 1024 / 1024 / 8)


CHUNK_SIZE = 1024 * 1024


@router.get("/stream/{video_id}/")
async def video_stream(video_id: int = Path(), range: str = Header(None)):
    video = Video.query.with_entities(Video.file_url).filter_by(id=video_id).first()
    video_path = Path(f"{video.file_url}").resolve()

    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE

    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            "Content-Range": f"bytes {str(start)}-{str(end)}/{filesize}",
            "Accept-Ranges": "bytes",
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")


@router.get("/frame/{video_id}")
async def get_video_frame(video_id: int = Path(), duration: str = Query()):
    img_output_path = Path(r"uploaded_videos\3\video_frame\videoframe.png").absolute()
    src_video_path = Path(r"uploaded_videos\3\long_video\redmagic-video.mp4").absolute()
    duration = duration
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        duration,
        "-i",
        src_video_path,
        "-vframes",
        "1",
        "-vf",
        "scale=225:130",
        img_output_path,
    ]
    subprocess.run(command, check=True)
    return {
        "data": r"http://127.0.0.1:8000/static/uploaded_videos\3\video_frame\videoframe.png"
    }
