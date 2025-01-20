from database.models.user import (
    Playlist,
    User,
    Video,
    Channel,
    playlist_video_association,
)
from sqlalchemy import desc, asc
from fastapi import APIRouter, Query, status, Path as Path_parameter
from typing import List, Optional
from dependencies import get_current_user_id
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from datetime import datetime
import secrets
from database.models.base import session

router = APIRouter(prefix="/playlist", tags=["playlists"])


@router.get("/")
async def get_user_playlists(user_session_id: str = Query(), sortBy: str = Query(None)):
    user_id = await get_current_user_id(user_session_id)
    playlists = Playlist.query.filter_by(owner_id=user_id)

    if sortBy and sortBy == "a-z":
        playlists = playlists.order_by(asc(Playlist.created_at))
    elif not sortBy or sortBy == "latest":
        playlists = playlists.order_by(desc(Playlist.created_at))

    serializer = [
        {
            "id": playlist.id,
            "title": playlist.title,
            "visibility": playlist.visibility,
            "is_default": playlist.is_default,
            "total_videos": playlist.video.count(),
            "last_video_unique_id": (
                await playlist_last_video_unique_id(list(playlist.video)[-1])
                if list(playlist.video)
                else None
            ),
            "last_video_thumbnail": (
                await playlist_last_video_thumbnail_url(list(playlist.video)[-1])
                if list(playlist.video)
                else None
            ),
        }
        for playlist in playlists
    ]
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/user-all-playlists/{video_id}")
async def get_all_user_playlists(
    video_id: str = Path_parameter(), user_session_id: str = Query()
):
    user_id = await get_current_user_id(user_session_id)
    # Corrected query
    playlists = Playlist.query.with_entities(
        Playlist.id,
        Playlist.title,
        Playlist.visibility,
    ).filter(Playlist.owner_id == user_id)

    serializer = [
        {
            "id": playlist.id,
            "title": playlist.title,
            "visibility": playlist.visibility,
            "video_exists": await check_video_exists_in_playlist(playlist.id, video_id),
        }
        for playlist in playlists
    ]
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/save-video-to-playlist/{video_id}", status_code=status.HTTP_200_OK)
async def save_video_to_playlist(
    video_id: str = Path_parameter(),
    playlists: Optional[List[str]] = Query(None, alias="playlists[]"),
):
    if not playlists:
        session.execute(
            playlist_video_association.delete().where(
                playlist_video_association.c.video_id == video_id
            )
        )
        session.commit()
        return

    playlist_ids = [int(playlist) for playlist in playlists]

    existing_associations = session.execute(
        playlist_video_association.select().where(
            playlist_video_association.c.video_id == video_id
        )
    ).fetchall()

    existing_playlist_ids = [
        association.playlist_id for association in existing_associations
    ]

    for playlist_id in playlist_ids:
        if playlist_id not in existing_playlist_ids:
            session.execute(
                playlist_video_association.insert().values(
                    playlist_id=playlist_id, video_id=video_id
                )
            )

    for existing_playlist_id in existing_playlist_ids:
        if existing_playlist_id not in playlist_ids:
            session.execute(
                playlist_video_association.delete()
                .where(playlist_video_association.c.playlist_id == existing_playlist_id)
                .where(playlist_video_association.c.video_id == video_id)
            )

    session.commit()


async def check_video_exists_in_playlist(playlist_id, video_id):
    video_exists = (
        Playlist.query.join(Playlist.video)
        .filter(Video.unique_id == video_id)
        .filter(Playlist.id == playlist_id)
        .first()
    )
    return bool(video_exists)


@router.delete("/delete/{playlist_id}")
async def delete_playlist(playlist_id: int = Path_parameter()):
    Playlist.query.filter_by(id=playlist_id).delete()
    return JSONResponse(
        {"data": "Playlist deleted successfully!"}, status_code=status.HTTP_202_ACCEPTED
    )


async def playlist_last_video_unique_id(video):
    return video.unique_id


async def playlist_last_video_thumbnail_url(video):
    return f"http://127.0.0.1:8000/static/{video.thumbnail_url}"


