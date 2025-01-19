from fastapi import (
    APIRouter,
    Path as Path_parameter,
    status,
    Query,
    Header,
    Form,
    HTTPException,
)
from database.models.base import session
from database.models.user import (
    Video,
    User,
    Like,
    SaveVideos,
    History,
    Channel,
    Comment,
    Notification,
    CommentLike,
    ChannelSubscription,
)
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select, desc, asc
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime
from pymediainfo import MediaInfo
from pathlib import Path
from dependencies import get_current_user_id
import re
import json
import requests
from googleapiclient.discovery import build
import yt_dlp
import redis
import socket


# Replace with your API key
API_KEY = "AIzaSyD4tVMAI9kvBA7DghHz3QDrA3UJEe6u7as"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

router = APIRouter(prefix="/videos", tags=["videos"])

redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0)


async def get_video_duration(file):  # Using pymediainfo (This is faster)
    media_info = MediaInfo.parse(file)
    return media_info.tracks[0].duration // 1000  # coverting Ms to S


async def time_difference(created_time):
    current_time = datetime.now()
    time_difference = current_time.date() - created_time.date()
    return time_difference.days


async def static_file(file_url):
    return f"http://127.0.0.1:8000/static/{file_url}"


async def check_video_exist(video_id):
    video = Video.query.filter_by(unique_id=video_id).first()
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This Video Doesnt Exist!"
        )


async def check_comment_exist(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment didnt find"
        )


async def get_username(user_id):
    user = User.query.with_entities(User.username).filter_by(id=user_id).first()
    return user.username


def get_channel_name(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.channel.name or user.username


def get_channel_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    return f"http://127.0.0.1:8000/static/{user.channel.profile_picture_url}"


def get_channel_unique_identifier(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.channel.unique_identifier


def get_channel_total_subs(channel_id):
    return ChannelSubscription.query.filter_by(channel_id=channel_id).count()


def is_channel_subed(channel_id, user_id):
    return bool(
        ChannelSubscription.query.filter_by(
            channel_id=channel_id, user_id=user_id
        ).first()
    )


async def get_users_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


@router.get("/generate/fake")  # Usage: Generate testing and random data to our DB
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
            Video.unique_id,
            Video.title,
            Video.thumbnail_url,
            Video.created_at,
            Video.user_id,
            Video.file_url,
            Video.views,
        )
        .where(Video.video_type == "long_video")
        .order_by(Video.created_at),
    )

    short_videos = (
        Video.query.with_entities(
            Video.id, Video.unique_id, Video.views, Video.title, Video.thumbnail_url
        )
        .filter_by(video_type="short_video")
        .limit(12)
        .all()
    )

    user_ip = await get_users_ip()
    response_data = {
        "long_videos": {
            "total": long_videos.total,
            "page": long_videos.page,
            "size": long_videos.size,
            "pages": long_videos.pages,
            "items": [
                {
                    "id": video.id,
                    "unique_id": video.unique_id,
                    "title": video.title,
                    "views": video.views,
                    "watch_progress": await get_current_video_time(
                        user_ip, video.unique_id, video.file_url
                    ),
                    # "watch_progress": None,
                    "thumbnail_url": await static_file(video.thumbnail_url),
                    "created_at": f"{await time_difference(video.created_at)} days",
                    "channel_profile_picture": get_channel_profile(video.user_id),
                    "channel_name": get_channel_name(video.user_id),
                    "channel_unique_identifier": get_channel_unique_identifier(
                        video.user_id
                    ),
                }
                for video in long_videos.items
            ],
        },
        "short_videos": [
            {
                "id": video.id,
                "unique_id": video.unique_id,
                "title": video.title,
                "views": video.views,
                "thumbnail_url": await static_file(video.thumbnail_url),
            }
            for video in short_videos
        ],
    }

    return JSONResponse({"data": response_data}, status_code=status.HTTP_200_OK)


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
                    "id": video.unique_id,
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


