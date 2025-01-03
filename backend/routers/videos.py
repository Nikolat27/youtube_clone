from fastapi import APIRouter, Path as Path_parameter, status, Query, Header
from database.models.base import session
from database.models.user import Video, User, Like, SaveVideos, Channel
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime
from pymediainfo import MediaInfo
from pathlib import Path
from dependencies import get_current_user_id

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
async def video_detail(
    video_id: int = Path_parameter(), user_session_id: str = Query(None)
):
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

    channel = (
        Channel.query.with_entities(
            Channel.name, Channel.profile_picture_url, Channel.video_watermark_url
        )
        .filter_by(owner_id=video.user_id)
        .first()
    )
    print("Channel: ", channel.profile_picture_url)

    serializer = {
        "id": video.id,
        "title": video.title,
        "user_id": video.user_id,
        "description": video.description or "",
        "file_url": await static_file(video.file_url),
        "thumbnail_url": await static_file(video.thumbnail_url),
        "duration": await get_video_duration(video.file_url),
        "created_at": f"{await time_difference(video.created_at)} days ",
        "channel_name": channel.name,
        "channel_profile_url": await static_file(channel.profile_picture_url) or "",
        "channel_watermark_url": await static_file(channel.video_watermark_url) or "",
    }
    print("File: ", serializer["channel_profile_url"])
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/stream/{video_id}/")
async def video_stream(video_id: int = Path_parameter(), range: str = Header(None)):
    video = Video.query.with_entities(Video.file_url).filter_by(id=video_id).first()
    video_path = Path(f"{video.file_url}").resolve()

    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    CHUNK_SIZE = 1024 * 1024
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


@router.get("/like/{video_id}/{action_type}/{user_session_id}")
async def like_video(
    video_id: str = Path_parameter(),
    action_type: bool = Path_parameter(),
    user_session_id: str = Path_parameter(),
):  # True == Like, False == Dislike
    user_id = await get_current_user_id(user_session_id)

    like = Like.query.filter_by(video_id=video_id, user_id=user_id).first()
    if like and like.action_type == action_type:
        session.delete(like)
    elif like and like.action_type != action_type:
        like.action_type = action_type
    else:
        new_like = Like(user_id=user_id, video_id=video_id, action_type=action_type)
        session.add(new_like)

    session.commit()
    return JSONResponse(
        {"data": action_type},
        status_code=status.HTTP_200_OK,
    )


@router.get("/like-situation/{video_id}/{user_session_id}")
async def is_user_liked(
    video_id: int = Path_parameter(), user_session_id: str = Path_parameter()
):
    user_id = await get_current_user_id(user_session_id)
    like_situation = None
    like = (
        Like.query.with_entities(Like.action_type)
        .filter_by(video_id=video_id, user_id=user_id)
        .first()
    )
    if like:
        like_situation = like.action_type

    return JSONResponse({"data": like_situation}, status_code=status.HTTP_200_OK)


@router.get("/save/{video_id}/{user_session_id}")
async def save_video(
    video_id: int = Path_parameter(), user_session_id: str = Path_parameter()
):
    user_id = await get_current_user_id(user_session_id)

    video_exist = Video.query.with_entities(Video.id).filter_by(id=video_id).first()
    if not video_exist:
        return JSONResponse(
            {"error": "This video doesnt exist!"}, status_code=status.HTTP_404_NOT_FOUND
        )

    save_instance = SaveVideos.query.filter_by(
        video_id=video_id, user_id=user_id
    ).first()
    if save_instance:  # If exists, just delete it (Unsave)
        session.delete(save_instance)
    else:  # If doesnt Exist, Create a new one (Save)
        save_instance = SaveVideos(video_id=video_id, user_id=user_id)
        session.add(save_instance)

    session.commit()
    return JSONResponse(
        {"data": "Your video saved successfully!"}, status_code=status.HTTP_200_OK
    )


@router.get("/is-save/{video_id}/{user_session_id}")
async def is_video_saved(
    video_id: int = Path_parameter(), user_session_id: str = Path_parameter()
):
    user_id = await get_current_user_id(user_session_id)

    video_exist = Video.query.with_entities(Video.id).filter_by(id=video_id).first()
    if not video_exist:
        return JSONResponse(
            {"error": "This video doesnt exist!"}, status_code=status.HTTP_404_NOT_FOUND
        )

    is_video_saved = False
    save_instance = SaveVideos.query.filter_by(
        video_id=video_id, user_id=user_id
    ).first()
    if save_instance:
        is_video_saved = True

    return JSONResponse({"data": is_video_saved}, status_code=status.HTTP_200_OK)
