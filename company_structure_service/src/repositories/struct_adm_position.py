from src.models import StructAdmPosition
from src.utils.repository import SqlAlchemyRepository


class StructAdmPositionRepository(SqlAlchemyRepository):
    model = StructAdmPosition
