from fastapi import APIRouter, Path, status
from database.models.base import session
from database.models.user import Video
from fastapi.responses import JSONResponse

from sqlalchemy import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("/")
async def videos_list() -> Page:
    videos = paginate(session, select(Video.id, Video.title).order_by(Video.created_at))
    response_data = {
        "total": videos.total,
        "page": videos.page,
        "size": videos.size,
        "pages": videos.pages,
        "items": [str(video) for video in videos.items] 
    }

    return JSONResponse({"data": response_data}, status_code=status.HTTP_200_OK)


@router.get("/detail/{video_id}")
async def video_detail(video_id: int = Path()):
    video = Video.query.filter_by(id=video_id).first()
