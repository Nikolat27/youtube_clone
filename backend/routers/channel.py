from fastapi import Path as Path_parameter, status, Query
from fastapi.responses import JSONResponse
from database.models.base import session
from database.models.user import (
    Video,
    User,
    Like,
    SaveVideos,
    Channel,
    ChannelSubscription,
    Comment,
    Notification,
    CommentLike,
)
from dependencies import get_current_user_id
from fastapi import APIRouter


router = APIRouter(prefix="/channel", tags=["channel"])


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


@router.get("/{unique_identifier}")
async def channel_page(
    unique_identifier: str = Path_parameter(), user_session_id: str = Query(None)
):
    channel = Channel.query.filter_by(unique_identifier=unique_identifier).first()
    total_subcriptions = ChannelSubscription.query.filter_by(
        channel_id=channel.id
    ).count()

    serializer = {
        "id": channel.id,
        "banner_url": await static_file(channel.banner_img_url) or "",
        "profile_url": await static_file(channel.profile_picture_url),
        "name": channel.name,
        "description": channel.description,
        "contact_email": channel.contact_email,
        "total_subs": total_subcriptions,
        "is_sub": await check_subscription(user_session_id or None, channel.id),
        "channel_notification": await check_channel_notification(user_session_id or None, channel.id)
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
