from src.models import Member
from src.utils.repository import SqlAlchemyRepository


class MemberRepository(SqlAlchemyRepository):
    model = Member
