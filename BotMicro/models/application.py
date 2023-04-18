from datetime import datetime
from typing import Any

from odetam.async_model import AsyncDetaModel
from pydantic import Field


class Application(AsyncDetaModel):
    created_at: datetime = Field(default_factory=datetime.now)

    creator_user_id: int

    data: dict[str, Any]

    files: list[tuple[str, str]] = Field(default_factory=list)  # drive, file_name

    @property
    def app_key(self) -> str:
        return str(self.key)
