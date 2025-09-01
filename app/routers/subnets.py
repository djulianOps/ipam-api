from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete("/{subnet_id}", status_code=204)
def delete_subnet(subnet_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_subnet(db, subnet_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Subnet not found")
    
@router.get("/search", response_model=schemas.SubnetOut)
def get_subnet_by_cidr(cidr: str, db: Session = Depends(get_db)):
    subnet = db.query(models.Subnet).filter(models.Subnet.cidr == cidr).first()
    if not subnet:
        raise HTTPException(status_code=404, detail="Subnet not found")
    return subnet