from bot.core.constants import UserRole
from bot.schemas.core import Model, IdMixin


class UserInit(Model):
    chat_id: int
    login: str
    name: str
    surname: str


class UserAbout(Model):
    role: UserRole
    about: str
    target: str


class UserShort(UserInit, IdMixin):
    about: UserAbout
