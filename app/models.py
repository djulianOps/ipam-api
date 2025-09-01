from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import CIDR
from .database import Base

class VNet(Base):
    __tablename__ = "vnets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False, index=True)
    cidr = Column(CIDR, nullable=False)

    address = Column(String(64))
    netmask = Column(String(64))
    wildcard = Column(String(64))
    network = Column(String(64))
    broadcast = Column(String(64))
    class_type = Column(String(2))

    subnets = relationship("Subnet", back_populates="vnet", cascade="all, delete-orphan")


class Subnet(Base):
    __tablename__ = "subnets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    cidr = Column(CIDR, nullable=False)
    vnet_id = Column(Integer, ForeignKey("vnets.id", ondelete="CASCADE"), nullable=False)

    address = Column(String(64))
    netmask = Column(String(64))
    wildcard = Column(String(64))
    network = Column(String(64))
    broadcast = Column(String(64))
    class_type = Column(String(2))

    vnet = relationship("VNet", back_populates="subnets")

    __table_args__ = (
        UniqueConstraint("vnet_id", "name", name="uq_subnet_name_per_vnet"),
        UniqueConstraint("vnet_id", "cidr", name="uq_subnet_cidr_per_vnet"),
    )