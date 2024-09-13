from typing import Union
from pydantic import BaseModel


class BankAccountBase(BaseModel):
    bank_name: str
    bank_account_no: Union[str, None]
    bank_phone_number: Union[str, None]
    bank_address: Union[str, None]
    bank_city: Union[str, None]
    bank_province: Union[str, None]
    bank_card_no: Union[str, None]
    user_id: int

class BankAccountUpdate(BankAccountBase):
    id: str


class UserBookMark(BaseModel):
    id: int
    user_id: int
    product_id: int
    is_favorite: bool


class ProductTag(BaseModel):
    tag_name: str


class ProductTagUpdate(ProductTag):
    id: int


class CompanyBase(BaseModel):
    company_name: str
    company_address: str
    company_phone: str
    user_id: int


class CompanyUpdate(CompanyBase):
    id : int


class ProductBase(BaseModel):
    product_name: str
    product_price: Union[str, float, int]
    product_tag_id: int
    company_id: int


class ProductUpdate(ProductBase):
    id: int


class UserBase(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    user_phone: str
    user_identity_code: str
    user_email: str
    user_address: str


class UserUpdate(UserCreate):
    id: int
    confirm_password: str


class Invoice(BaseModel):
    product_id: int
    user_id: int
    company_id: int
    status: str = "approved"

class InvoiceUpdate(Invoice):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None