import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    NETBOX_API_URL = os.getenv('NETBOX_API_URL', 'http://localhost:8000/api/v2/')
    NETBOX_TOKEN = os.getenv('NETBOX_TOKEN', 'your_netbox_token_here')
    DISCOVERY_DATA_FILE = os.getenv('DISCOVERY_DATA_FILE', 'data/discovery.json')
    TIMEOUT = int(os.getenv('TIMEOUT', 10))  # seconds
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))