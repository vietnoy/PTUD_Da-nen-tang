from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


# Result message structure used in responses
class ResultMessage(BaseModel):
    en: str
    vn: str


# Base response structure
class BaseResponse(BaseModel):
    result_message: ResultMessage = Field(..., alias="resultMessage")
    result_code: str = Field(..., alias="resultCode")


# Log data structure
class LogData(BaseModel):
    id: int
    user_id: int = Field(..., alias="userId")
    result_code: str = Field(..., alias="resultCode")
    level: str
    error_message: str = Field(..., alias="errorMessage")
    ip: str
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt")


# Get logs endpoint schemas
class GetLogsRequest(BaseModel):
    pass  # No body parameters needed, it's a GET request


class GetLogsResponse(BaseResponse):
    logs: List[LogData] = []