@router.get("/detail/{unique_id}")
async def video_detail(
    unique_id: str = Path_parameter(), user_session_id: str = Query(None)
):
    user_id = None
    if user_session_id:
        user_id = await get_current_user_id(user_session_id)

    video = (
        Video.query.with_entities(
            Video.id,
            Video.unique_id,
            Video.views,
            Video.user_id,
            Video.title,
            Video.description,
            Video.file_url,
            Video.thumbnail_url,
            Video.created_at,
        )
        .filter_by(unique_id=unique_id)
        .first()
    )

    if not video:
        DIR = Path("youtube_videos")
        FILE_PATH = Path(DIR / unique_id / f"{unique_id}.mp4")
        if FILE_PATH.exists():
            return JSONResponse(
                {"data": str(FILE_PATH)}, status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                {"data": f"https://www.youtube.com/embed/{unique_id}"},
                status_code=status.HTTP_202_ACCEPTED,
            )

    channel = (
        Channel.query.with_entities(
            Channel.id,
            Channel.name,
            Channel.profile_picture_url,
            Channel.video_watermark_url,
        )
        .filter_by(owner_id=video.user_id)
        .first()
    )

    user_ip = await get_users_ip()

    current_time = redis_client.get(
        f"{video.unique_id}-{user_ip}-current_time"
    )  # this one is in bytes
    if current_time:
        decode_current_time = float(current_time.decode("utf-8"))
    else:
        decode_current_time = 0

    serializer = {
        "id": video.unique_id,
        "title": video.title,
        "views": video.views,
        "user_id": video.user_id,
        "description": video.description or "",
        "file_url": await static_file(video.file_url),
        "thumbnail_url": await static_file(video.thumbnail_url),
        "current_time": decode_current_time,
        "duration": await get_video_duration(video.file_url),
        "created_at": f"{await time_difference(video.created_at)} days ",
        "channel_id": channel.id,
        "channel_name": channel.name or "",
        "channel_profile_url": await static_file(channel.profile_picture_url) or "",
        "channel_watermark_url": await static_file(channel.video_watermark_url) or "",
        "channel_total_subs": get_channel_total_subs(channel.id),
        "is_channel_subed": is_channel_subed(channel.id, user_id),
        "total_likes": await total_video_likes(video.unique_id),
    }
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/stream/{unique_id}/")
async def video_stream(unique_id: str = Path_parameter(), range: str = Header(None)):
    video = (
        Video.query.with_entities(Video.file_url).filter_by(unique_id=unique_id).first()
    )
    if video:
        video_path = Path(f"{video.file_url}").resolve()
    else:
        DIR = Path("youtube_videos")
        video_path = Path(DIR / unique_id / f"{unique_id}.mp4").resolve()

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

        redis_client.set("filesize", filesize)
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")


@router.get("/stream/watch-time/{unique_id}")
async def video_watch_time(
    unique_id: str = Path_parameter(),
    watch_time: float = Query(),
    duration: float = Query(),
):
    if duration <= 30:
        if watch_time >= duration:
            video = Video.query.filter_by(unique_id=unique_id).first()
            video.views += 1
            session.commit()
    else:
        if watch_time >= 30:
            video = Video.query.filter_by(unique_id=unique_id).first()
            video.views += 1
            session.commit()


# @router.get("/stream/watch-time/{unique_id}")
# async def video_watch_time(
#     unique_id: str = Path_parameter(),
#     watch_time: float = Query(),
#     duration: float = Query(),
# ):
#     user_ip = await get_users_ip()
#     redis_client.set(f"{unique_id}-{user_ip}-watch_time", watch_time, ex=3600) # 1 Hour expiration time
#     await check_video_watch_time(unique_id, user_ip, duration)


# async def check_video_watch_time(unique_id, user_ip, duration):
#     watch_time = redis_client.get(f"{unique_id}-{user_ip}-watch_time")
#     video_duration = duration

#     if video_duration <= 30:
#         if watch_time >= video_duration:
#             video = Video.query.filter_by(unique_id=unique_id).first()
#             video.views += 1
#             session.commit()
#     else:
#         if watch_time >= 30:
#             video = Video.query.filter_by(unique_id=unique_id).first()
#             video.views += 1
#             session.commit()


@router.get("/stream/current-time/{unique_id}")
async def set_current_video_time(
    unique_id: str = Path_parameter,
    current_time: float = Query(),
):
    user_ip = await get_users_ip()
    current_time = round(current_time, 1)
    redis_client.set(f"{unique_id}-{user_ip}-current_time", current_time)


async def get_current_video_time(user_ip, unique_id, file_url):
    try:
        current_time = redis_client.get(f"{unique_id}-{user_ip}-current_time")
        decode_current_time = float(current_time.decode("utf-8"))
        video_duration = await get_video_duration(file_url)
        progress_percentage = (decode_current_time * 100) / video_duration
        return progress_percentage
    except:
        return None


@router.get("/like/{unique_id}/{action_type}/{user_session_id}")
async def like_video(
    unique_id: str = Path_parameter(),
    action_type: bool = Path_parameter(),
    user_session_id: str = Path_parameter(),
):  # True == Like, False == Dislike
    user_id = await get_current_user_id(user_session_id)

    like = Like.query.filter_by(video_id=unique_id, user_id=user_id).first()
    if like and like.action_type == action_type:
        session.delete(like)
    elif like and like.action_type != action_type:
        like.action_type = action_type
    else:
        new_like = Like(user_id=user_id, video_id=unique_id, action_type=action_type)
        session.add(new_like)

    session.commit()
    return JSONResponse(
        {"data": action_type, "total_likes": await total_video_likes(unique_id)},
        status_code=status.HTTP_200_OK,
    )


