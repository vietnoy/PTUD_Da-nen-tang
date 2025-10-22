from ..core.security import hash_password, verify_password
from ..models import User
from fastapi import HTTPException, status

def validate_password(old_password: str, new_password: str, user: User):
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "00072", "message": "Old password incorrect"}
        )
    
    if old_password == new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "00073", "message": "New password must be different"}
        )
    
    return hash_password(new_password)