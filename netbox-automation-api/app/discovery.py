from typing import List, Dict
import json

class DeviceDiscovery:
    def __init__(self, data_file: str):
        self.data_file = data_file

    def discover_devices(self) -> List[Dict]:
        with open(self.data_file, 'r') as file:
            data = json.load(file)
        
        devices = []
        for device in data.get('devices', []):
            device_info = {
                'name': device.get('name'),
                'ip_address': device.get('ip_address'),
                'mac_address': device.get('mac_address'),
                'device_type': device.get('device_type'),
                'vendor': device.get('vendor'),
            }
            devices.append(device_info)
        
        return devices

    def filter_devices(self, devices: List[Dict], criteria: Dict) -> List[Dict]:
        filtered_devices = []
        for device in devices:
            if all(device.get(key) == value for key, value in criteria.items()):
                filtered_devices.append(device)
        return filtered_devices