async def total_video_likes(video_unique_id):
    return Like.query.filter_by(video_id=video_unique_id, action_type=True).count()


@router.get("/like-situation/{unique_id}/{user_session_id}")
async def is_user_liked(
    unique_id: str = Path_parameter(), user_session_id: str = Path_parameter()
):
    user_id = await get_current_user_id(user_session_id)
    like_situation = None
    like = (
        Like.query.with_entities(Like.action_type)
        .filter_by(video_id=unique_id, user_id=user_id)
        .first()
    )
    if like:
        like_situation = like.action_type

    return JSONResponse(
        {"data": like_situation, "total_likes": await total_video_likes(unique_id)},
        status_code=status.HTTP_200_OK,
    )


@router.get("/save/{unique_id}/{user_session_id}")
async def save_video(
    unique_id: str = Path_parameter(), user_session_id: str = Path_parameter()
):
    user_id = await get_current_user_id(user_session_id)
    await check_video_exist(unique_id)

    save_instance = SaveVideos.query.filter_by(
        video_id=unique_id, user_id=user_id
    ).first()
    if save_instance:  # If exists, just delete it (Unsave)
        session.delete(save_instance)
    else:  # If doesnt Exist, Create a new one (Save)
        save_instance = SaveVideos(video_id=unique_id, user_id=user_id)
        session.add(save_instance)

    session.commit()
    return JSONResponse(
        {"data": "Your video saved successfully!"}, status_code=status.HTTP_200_OK
    )


@router.get("/is-save/{unique_id}/{user_session_id}")
async def is_video_saved(
    unique_id: str = Path_parameter(), user_session_id: str = Path_parameter()
):
    user_id = await get_current_user_id(user_session_id)
    await check_video_exist(unique_id)

    is_video_saved = False
    save_instance = SaveVideos.query.filter_by(
        video_id=unique_id, user_id=user_id
    ).first()
    if save_instance:
        is_video_saved = True

    return JSONResponse({"data": is_video_saved}, status_code=status.HTTP_200_OK)


@router.get("/comment/list/{unique_id}")
async def get_comments_list(
    unique_id: str = Path_parameter(), user_session_id: str = Query(None)
) -> Page:
    user_id = None
    if user_session_id:
        user_id = await get_current_user_id(user_session_id)

    await check_video_exist(unique_id)
    comments = paginate(
        session,
        select(Comment)
        .where(Comment.video_id == unique_id, Comment.parent_id == None)
        .order_by(desc(Comment.created_at)),
    )

    serializer = [
        {
            "id": comment.id,
            "user_id": comment.user_id,
            "username": await get_username(comment.user_id),
            "text": comment.text,
            "parent_id": comment.parent_id,
            "created_at": await time_difference(comment.created_at),
            "user_profile_picrure": get_channel_profile(comment.user_id),
            "is_liked": await is_comment_liked(comment.id, user_id),
            "replies_count": len(comment.replies),
            "replies": [],
        }
        for comment in comments.items
    ]
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


async def create_notification(
    sender_id, receiver_id, video_id, channel_name, type, text, comment_id=None
):
    notification = Notification(
        sender_id=sender_id,
        receiver_id=receiver_id,
        video_id=video_id,
        channel_name=channel_name,
        type=type,
        text=text,
        comment_id=comment_id,
    )
    session.add(notification)
    session.commit()


@router.post("/comment/add")
async def add_comment(
    video_id: str = Form(),
    user_session_id: str = Form(),
    comment_text: str = Form(),
    parent_id: int = Form(None),
):
    user_id = await get_current_user_id(user_session_id)
    await check_video_exist(video_id)

    comment = Comment(
        video_id=video_id,
        user_id=user_id,
        text=comment_text,
        parent_id=parent_id or None,
    )
    session.add(comment)
    session.commit()

    if parent_id:  # If you have parent_id it means that your replying to a comment.
        receiver_id = (
            Comment.query.with_entities(Comment.user_id).filter_by(id=parent_id).first()
        )
    else:  # If you dont, it means that your commenting on a video, So your receiver is the video owner
        receiver_id = (
            Video.query.with_entities(Video.user_id)
            .filter_by(unique_id=video_id)
            .first()
        )

    await create_notification(
        user_id,
        receiver_id.user_id,
        video_id,
        await get_username(user_id),
        "comment",
        comment_text,
        comment_id=comment.id,
    )
    return JSONResponse(
        {"data": "Comment added successfully!"}, status_code=status.HTTP_201_CREATED
    )


