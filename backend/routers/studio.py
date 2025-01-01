from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Query,
    Form,
    status,
    Path as Path_paramter,
)
from fastapi.responses import JSONResponse
from database.models.user import Video, Playlist, Subtitle, Community, Channel
from database.models.base import session
from sqlalchemy import desc, asc
from pydantic import BaseModel
from pathlib import Path
from typing import Optional
from pymediainfo import MediaInfo
import shutil
import json
from dependencies import get_current_user_id
from datetime import datetime

UPLOAD_DIR = Path("uploaded_videos")
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter(prefix="/studio", tags=["studio"])


async def time_formatter(time):
    if not time:
        return None

    time_str = str(time)
    try:
        parsed_datetime = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        parsed_datetime = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return parsed_datetime.date().isoformat()


async def get_video_duration(file):  # Using pymediainfo (This is faster)
    media_info = MediaInfo.parse(file)
    return media_info.tracks[0].duration // 1000  # coverting ms to s


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    user_session_id: str = Form(),
    video_type: str = Form(),
):
    user_id = await get_current_user_id(user_session_id)

    UPLOAD_DIR_USER = Path(UPLOAD_DIR / str(user_id) / video_type)
    UPLOAD_DIR_USER.mkdir(exist_ok=True)

    # Validating the File type (it must be video)
    if not file.content_type.startswith("video/"):
        return JSONResponse({"error": "Your file type is not video!"})

    file_path = UPLOAD_DIR_USER / file.filename

    created_video = Video(
        user_id=user_id,
        title=file.filename,
        video_type=video_type,
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
    UPLOAD_DIR_USER = Path(UPLOAD_DIR / str(user_id) / type)
    UPLOAD_DIR_USER.mkdir(parents=True, exist_ok=True)
    thumbnail_path = UPLOAD_DIR_USER / file.filename
    with thumbnail_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return thumbnail_path


def delete_file(file_url):
    file_path = Path(file_url)
    try:
        if file_path.exists():
            file_path.unlink()  # Delete the file
            print(f"File {file_path} deleted successfully.")
        else:
            print(f"File {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while trying to delete the file: {e}")


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


# Video part
@router.get("/get")
async def get_video(video_id: int = Query()):
    video = Video.query.filter_by(id=video_id).first()

    playlists = [playlist.id for playlist in video.playlists if video.playlists]
    subtitle = video.subtitle.file_name if video.subtitle else None
    serializer = {
        "video_type": video.video_type,
        "details": {
            "video_id": video_id,
            "title": video.title,
            "description": video.description,
            "thumbnail_url": f"http://127.0.0.1:8000/static/{video.thumbnail_url}",
            "audience": "kids" if video.audience else "not-kids",
            "ageRestriction": "yes" if video.age_restriction else "no",
            "language": video.language,
            "playlists": playlists,
            "monetized": video.monetization,
        },
        "thumbnailFile": video.thumbnail_url,
        "subtitleFile": subtitle,
        "visibility": {
            "scheduled": True if video.schedule_time else False,
            "scheduledTime": await time_formatter(video.schedule_time) or None,
            "publish": "public" if video.visibility else "private",
        },
    }

    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.post("/update")
async def create_video(
    user_session_id: str = Form(...),
    video_type: str = Form(...),
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
        await update_video(
            int(details_dict["video_id"]),
            video_type,
            details_dict,
            visibility_dict,
            thumbnail_path,
        )

    if subtitleFile:
        await update_subtitle(
            int(details_dict["video_id"]), subtitleFile, subtitle_path
        )

    if "playlists" in details_dict:
        await update_playlists(int(details_dict["video_id"]), details_dict["playlists"])

    session.commit()
    return JSONResponse(
        {"message": "Your video updated successfully!"}, status_code=status.HTTP_200_OK
    )


async def update_video(
    video_id: int,
    video_type: str,
    details: dict,
    visibility: dict,
    thumbnail_path: Path,
):
    Video.query.filter_by(id=video_id).update(
        {
            "title": details["title"],
            "video_type": video_type,
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


@router.get("/list")
async def list_video(
    user_session_id: str = Query(),
    video_type: str = Query(None),
    filter: str = Query(None, alias="queries[filter]"),
    sort_type: str = Query(None, alias="queries[sortByType]"),
    sort_order: str = Query(None, alias="queries[sortByOrder]"),
):
    user_id = await get_current_user_id(user_session_id)

    videos = Video.query.with_entities(
        Video.id,
        Video.video_type,
        Video.title,
        Video.description,
        Video.thumbnail_url,
        Video.visibility,
        Video.file_url,
        Video.age_restriction,
        Video.created_at,
    ).filter_by(user_id=user_id, video_type=video_type)

    if filter and filter == "age-restriction":
        videos = videos.filter(Video.age_restriction == True)
    elif filter and filter == "made-for-kids":
        videos = videos.filter(Video.audience == True)
    elif filter and filter == "visibility":
        videos = videos.filter(Video.visibility == True)

    if sort_type and sort_order and sort_type == "date" and sort_order == "DESC":
        videos = videos.order_by(desc(Video.id)).all()
    elif sort_type and sort_order and sort_type == "date" and sort_order == "ASC":
        videos = videos.order_by(asc(Video.id)).all()

    serializer = []
    for video in videos:
        serializer.append(
            {
                "id": video.id,
                "title": video.title,
                "video_type": video_type,
                "description": video.description,
                "duration": await get_video_duration(video.file_url),
                "thumbnail_url": f"http://127.0.0.1:8000/static/{video.thumbnail_url}",
                "visibility": video.visibility,
                "restriction": video.age_restriction,
                "created_at": await time_formatter(video.created_at),
            }
        )
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


# Playlist part
class PlaylistSerializer(BaseModel):
    user_session_id: str
    title: str
    description: str | None
    visibility: str


@router.get("/playlist")
async def retrieve_playlist(user_session_id: str = Query(), playlist_id: int = Query()):
    user_id = await get_current_user_id(user_session_id)

    playlist = Playlist.query.filter_by(id=playlist_id).first()

    serializer = {"title": playlist.title, "description": playlist.description}


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


@router.get("/playlist/get/{playlist_id}")
async def get_playlist(
    user_session_id: str = Query(), playlist_id: int = Path_paramter()
):
    user_id = await get_current_user_id(user_session_id)

    playlist = Playlist.query.filter_by(id=playlist_id).first()

    serializer = {
        "id": playlist.id,
        "title": playlist.title,
        "description": playlist.description,
        "visibility": playlist.visibility,
    }
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.put("/playlist/edit/{playlist_id}")
async def edit_playlist(
    user_session_id: str = Form(),
    playlist_id: int = Path_paramter(),
    title: str = Form(),
    description: Optional[str] = Form(),
    visibility: str = Form(),
):
    user_id = await get_current_user_id(user_session_id)
    playlist = Playlist.query.filter_by(id=playlist_id).first()

    playlist.title = title
    playlist.description = description
    playlist.visibility = visibility
    session.commit()

    return JSONResponse(
        {"data": "Your playlist updated successfully!"}, status_code=status.HTTP_200_OK
    )


@router.delete("/playlist/delete/{playlist_id}")
async def delete_playlist(
    playlist_id: int = Path_paramter(), user_session_id: str = Query()
):
    user_id = await get_current_user_id(user_session_id)

    playlist = Playlist.query.filter_by(id=playlist_id).first()
    session.delete(playlist)
    session.commit()

    return JSONResponse(
        {"data": "Your playlist deleted successfully!"},
        status_code=status.HTTP_202_ACCEPTED,
    )


async def update_playlists(
    video_id: int, playlist_ids: list
):  # This function is used in Video Editing
    video = Video.query.filter_by(id=video_id).first()
    if video:
        video.playlists.clear()
        for id in playlist_ids:
            playlist = Playlist.query.filter_by(id=int(id)).first()
            if playlist:
                video.playlists.append(playlist)


@router.post("/community/create")
async def create_community_post(
    user_session_id: str = Form(),
    community_text: str = Form(),
    image_file: UploadFile = File(None),
):
    user_id = await get_current_user_id(user_session_id)
    if image_file:
        image_path = upload_file(user_id, image_file, "community_images")
        new_community = Community(
            user_id=user_id,
            community_text=community_text,
            image_name=image_file.filename,
            image_url=str(image_path),
        )
    else:
        new_community = Community(
            user_id=user_id,
            community_text=community_text,
        )

    session.add(new_community)
    session.commit()
    return JSONResponse(
        {"data": "Your community added successfully!"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/community/list")
async def list_community_posts(
    user_session_id: str = Query(),
    filter: str = Query(None, alias="queries[filter]"),
    type: str = Query(None, alias="queries[sortByType]"),
    order: str = Query(None, alias="queries[sortByOrder]"),
):

    user_id = await get_current_user_id(user_session_id)
    communities = Community.query.filter_by(user_id=user_id)

    if type and order and type == "date" and order == "ASC":
        communities = communities.order_by(asc(Community.id)).all()
    elif type and order and type == "date" and order == "DESC":
        communities = communities.order_by(desc(Community.id)).all()

    serializer = [
        {"id": community.id, "community_text": community.community_text}
        for community in communities
    ]

    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.post("/community/edit")
async def edit_community_post(
    user_session_id: str = Form(),
    community_id: int = Form(),
    community_text: str = Form(),
):
    user_id = await get_current_user_id(user_session_id)

    community = Community.query.filter_by(id=community_id).first()
    community.community_text = community_text

    session.commit()
    return JSONResponse(
        {"data": "community updated successfully!"}, status_code=status.HTTP_200_OK
    )


@router.get("/channel/customization")
async def get_channel_info(user_session_id: str = Query()):
    user_id = await get_current_user_id(user_session_id)

    channel = Channel.query.filter_by(owner_id=user_id).first()

    serializer = {
        "detail": {
            "owner_id": user_id,
            "name": channel.name or "",
            "unique_identifier": channel.unique_identifier or "",
            "description": channel.description or "",
            "contact_email": channel.contact_email or "",
        },
        "banner_img": f"http://127.0.0.1:8000/static/{channel.banner_img_url}" or "",
        "profile_picture": f"http://127.0.0.1:8000/static/{channel.profile_picture_url}"
        or "",
        "video_watermark": f"http://127.0.0.1:8000/static/{channel.video_watermark_url}"
        or "",
    }

    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.put("/channel/customization/update")
async def update_channel_info(
    user_session_id: str = Form(),
    detail: str = Form(),
    banner_img: UploadFile = File(None),
    profile_img: UploadFile = File(None),
    watermark_img: UploadFile = File(None),
):
    user_id = await get_current_user_id(user_session_id)
    detail = json.loads(detail)

    channel = Channel.query.filter_by(owner_id=user_id).first()

    channel.name = detail["name"]
    channel.description = detail["description"]
    channel.unique_identifier = detail["unique_identifier"]
    channel.contact_email = detail["contact_email"]

    if banner_img:
        banner_img_url = upload_file(user_id, banner_img, "banner_img")
        channel.banner_img_url = str(banner_img_url)

    if profile_img:
        profile_img_url = upload_file(user_id, profile_img, "profile_img")
        channel.profile_img_url = profile_img_url

    if watermark_img:
        watermark_img_url = upload_file(user_id, watermark_img, "watermark_img")
        channel.watermark_img_url = watermark_img_url

    session.commit()
    return JSONResponse(
        {"data": "Channel updated successfully!"}, status_code=status.HTTP_200_OK
    )


@router.delete("/channel/customization/remove")
async def remove_channel_image(
    user_session_id: str = Query(...),
    image_type: str = Query(...),
):
    user_id = await get_current_user_id(user_session_id)

    channel = Channel.query.filter_by(owner_id=user_id).first()
    if not channel:
        return JSONResponse(
            {"error": "Channel not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    if image_type == "banner_img":
        if channel.banner_img_url:
            delete_file(channel.banner_img_url)
            channel.banner_img_url = ""
    elif image_type == "profile_img":
        if channel.profile_img_url:
            delete_file(channel.profile_img_url)
            channel.profile_img_url = ""
    elif image_type == "watermark_img":
        if channel.watermark_img_url:
            delete_file(channel.watermark_img_url)
            channel.watermark_img_url = ""

    session.commit()
    return JSONResponse(
        {"data": f"{image_type} removed successfully!"}, status_code=status.HTTP_200_OK
    )
