from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas
import ipaddress

# ---------- Helpers ----------
def _network(obj_cidr: str):
    return ipaddress.ip_network(obj_cidr, strict=True)

def _ensure_subnet_within_vnet(vnet_cidr: str, subnet_cidr: str):
    vnet_net = _network(vnet_cidr)
    sub_net = _network(subnet_cidr)
    if not (sub_net.subnet_of(vnet_net)):
        raise ValueError("The subnet CIDR is not contained within the VNet CIDR.")

def _ensure_no_overlap(existing_cidrs: list[str], new_cidr: str):
    new_net = _network(new_cidr)
    for c in existing_cidrs:
        if _network(c).overlaps(new_net):
            raise ValueError(f"Subnet CIDR overlaps '{c}'.")
    return True

def _cidr_to_details(cidr: str) -> dict:
    net = ipaddress.ip_network(cidr, strict=True)
    address = str(net.network_address)
    netmask = str(net.netmask)
    wildcard = str(net.hostmask)
    network = str(net.network_address)
    broadcast = str(net.broadcast_address)
    # Determine class
    first_octet = int(str(net.network_address).split(".")[0])
    if 1 <= first_octet <= 126:
        cls = "A"
    elif 128 <= first_octet <= 191:
        cls = "B"
    elif 192 <= first_octet <= 223:
        cls = "C"
    elif 224 <= first_octet <= 239:
        cls = "D"
    else:
        cls = "E"
    return {
        "address": address,
        "netmask": netmask,
        "wildcard": wildcard,
        "network": network,
        "broadcast": broadcast,
        "class_type": cls,
    }

# ---------- VNET ----------
def create_vnet(db: Session, data: schemas.VNetCreate) -> models.VNet:
    details = _cidr_to_details(data.cidr)
    vnet = models.VNet(name=data.name, cidr=data.cidr, **details)
    db.add(vnet)
    db.commit()
    db.refresh(vnet)

    for s in data.subnets or []:
        create_subnet(db, s.dict(), vnet.id)

    return vnet

def get_vnets(db: Session, skip=0, limit=100):
    return db.execute(select(models.VNet).offset(skip).limit(limit)).scalars().all()

def get_vnet(db: Session, vnet_id: int):
    return db.get(models.VNet, vnet_id)

def update_vnet(db: Session, vnet_id: int, data: schemas.VNetUpdate):
    vnet = db.get(models.VNet, vnet_id)
    if not vnet:
        return None

    if data.cidr:
        new_vnet_net = _network(data.cidr)
        for s in vnet.subnets:
            if not _network(s.cidr).subnet_of(new_vnet_net):
                raise ValueError(f"Subnet '{s.name}' does not fit in new VNet CIDR.")
        vnet.cidr = data.cidr
        details = _cidr_to_details(data.cidr)
        for key, value in details.items():
            setattr(vnet, key, value)

    if data.name:
        vnet.name = data.name

    db.commit()
    db.refresh(vnet)

    for s in data.subnets or []:
        if hasattr(s, "id") and s.id:  # Update existing
            update_subnet(db, s.id, s.dict())
        else:  # Create new subnet
            create_subnet(db, s.dict(), vnet.id)

    return vnet

def delete_vnet(db: Session, vnet_id: int):
    vnet = db.get(models.VNet, vnet_id)
    if not vnet:
        return False
    db.delete(vnet)
    db.commit()
    return True

# ---------- SUBNET ----------
def create_subnet(db: Session, data: dict, vnet_id: int) -> models.Subnet:
    vnet = db.get(models.VNet, vnet_id)
    if not vnet:
        raise ValueError("VNet not found.")

    _ensure_subnet_within_vnet(vnet.cidr, data['cidr'])
    existing = [s.cidr for s in vnet.subnets]
    _ensure_no_overlap(existing, data['cidr'])

    details = _cidr_to_details(data['cidr'])
    s = models.Subnet(
        name=data['name'],
        cidr=data['cidr'],
        vnet_id=vnet.id,
        **details
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

def get_subnets(db: Session, skip=0, limit=100):
    return db.execute(select(models.Subnet).offset(skip).limit(limit)).scalars().all()

def get_subnet(db: Session, subnet_id: int):
    return db.get(models.Subnet, subnet_id)

def update_subnet(db: Session, subnet_id: int, data: dict):
    s = db.get(models.Subnet, subnet_id)
    if not s:
        return None

    if 'cidr' in data and data['cidr']:
        vnet = s.vnet
        _ensure_subnet_within_vnet(vnet.cidr, data['cidr'])
        existing = [x.cidr for x in vnet.subnets if x.id != s.id]
        _ensure_no_overlap(existing, data['cidr'])
        s.cidr = data['cidr']
        details = _cidr_to_details(data['cidr'])
        for key, value in details.items():
            setattr(s, key, value)

    if 'name' in data and data['name']:
        s.name = data['name']

    db.commit()
    db.refresh(s)
    return s

def delete_subnet(db: Session, subnet_id: int):
    s = db.get(models.Subnet, subnet_id)
    if not s:
        return False
    db.delete(s)
    db.commit()
    return True