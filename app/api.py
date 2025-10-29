from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .discovery import DeviceDiscovery  
from .netbox_client import NetBoxClient

app = FastAPI()
netbox_client = NetBoxClient()


try:
    discovery_client = DeviceDiscovery(data_file="app/devices.json")
except FileNotFoundError:
    print("ERRO: O arquivo 'app/devices.json' não foi encontrado.")

    discovery_client = None 

class DiscoverRequest(BaseModel):
    pass

@app.post("/api/v1/discover")
async def discover(request: DiscoverRequest):
    if discovery_client is None:
        raise HTTPException(status_code=500, detail="Erro no servidor: arquivo de dados de discovery não encontrado.")

    try:
        devices = discovery_client.discover_devices() 
        
        for device in devices:
            netbox_client.update_or_create_device(device)
        return {"status": "success", "devices": devices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))