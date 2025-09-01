import logging
import logging.config
import time
from fastapi import FastAPI, Request
from app.routers import vnets, subnets
from app.database import Base, engine

logging.config.fileConfig("app/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("app.requests")

app = FastAPI(title="IPAM API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = f"{request.method} {request.url.path}"
    body = await request.body()
    logger.info(f"START {idem} body={body.decode('utf-8') if body else None}")
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"END {idem} status={response.status_code} duration={duration:.3f}s")
    return response

app.include_router(vnets.router, prefix="/vnets", tags=["Vnets"])
app.include_router(subnets.router, prefix="/subnets", tags=["Subnets"])

@app.get("/ping", tags=["Healthy"])
def ping():
    return {"ping": "pong"}