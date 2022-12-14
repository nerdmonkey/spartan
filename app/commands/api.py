import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter
from .models import Commands
from ..devices.models import Devices
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class InfoCommand(BaseModel):
    device_id: int

class WorkCommand(BaseModel):
    device_id: int
    value: int

router = APIRouter(
    prefix="/api",
    tags=["Commands"],
    responses={404: {"description": "Resource not found"}}
)

@router.post('/commands/info')
async def fetch_info_command(command: InfoCommand, db: Session=Depends(get_db)):

    # Get device info
    data = db.query(Devices)\
                    .filter(Devices.id == command.device_id)\
                    .first()

    # Hardware communication here
    address = data.address
    unit = data.unit

    # Get result value
    get_this_value = 30

    return {
        'data': {
            'address': address,
            'unit': unit,
            'value': get_this_value
        },
        'status': 200
    }

@router.post('/commands/work')
async def do_work_command(command: WorkCommand, db: Session=Depends(get_db)):

    # Get device info
    data = db.query(Devices)\
                    .filter(Devices.id == command.device_id)\
                    .first()

    # Hardware communication here
    address = data.address
    unit = data.unit

    # Set value to the device
    set_this_value = True

    return {
        'data': {
            'address': address,
            'unit': unit,
            'value': set_this_value
        },
        'status': 200
    }
