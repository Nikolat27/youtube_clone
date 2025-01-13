from database.models.user import Playlist, User, Video, Channel
from sqlalchemy import desc, asc
from fastapi import APIRouter, Query, status, Path as Path_parameter
from dependencies import get_current_user_id
from fastapi.responses import JSONResponse
from datetime import datetime

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
            "total_videos": len(playlist.video),
            "last_video_unique_id": await playlist_last_video_unique_id(
                playlist.video[-1]
            ),  # Sending the last index video
            "last_video_thumbnail": await playlist_last_video_thumbnail_url(
                playlist.video[-1]
            ),  # Sending the last index video again
        }
        for playlist in playlists
    ]

    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.delete("/delete/{playlist_id}")
async def delete_playlist(playlist_id: int = Path_parameter()):
    Playlist.query.filter_by(id=playlist_id).delete()
    return JSONResponse(
        {"data": "Playlist deleted successfully!"}, status_code=status.HTTP_202_ACCEPTED
    )


async def playlist_last_video_unique_id(video):
    return video.unique_id


async def playlist_last_video_thumbnail_url(video):
    return video.thumbnail_url


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
async def get_playlist(playlist_id: int = Path_parameter()):
    playlist = Playlist.query.filter_by(id=playlist_id).first()

    serializer = {
        "id": playlist.id,
        "title": playlist.title,
        "username": await get_username(playlist.owner_id),
        "videos": [
            {
                "id": video.id,
                "unique_id": video.unique_id,
                "title": video.title,
                "created_at": await time_difference(video.created_at),
                "thumbnail_url": f"http://127.0.0.1:8000/static/{video.thumbnail_url}",
                "channel_name": await video_channel(video.user_id),
            }
            for video in playlist.video
        ],
        "last_video_thumbnail": await playlist_last_video_thumbnail_url(
            playlist.video[-1]
        ),
        "total_videos": len(playlist.video),
    }

    print("Serializer: ", serializer)
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)
