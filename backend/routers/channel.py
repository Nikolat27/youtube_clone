from fastapi import Path as Path_parameter, status, Query
from fastapi.responses import JSONResponse
from database.models.base import session
from database.models.user import (
    Video,
    Channel,
    ChannelSubscription,
    Playlist,
    Community,
    CommunityLike,
)
from dependencies import get_current_user_id
from fastapi import APIRouter
from datetime import datetime
from pymediainfo import MediaInfo
from sqlalchemy import desc, asc, select
from fastapi_pagination.ext.sqlalchemy import paginate
import math

router = APIRouter(prefix="/channel", tags=["channel"])


async def time_difference(created_at):
    difference = datetime.now().date() - created_at.date()
    return f"{str(difference.days)} days"


async def static_file(file_url):
    return f"http://127.0.0.1:8000/static/{file_url}"


async def check_subscription(user_session_id, channel_id):
    if not user_session_id:
        return False
    user_id = await get_current_user_id(user_session_id)
    sub = (
        ChannelSubscription.query.with_entities(ChannelSubscription.id)
        .filter_by(user_id=user_id, channel_id=channel_id)
        .first()
    )
    return True if sub else False


async def check_channel_notification(user_session_id, channel_id):
    if not user_session_id:
        return False
    user_id = await get_current_user_id(user_session_id)
    notification = (
        ChannelSubscription.query.with_entities(ChannelSubscription.notification)
        .filter_by(user_id=user_id, channel_id=channel_id)
        .first()
    )
    return True if notification else False


async def get_video_duration(file):
    media_info = MediaInfo.parse(file)
    return media_info.tracks[0].duration // 1000


@router.get("/{unique_identifier}")
async def channel_page(
    unique_identifier: str = Path_parameter(), user_session_id: str = Query(None)
):
    channel = Channel.query.filter_by(unique_identifier=unique_identifier).first()
    total_subcriptions = ChannelSubscription.query.filter_by(
        channel_id=channel.id
    ).count()

    serializer = {
        "details": {
            "id": channel.id,
            "banner_url": await static_file(channel.banner_img_url) or "",
            "profile_url": await static_file(channel.profile_picture_url),
            "name": channel.name,
            "description": channel.description,
            "contact_email": channel.contact_email,
            "total_subs": total_subcriptions,
        },
        "is_sub": await check_subscription(user_session_id or None, channel.id),
        "channel_notification": await check_channel_notification(
            user_session_id or None, channel.id
        ),
    }
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/subscribe/{channel_id}")
async def channel_subscribe(
    channel_id: int = Path_parameter(), user_session_id: str = Query()
):
    user_id = await get_current_user_id(user_session_id)
    sub_situation = ChannelSubscription.query.filter_by(
        channel_id=channel_id, user_id=user_id
    ).first()

    if not sub_situation:
        new_sub = ChannelSubscription(channel_id=channel_id, user_id=user_id)
        session.add(new_sub)
        message = "You've successfully subscribed from this channel"
    else:
        message = "You've successfully unsubscribed from this channel"
        session.delete(sub_situation)

    session.commit()
    return JSONResponse({"data": message}, status_code=status.HTTP_200_OK)


@router.get("/notification/{channel_id}")
async def channel_notification(
    channel_id: int = Path_parameter(),
    user_session_id: str = Query(),
    notification: str = Query(),
):
    user_id = await get_current_user_id(user_session_id)
    channel = ChannelSubscription.query.filter_by(
        user_id=user_id, channel_id=channel_id
    ).first()

    if notification == "all":
        channel.notification = True
    elif notification == "none":
        channel.notification = False

    session.commit()
    return JSONResponse(
        {"data": "Notifications Changed successfully!"}, status_code=status.HTTP_200_OK
    )


@router.get("/{channel_id}/home-videos/")
async def home_channel_videos(channel_id: str = Path_parameter()):
    channel = (
        Channel.query.with_entities(Channel.owner_id)
        .filter_by(unique_identifier=channel_id)
        .first()
    )
    videos = (
        Video.query.with_entities(
            Video.unique_id, Video.created_at, Video.thumbnail_url, Video.title
        )
        .filter_by(user_id=channel.owner_id)
        .limit(12)
        .all()
    )

    serializer = [
        {
            "unique_id": video.unique_id,
            "title": video.title,
            "thumbnail_url": await static_file(video.thumbnail_url),
            "created_at": await time_difference(video.created_at),
        }
        for video in videos
    ]
    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/{channel_id}/videos/")
