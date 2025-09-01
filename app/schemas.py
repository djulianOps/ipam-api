from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
import ipaddress

class SubnetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    cidr: str

    @field_validator("cidr")
    @classmethod
    def validate_cidr(cls, v: str):
        try:
            ipaddress.ip_network(v, strict=True)
        except Exception as e:
            raise ValueError(f"CIDR inválido: {e}")
        return v

class SubnetCreate(SubnetBase):
    pass

class SubnetUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    cidr: Optional[str] = None

    @field_validator("cidr")
    @classmethod
    def validate_cidr(cls, v: Optional[str]):
        if v is None:
            return v
        ipaddress.ip_network(v, strict=True)
        return v

class SubnetOut(SubnetBase):
    id: int
    vnet_id: int
    address: str
    netmask: str
    wildcard: str
    network: str
    broadcast: str
    class_type: str

    model_config = ConfigDict(from_attributes=True)

class VNetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    cidr: str

    @field_validator("cidr")
    @classmethod
    def validate_cidr(cls, v: str):
        ipaddress.ip_network(v, strict=True)
        return v

class VNetCreate(VNetBase):
    subnets: Optional[List[SubnetCreate]] = Field(default_factory=list)  # <—

class VNetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=128)
    cidr: Optional[str] = None
    subnets: Optional[List[SubnetUpdate]] = None

    @field_validator("cidr")
    @classmethod
    def validate_cidr(cls, v: Optional[str]):
        if v is None:
            return v
        ipaddress.ip_network(v, strict=True)
        return v

class VNetOut(VNetBase):
    id: int
    address: str
    netmask: str
    wildcard: str
    network: str
    broadcast: str
    class_type: str
    subnets: List[SubnetOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)