from fastapi import Path as Path_parameter, status
from fastapi.responses import JSONResponse
from database.models.base import session
from database.models.user import (
    Video,
    User,
    Like,
    SaveVideos,
    Channel,
    Comment,
    Notification,
    CommentLike,
)
from dependencies import get_current_user_id
from fastapi import APIRouter


router = APIRouter(prefix="/channel", tags=["channel"])


async def static_file(file_url):
    return f"http://127.0.0.1:8000/static/"


@router.get("/{unique_identifier}")
async def channel_page(unique_identifier: str = Path_parameter()):
    channel = Channel.query.filter_by(unique_identifier=unique_identifier).first()

    return JSONResponse({"data": "channel"}, status_code=status.HTTP_200_OK)
