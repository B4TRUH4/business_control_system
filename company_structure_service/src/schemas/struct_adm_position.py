from pydantic import BaseModel

from src.schemas.position import PositionDB


class StructAdmPositionBase(BaseModel):
    pass
    # struct_adm_id: int
    # position_id: int
    is_manager: bool


class StructAdmPositionDB(StructAdmPositionBase):
    position: PositionDB