@router.get("/replies/list/{comment_id}")
async def get_replies_list(
    comment_id: int = Path_parameter(), user_session_id: str = Query(None)
):
    user_id = None
    if user_session_id:
        user_id = await get_current_user_id(user_session_id)

    comment = Comment.query.filter_by(id=comment_id).first()
    serializer = [
        {
            "id": reply.id,
            "parent_username": await get_username(reply.user_id),
            "user_id": reply.user_id,
            "username": await get_username(reply.user_id),
            "user_profile_picrure": get_channel_profile(comment.user_id),
            "is_liked": await is_comment_liked(reply.id, user_id),
            "text": reply.text,
            "parent_id": reply.parent_id,
            "created_at": await time_difference(reply.created_at),
        }
        for reply in comment.replies
    ]

    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/comment/like/{comment_id}")
async def like_comment(
    comment_id: int = Path_parameter(),
    user_session_id: str = Query(),
    action_type: bool = Query(),
):
    user_id = await get_current_user_id(user_session_id)
    await check_comment_exist(comment_id)

    like_instance = CommentLike.query.filter_by(
        user_id=user_id, comment_id=comment_id
    ).first()

    if like_instance and like_instance.action_type == action_type:
        session.delete(like_instance)
    elif like_instance and like_instance.action_type != action_type:
        like_instance.action_type = not like_instance.action_type
    else:
        new_like = CommentLike(
            user_id=user_id,
            comment_id=comment_id,
            action_type=action_type,
        )
        session.add(new_like)

    session.commit()
    return JSONResponse({"data": "Successful!"}, status_code=status.HTTP_200_OK)


async def is_comment_liked(comment_id, user_id=None):
    if not user_id:
        is_liked = None
    else:
        like_instance = (
            CommentLike.query.with_entities(CommentLike.action_type)
            .filter_by(user_id=user_id, comment_id=comment_id)
            .first()
        )
        is_liked = like_instance.action_type if like_instance else None
    return is_liked


@router.get("/search/autocomplete")
def get_youtube_autocomplete_suggestions(query: str = Query()):
    url = "https://suggestqueries.google.com/complete/search"
    params = {
        "client": "youtube",
        "q": query,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        json_data = re.search(r"^[^(]*\((.*)\)\s*$", response.text).group(1)
        parsed_data = json.loads(json_data)
        suggestions = parsed_data[1]
        return [suggest[0] for suggest in suggestions]


@router.get("/search")
def search_youtube(query: str = Query(), size: int = Query(None)):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    # Search the Query
    search_response = (
        youtube.search()
        .list(q=query, part="id,snippet", maxResults=size or 1, type="video")
        .execute()
    )
    videos = [
        {
            "title": search_result["snippet"]["title"],
            "description": search_result["snippet"]["description"],
            "thumbnail": search_result["snippet"]["thumbnails"]["high"]["url"],
            "channel": search_result["snippet"]["channelTitle"],
            "published_date": search_result["snippet"]["publishedAt"],
            "video_id": search_result["id"]["videoId"],
        }
        for search_result in search_response.get("items", [])
    ]
    return JSONResponse({"data": videos}, status_code=status.HTTP_200_OK)


UPLOAD_DIR = Path("youtube_videos")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/download/{video_id}")
def download_video(video_id: str = Path_parameter()):
    # The URL of the YouTube video
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    UPLOAD_DIR_VIDEO = Path(UPLOAD_DIR / video_id)
    check_video_exist = UPLOAD_DIR_VIDEO.exists()
    if not check_video_exist:
        UPLOAD_DIR_VIDEO.mkdir(exist_ok=True, parents=True)

        # Options for the downloader
        ydl_opts = {
            "format": "bestvideo[ext=mp4][height<=480]+bestaudio[ext=m4a]/best[ext=mp4]",
            "merge_output_format": "mp4",
            "outtmpl": f"{str(UPLOAD_DIR_VIDEO)}/{video_id}.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    return JSONResponse(
        {"data": "This video have been downloaded"}, status_code=status.HTTP_200_OK
    )


@router.get("/add-watch-history/{video_id}")
async def add_video_watch_history(
    video_id: str = Path_parameter(), user_session_id: str = Query()
):
    user_id = await get_current_user_id(user_session_id)

    # Checking the history
    history = History.query.filter_by(user_id=user_id, video_id=video_id).first()
    if history:
        history.created_at = datetime.utcnow()
    else:
        new_history = History(user_id=user_id, video_id=video_id)
        session.add(new_history)
    session.commit()


@router.get("/user-watch-history/")
async def get_user_video_watch_history(user_session_id: str = Query()):
    user_id = await get_current_user_id(user_session_id)

    histories = History.query.filter_by(user_id=user_id).all()

    return JSONResponse({"data": "hizdxfasdf"}, status_code=status.HTTP_200_OK)
