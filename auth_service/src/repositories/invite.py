from src.models import Invite
from src.utils.repository import SqlAlchemyRepository


class InviteRepository(SqlAlchemyRepository):
    model = Invite
