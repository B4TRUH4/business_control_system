from sqlalchemy_utils import Ltree

from src.api.exceptions import (
    StructAdmDoesNotExistsException,
    PositionDoesNotExistsException,
    StructAdmAlreadyExistsException,
)
from src.models import StructAdm
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class StructAdmService(BaseService):
    base_repository = 'struct_adm'

    @transaction_mode
    async def create_struct_adm(
        self,
        name: str,
        company_id: int,
        parent_id: int = None,
        manager_position_ids: list[int] = None,
        employee_position_ids: list[int] = None,
    ) -> StructAdm:
        struct_adm_id = await self._create_struct_adm(
            name=name, company_id=company_id
        )
        return await self._create_linked_and_update_struct_adm(
            struct_adm_id,
            name,
            parent_id,
            manager_position_ids,
            employee_position_ids,
        )

    @transaction_mode
    async def update_struct_adm(
        self,
        name: str,
        struct_adm_id: int,
        company_id: int,
        parent_id: int = None,
        manager_position_ids: list[int] = None,
        employee_position_ids: list[int] = None,
    ) -> StructAdm:
        struct_adm = await self._get_struct_adm(
            id=struct_adm_id, company_id=company_id
        )
        await self.uow.struct_adm_position.delete_by_query(
            struct_adm_id=struct_adm.id
        )
        return await self._create_linked_and_update_struct_adm(
            struct_adm_id=struct_adm.id,
            name=name,
            parent_id=parent_id,
            company_id=company_id,
            manager_position_ids=manager_position_ids,
            employee_position_ids=employee_position_ids,
        )

    @transaction_mode
    async def list_struct_adm(self, company_id: int):
        return await self.uow.struct_adm.get_by_query_all_with_positions(
            company_id=company_id
        )

    @transaction_mode
    async def get_struct_adm(self, struct_adm_id: int, company_id: int):
        return await self._get_struct_adm_with_positions(
            id=struct_adm_id, company_id=company_id
        )

    @transaction_mode
    async def delete_struct_adm(self, struct_adm_id: int, company_id: int):
        await self._get_struct_adm(id=struct_adm_id, company_id=company_id)
        await self.uow.struct_adm.delete_by_query(id=struct_adm_id)

    async def _get_struct_adm_with_positions(self, **kwargs):
        struct_adm = (
            await self.uow.struct_adm.get_by_query_one_or_none_with_positions(
                **kwargs
            )
        )
        if not struct_adm:
            raise StructAdmDoesNotExistsException
        return struct_adm

    async def _get_struct_adm(self, **kwargs):
        struct_adm = await self.uow.struct_adm.get_by_query_one_or_none(
            **kwargs
        )
        if not struct_adm:
            raise StructAdmDoesNotExistsException
        return struct_adm

    async def _create_struct_adm(self, name: str, company_id: int, **kwargs):
        struct_adm = await self.uow.struct_adm.get_by_query_one_or_none(
            name=name,
            company_id=company_id,
        )
        if struct_adm:
            raise StructAdmAlreadyExistsException
        return await self.uow.struct_adm.add_one_and_get_id(
            name=name, company_id=company_id
        )

    async def _check_position_exists(self, position_id: int, company_id: int):
        manager_position = await self.uow.position.get_by_query_one_or_none(
            id=position_id, company_id=company_id
        )
        if not manager_position:
            raise PositionDoesNotExistsException
        return manager_position

    async def _create_linked_and_update_struct_adm(
        self,
        struct_adm_id: int,
        name: str,
        company_id: int,
        parent_id: int = None,
        manager_position_ids: list[int] = None,
        employee_position_ids: list[int] = None,
    ):
        if parent_id:
            parent = await self._get_struct_adm(
                id=parent_id, company_id=company_id
            )

        if employee_position_ids:
            for position_id in employee_position_ids:
                await self._check_position_exists(
                    position_id=position_id, company_id=company_id
                )
                await self.uow.struct_adm_position.add_one(
                    struct_adm_id=struct_adm_id,
                    position_id=position_id,
                )

        if manager_position_ids:
            for position_id in manager_position_ids:
                await self._check_position_exists(
                    position_id=position_id, company_id=company_id
                )
                await self.uow.struct_adm_position.add_one(
                    struct_adm_id=struct_adm_id,
                    position_id=position_id,
                    is_manager=True,
                )

        struct_adm = await self.uow.struct_adm.update_one_by_id_with_positions(
            obj_id=struct_adm_id,
            name=name,
            path=Ltree(f'{parent.path}.{struct_adm_id}')
            if parent_id
            else Ltree(str(struct_adm_id)),
        )
        return struct_adm
