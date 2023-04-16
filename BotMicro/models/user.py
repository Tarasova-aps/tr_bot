from typing import Optional
from odetam.async_model import AsyncDetaModel


class User(AsyncDetaModel):
    name: str
    chat_id: Optional[int] = None

    @property
    def user_key(self) -> str:
        return str(self.key)
    