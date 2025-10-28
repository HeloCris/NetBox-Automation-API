from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .discovery import discover_devices
from .netbox_client import NetBoxClient

app = FastAPI()
netbox_client = NetBoxClient()

class DiscoverRequest(BaseModel):
    pass

@app.post("/api/v1/discover")
async def discover(request: DiscoverRequest):
    try:
        devices = discover_devices()
        for device in devices:
            netbox_client.update_or_create_device(device)
        return {"status": "success", "devices": devices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))