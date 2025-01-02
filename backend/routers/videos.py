from fastapi import APIRouter, Path, status, Query
from database.models.base import session
from database.models.user import Video, User
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime

router = APIRouter(prefix="/videos", tags=["videos"])


async def time_difference(created_time):
    current_time = datetime.now()
    time_difference = current_time.date() - created_time.date()
    return time_difference.days


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
                    "thumbnail_url": f"http://127.0.0.1:8000/static/{video.thumbnail_url}",
                    "created_at": f"{await time_difference(video.created_at)} days",
                }
                for video in long_videos.items
            ],
        },
        "short_videos": [
            {
                "id": video.id,
                "title": video.title,
                "thumbnail_url": f"http://127.0.0.1:8000/static/{video.thumbnail_url}",
            }
            for video in short_videos
        ],
    }

    return JSONResponse({"data": response_data}, status_code=status.HTTP_200_OK)


class UserSerializer(BaseModel):
    username: str


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
                    "thumbnail_url": f"http://127.0.0.1:8000/static/{video.thumbnail_url}",
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
    video = Video.query.filter_by(id=video_id).first()
