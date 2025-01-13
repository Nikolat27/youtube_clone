from database.models.user import Playlist
from database.models.user import User
from fastapi import APIRouter, Query, status
from dependencies import get_current_user_id
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/playlist", tags=["playlists"])


@router.get("/")
async def get_user_playlists(user_session_id: str = Query()):
    user_id = await get_current_user_id(user_session_id)
    playlists = Playlist.query.filter_by(owner_id=user_id).all()

    serializer = [
        {
            "title": playlist.title,
            "visibility": playlist.visibility,
            "total_videos": playlist.videos.count(),
        }
        for playlist in playlists
    ]

    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)
