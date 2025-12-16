from typing import Optional

from pydantic import BaseModel, Field


class MerchantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class MerchantCreate(MerchantBase):
    pass


class MerchantUpdate(MerchantBase):
    pass


class MerchantOut(MerchantBase):
    id: int

