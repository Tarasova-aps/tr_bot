from typing import Optional

from odetam.async_model import AsyncDetaModel


class User(AsyncDetaModel):
    name: str

    chat_id: Optional[int] = None

    deleted: bool = False

    @classmethod
    async def get_available(cls) -> list['User']:
        return await User.query(User.deleted == False)  # type: ignore

    @property
    def user_key(self) -> str:
        return str(self.key)
