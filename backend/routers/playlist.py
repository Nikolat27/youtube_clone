from database.models.user import Playlist, User, Video
from sqlalchemy import desc, asc
from fastapi import APIRouter, Query, status, Path as Path_parameter
from dependencies import get_current_user_id
from fastapi.responses import JSONResponse

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
