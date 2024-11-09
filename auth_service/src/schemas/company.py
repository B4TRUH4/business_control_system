from pydantic import BaseModel


class CompanyID(BaseModel):
    id: int


class CompanyBase(BaseModel):
    company_name: str


class CompanyDB(CompanyBase, CompanyID):
    pass


class CompanyResponse(CompanyDB):
    pass


class CreateCompanyRequest(CompanyBase):
    pass


class CreateCompanyResponse(CompanyResponse):
    pass
