from src.models import UserPosition
from src.utils.repository import SqlAlchemyRepository


class UserPositionRepository(SqlAlchemyRepository):
    model = UserPosition
