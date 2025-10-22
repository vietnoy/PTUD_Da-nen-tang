"""User management API routes."""

from fastapi import APIRouter, Depends

from ..core.deps import get_current_user
from ..models import User
from ..schemas import GetUserResponse
from ..schemas.User.user import ResultMessage
from ..utils.responseCodeEnums import ResponseCode

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=GetUserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return GetUserResponse(
        user=current_user,
        resultMessage=ResultMessage(
            en="User profile retrieved successfully",
            vn=ResponseCode.USER_INFO_RETRIEVED.value[1],
        ),
        resultCode=ResponseCode.USER_INFO_RETRIEVED.value[0],
    )
