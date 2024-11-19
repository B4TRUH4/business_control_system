from pydantic import BaseModel

from src.schemas.response import BaseResponse, BaseCreateResponse
from src.schemas.struct_adm_position import StructAdmPositionDB
from src.utils.custom_types import LtreeField


class StructAdmID(BaseModel):
    id: int


class StructAdmBase(BaseModel):
    name: str
    path: LtreeField
    company_id: int


class StructAdmDB(StructAdmBase, StructAdmID):
    struct_positions: list[StructAdmPositionDB]


class CreateStructAdmRequest(BaseModel):
    name: str
    parent_id: int = None
    manager_position_ids: list[int] = None
    employee_position_ids: list[int] = None


class StructAdmResponse(BaseResponse):
    payload: StructAdmDB


class ListStructAdmResponse(BaseResponse):
    payload: list[StructAdmDB]


class CreateStructAdmResponse(BaseCreateResponse):
    payload: StructAdmDB