async def get_username(user_id):
    return (
        User.query.with_entities(User.username).filter_by(id=user_id).first()
    ).username


async def time_difference(created_at):
    difference = datetime.now().date() - created_at.date()
    return str(difference.days)


async def video_channel(user_id):
    return (
        Channel.query.with_entities(Channel.name).filter_by(owner_id=user_id).first()
    ).name


@router.get("/{playlist_id}")
async def get_playlist(
    playlist_id: int = Path_parameter(),
    filter: str = Query(),
    user_session_id: str = Query(None),
):
    playlist = Playlist.query.filter_by(id=playlist_id).first()

    if (
        playlist.is_default or playlist.visibility == "private"
    ):  # Only user can access the default and private playlists
        user_id = await get_current_user_id(user_session_id)
        if playlist.owner_id != user_id:
            raise HTTPException(detail="Only the user can see this playlist")

    videos = playlist.video
    match filter:
        case "all":
            videos = videos
        case "videos":
            videos = videos.filter(Video.video_type == "long_video")
        case "shorts":
            videos = videos.filter(Video.video_type == "short_video")

    serializer = {
        "id": playlist.id,
        "title": playlist.title,
        "username": await get_username(playlist.owner_id),
        "videos": [
            {
                "id": video.id,
                "views": video.views,
                "unique_id": video.unique_id,
                "title": video.title,
                "created_at": await time_difference(video.created_at),
                "thumbnail_url": f"http://127.0.0.1:8000/static/{video.thumbnail_url}",
                "channel_name": await video_channel(video.user_id),
            }
            for video in videos.order_by(desc(Video.created_at))
        ],
        "last_video_unique_id": (
            await playlist_last_video_unique_id(list(playlist.video)[-1])
            if list(playlist.video)
            else None
        ),
        "last_video_thumbnail": (
            await playlist_last_video_thumbnail_url(list(playlist.video)[-1])
            if list(playlist.video)
            else None
        ),
        "total_videos": playlist.video.count(),
    }

    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/shuffle/{playlist_id}")
async def shuffle_playlist(playlist_id: int = Path_parameter()):
    playlist_videos = Playlist.query.filter_by(id=playlist_id).first()
    total_videos = playlist_videos.video.count()
    random_video_index = secrets.randbelow(total_videos)  # 0, total - 1
    videos = list(playlist_videos.video)
    unique_id = videos[random_video_index].unique_id
    return JSONResponse({"data": unique_id}, status_code=status.HTTP_200_OK)


@router.get(
    "/video-info/{playlist_id}/{video_id}"
)  # receive current video Id and next video title
async def get_current_video_playlist_info(
    playlist_id: int = Path_parameter(), video_id: str = Path_parameter()
):
    playlist = Playlist.query.filter_by(id=playlist_id).first()
    videos = list(playlist.video)

    indexes = [video.unique_id for video in videos]
    current_video_index = indexes.index(video_id)

    next_video_title = None
    if current_video_index + 1 < len(videos):
        next_video_title = videos[current_video_index + 1].title

    return JSONResponse(
        {
            "current_video_index": current_video_index,
            "next_video_title": next_video_title,
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/watch/later")
async def watch_later_user_playlist(user_session_id: str = Query()):
    if not user_session_id:
        raise HTTPException(status_code=400, detail="user_session_id is required")

    user_id = await get_current_user_id(user_session_id)
    # In this function we just pass the id of the playlist then redirect the user
    playlist = (
        Playlist.query.with_entities(Playlist.id)
        .filter_by(owner_id=user_id, title="Watch later")
        .first()
    )
    return playlist.id


@router.get("/liked/videos")
async def liked_videos_user_playlist(user_session_id: str = Query()):
    if not user_session_id:
        raise HTTPException(status_code=400, detail="user_session_id is required")

    user_id = await get_current_user_id(user_session_id)
    # In this function we just pass the id of the playlist then redirect the user
    playlist = (
        Playlist.query.with_entities(Playlist.id)
        .filter_by(owner_id=user_id, title="Liked videos")
        .first()
    )
    return playlist.id
