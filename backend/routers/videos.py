from fastapi import APIRouter, UploadFile, File, Query, Form, status
from fastapi.responses import JSONResponse
from database.models.user import Video, Playlist, Subtitle
from database.models.base import session
from sqlalchemy import desc
from pydantic import BaseModel
from pathlib import Path
from pymediainfo import MediaInfo
import shutil
import json
import time
from dependencies import get_current_user_id
import subprocess

UPLOAD_DIR = Path("uploaded_videos")
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter(prefix="/videos", tags=["videos"])

# async def get_video_duration(file): # Using openCv
#     import cv2
#     data = cv2.VideoCapture(file)
#     frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
#     fps = data.get(cv2.CAP_PROP_FPS)
#     return frames / fps

async def get_video_duration(file):  # Using pymediainfo (This is faster)
    print(file)
    media_info = MediaInfo.parse(file)
    return media_info.tracks[0].duration


@router.post("/upload")
async def upload_video(file: UploadFile = File(...), user_session_id: str = Form()):
    user_id = await get_current_user_id(user_session_id)

    UPLOAD_DIR_USER = Path(UPLOAD_DIR / str(user_id))
    UPLOAD_DIR_USER.mkdir(exist_ok=True)

    # Validating the File type (it must be video)
    if not file.content_type.startswith("video/"):
        return JSONResponse({"error": "Your file type is not video!"})

    file_path = UPLOAD_DIR_USER / file.filename

    created_video = Video(
        user_id=user_id,
        title=file.filename,
        file_name=file.filename,
        file_url=str(file_path),
    )
    session.add(created_video)
    session.commit()

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    duration = await get_video_duration(file_path)
    return JSONResponse(
        {"video_id": created_video.id},
        status_code=status.HTTP_201_CREATED,
    )


def upload_file(user_id, file, type):
    UPLOAD_DIR_USER = Path(UPLOAD_DIR / str(user_id) / f"{type}")
    UPLOAD_DIR_USER.mkdir(exist_ok=True)
    thumbnail_path = UPLOAD_DIR_USER / file.filename
    with thumbnail_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return thumbnail_path


async def update_video_details(
    video_id: int, details: dict, visibility: dict, thumbnail_path: Path
):
    Video.query.filter_by(id=video_id).update(
        {
            "title": details["title"],
            "description": details["description"],
            "thumbnail_name": thumbnail_path.name if thumbnail_path else "",
            "thumbnail_url": str(thumbnail_path) if thumbnail_path else "",
            "audience": True if (details["audience"] == "kids") else False,
            "age_restriction": (
                True if (details["ageRestriction"] == "yes") else False
            ),
            "language": details["language"],
            "monetization": details["monetized"],
            "visibility": True if (visibility["publish"] == "public") else False,
            "schedule_time": visibility["scheduledTime"] or None,
        }
    )


async def update_subtitle(
    video_id: int, subtitle_file: UploadFile, subtitle_path: Path
):
    subtitle = Subtitle.query.filter_by(video_id=video_id).first()
    if subtitle:
        subtitle.video_id = video_id
        subtitle.title = subtitle_file.filename
        subtitle.file_name = subtitle_file.filename
        subtitle.file_url = str(subtitle_path)
    else:
        new_subtitle = Subtitle(
            video_id=video_id,
            title=subtitle_file.filename,
            file_name=subtitle_file.filename,
            file_url=str(subtitle_path),
        )
        session.add(new_subtitle)


async def update_playlists(video_id: int, playlist_ids: list):
    video = Video.query.filter_by(id=video_id).first()
    if video:
        video.playlists.clear()
        for id in playlist_ids:
            playlist = Playlist.query.filter_by(id=int(id)).first()
            if playlist:
                video.playlists.append(playlist)


@router.post("/update")
async def update_video(
    user_session_id: str = Form(...),
    details: str = Form(...),
    thumbnailFile: UploadFile = File(None),
    subtitleFile: UploadFile = File(None),
    visibility: str = Form(...),
):
    user_id = await get_current_user_id(user_session_id)
    details_dict = json.loads(details)
    visibility_dict = json.loads(visibility)

    thumbnail_path = (
        upload_file(user_id, thumbnailFile, "thumbnail") if thumbnailFile else None
    )
    subtitle_path = (
        upload_file(user_id, subtitleFile, "subtitle") if subtitleFile else None
    )

    if details_dict:
        await update_video_details(
            int(details_dict["video_id"]), details_dict, visibility_dict, thumbnail_path
        )

    if subtitleFile:
        await update_subtitle(
            int(details_dict["video_id"]), subtitleFile, subtitle_path
        )

    if "playlists" in details_dict:
        await update_playlists(int(details_dict["video_id"]), details_dict["playlists"])

    session.commit()

    time.sleep(1)
    return JSONResponse(
        {"message": "Your video updated successfully!"}, status_code=status.HTTP_200_OK
    )


class PlaylistSerializer(BaseModel):
    user_session_id: str
    title: str
    description: str | None
    visibility: str


@router.get("/playlist/list")
async def all_playlists(user_session_id: str = Query()):
    user_id = await get_current_user_id(user_session_id)
    playlists = (
        Playlist.query.with_entities(
            Playlist.id, Playlist.owner_id, Playlist.title, Playlist.visibility
        )
        .filter_by(owner_id=user_id)
        .order_by(desc(Playlist.id))
        .all()
    )

    serializer = [
        {
            "id": playlist.id,
            "owner_id": playlist.owner_id,
            "title": playlist.title,
            "visibility": playlist.visibility,
        }
        for playlist in playlists
    ]
    return JSONResponse({"playlists": serializer}, status_code=status.HTTP_200_OK)


@router.post("/playlist/create")
async def create_playlist(
    user_session_id: str = Form(...),
    title: str = Form(...),
    description: str | None = Form(None),
    visibility: str = Form(...),
):
    user_id = await get_current_user_id(user_session_id)

    new_playlist = Playlist(
        owner_id=user_id, title=title, description=description, visibility=visibility
    )
    session.add(new_playlist)
    session.commit()
    return JSONResponse(
        {"data": "playlist created successfully!"}, status_code=status.HTTP_201_CREATED
    )


@router.get("/list")
async def user_videos(user_session_id: str = Query()):
    user_id = await get_current_user_id(user_session_id)

    videos = Video.query.filter_by(user_id=user_id).all()
    print(videos)

    return JSONResponse({"data": "Hello World!"}, status_code=status.HTTP_200_OK)