async def channel_long_videos(
    channel_id: str = Path_parameter(),
    page: int = Query(),
    size: int = Query(),
    sortBy: str = Query(None),
):

    channel = (
        Channel.query.with_entities(Channel.owner_id)
        .filter_by(unique_identifier=channel_id)
        .first()
    )

    videos = Video.query.with_entities(
        Video.unique_id,
        Video.file_url,
        Video.created_at,
        Video.thumbnail_url,
        Video.title,
    ).filter_by(user_id=channel.owner_id, video_type="long_video")

    total_videos = Video.query.filter_by(
        user_id=channel.owner_id, video_type="long_video"
    ).count()

    if not sortBy or sortBy == "latest":
        videos = videos.order_by(desc(Video.created_at))
    elif sortBy and sortBy == "popular":
        pass
    elif sortBy and sortBy == "oldest":
        videos = videos.order_by(asc(Video.created_at))

    videos.offset(page * size - size).limit(size).all()

    serializer = [
        {
            "unique_id": video.unique_id,
            "title": video.title,
            "thumbnail_url": await static_file(video.thumbnail_url),
            "duration": await get_video_duration(video.file_url),
            "created_at": await time_difference(video.created_at),
        }
        for video in videos
    ]
    return JSONResponse(
        {"data": serializer, "total_pages": math.ceil(total_videos / size)},
        status_code=status.HTTP_200_OK,
    )


@router.get("/{channel_id}/shorts/")
async def channel_short_videos(
    channel_id: str = Path_parameter(),
    page: int = Query(),
    size: int = Query(),
    sortBy: str = Query(None),
):

    channel = (
        Channel.query.with_entities(Channel.owner_id)
        .filter_by(unique_identifier=channel_id)
        .first()
    )

    shorts = Video.query.with_entities(
        Video.unique_id,
        Video.file_url,
        Video.created_at,
        Video.thumbnail_url,
        Video.title,
    ).filter_by(user_id=channel.owner_id, video_type="short_video")

    total_videos = Video.query.filter_by(
        user_id=channel.owner_id, video_type="short_video"
    ).count()

    if not sortBy or sortBy == "latest":
        shorts = shorts.order_by(desc(Video.created_at))
    elif sortBy and sortBy == "popular":
        pass
    elif sortBy and sortBy == "oldest":
        shorts = shorts.order_by(asc(Video.created_at))

    shorts.offset(page * size - size).limit(size).all()

    serializer = [
        {
            "unique_id": short.unique_id,
            "title": short.title,
            "thumbnail_url": await static_file(short.thumbnail_url),
        }
        for short in shorts
    ]
    return JSONResponse(
        {"data": serializer, "total_pages": math.ceil(total_videos / size)},
        status_code=status.HTTP_200_OK,
    )


@router.get("/{channel_id}/playlists/")
async def channel_playlists(
    channel_id: str = Path_parameter(),
    page: int = Query(),
    size: int = Query(),
    sortBy: str = Query(None),
):

    channel = (
        Channel.query.with_entities(Channel.owner_id)
        .filter_by(unique_identifier=channel_id)
        .first()
    )

    playlists = Playlist.query.filter_by(owner_id=channel.owner_id)
    total_playlists = Playlist.query.filter_by(owner_id=channel.owner_id).count()

    if not sortBy or sortBy == "latest":
        playlists = playlists.order_by(desc(Playlist.created_at))
    elif sortBy and sortBy == "popular":
        pass
    elif sortBy and sortBy == "oldest":
        playlists = playlists.order_by(asc(Playlist.created_at))

    playlists.offset(page * size - size).limit(size).all()
    serializer = [
        {
            "id": playlist.id,
            "title": playlist.title,
            "thumbnail_url": "",
        }
        for playlist in playlists
    ]
    return JSONResponse(
        {"data": serializer, "total_pages": math.ceil(total_playlists / size)},
        status_code=status.HTTP_200_OK,
    )


@router.get("/{channel_id}/communities")
async def channel_communities(
    channel_id: str = Path_parameter(), user_session_id: str = Query(None)
):
    channel = (
        Channel.query.with_entities(Channel.owner_id)
        .filter_by(unique_identifier=channel_id)
        .first()
    )

    communities = Community.query.filter_by(user_id=channel.owner_id).all()

    serializer = [
        {
            "id": community.id,
            "text": community.community_text,
            "image_url": await static_file(community.image_url),
            "created_at": await time_difference(community.created_at),
            "is_liked": True,
        }
        for community in communities
    ]

    return JSONResponse({"data": serializer}, status_code=status.HTTP_200_OK)


@router.get("/like/{community_id}/{action_type}/{user_session_id}")
async def like_video(
    community_id: int = Path_parameter(),
    action_type: bool = Path_parameter(),
    user_session_id: str = Path_parameter(),
):  # True == Like, False == Dislike
    user_id = await get_current_user_id(user_session_id)

    like = CommunityLike.query.filter_by(
        community_id=community_id, user_id=user_id
    ).first()
    if like and like.action_type == action_type:
        session.delete(like)
    elif like and like.action_type != action_type:
        like.action_type = action_type
    else:
        new_like = CommunityLike(
            user_id=user_id, community_id=community_id, action_type=action_type
        )
        session.add(new_like)

    session.commit()
    return JSONResponse(
        {"data": action_type},
        status_code=status.HTTP_200_OK,
    )


async def has_user_liked(id: int, user_session_id: str) -> JSONResponse:
    user_id = await get_current_user_id(user_session_id)
    like = (
        CommunityLike.query.with_entities(CommunityLike.action_type)
        .filter_by(community_id=id, user_id=user_id)
        .first()
    )

    like_situation = None
    if like:
        like_situation = like.action_type

    return JSONResponse({"data": like_situation}, status_code=status.HTTP_200_OK)
