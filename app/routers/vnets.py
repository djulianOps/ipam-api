from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal, Base, engine
from .. import schemas, crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

@router.post("/", response_model=schemas.VNetOut, status_code=201)
def create_vnet(payload: schemas.VNetCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_vnet(db, payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[schemas.VNetOut])
def list_vnets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vnets(db, skip, limit)

@router.get("/{vnet_id}", response_model=schemas.VNetOut)
def get_vnet(vnet_id: int, db: Session = Depends(get_db)):
    v = crud.get_vnet(db, vnet_id)
    if not v:
        raise HTTPException(status_code=404, detail="VNet not found")
    return v

@router.patch("/{vnet_id}", response_model=schemas.VNetOut)
def update_vnet(vnet_id: int, payload: schemas.VNetUpdate, db: Session = Depends(get_db)):
    try:
        v = crud.update_vnet(db, vnet_id, payload)
        if not v:
            raise HTTPException(status_code=404, detail="VNet not found")
        return v
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{vnet_id}", status_code=204)
def delete_vnet(vnet_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_vnet(db, vnet_id)
    if not ok:
        raise HTTPException(status_code=404, detail="VNet not found")