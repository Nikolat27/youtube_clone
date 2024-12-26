from fastapi import HTTPException, Query
from database.models.user import UserLogInfo
from fastapi import status
from routers.users import is_user_authenticated


async def get_current_user_id(user_session_id: str = Query(None)):
    is_authenticated = await is_user_authenticated(str(user_session_id))
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated"
        )

    user_log_info = UserLogInfo.query.filter_by(session_id=str(user_session_id)).first()
    if not user_log_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User session not found"
        )

    return user_log_info.user_id
