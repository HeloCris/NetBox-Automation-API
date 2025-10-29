from typing import List, Dict
import json
import sys

class DeviceDiscovery:
    def __init__(self, data_file: str):
        self.data_file = data_file
        if not self.data_file:
            print("ERRO: Nenhum arquivo de dados fornecido para DeviceDiscovery.")
            sys.exit(1)

    def discover_devices(self) -> List[Dict]:
        """
        Carrega os dados do arquivo JSON.

        A estrutura de dados esperada é:
        {
            "IP_ADDRESS_1": { "sysName": "...", "interfaces": [...] },
            "IP_ADDRESS_2": { "sysName": "...", "interfaces": [...] }
        }
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"ERRO no Discovery: O arquivo {self.data_file} não foi encontrado.")
            return []
        except json.JSONDecodeError:
            print(f"ERRO no Discovery: O arquivo {self.data_file} contém um JSON inválido ou está vazio.")
            return []
        except Exception as e:
            print(f"ERRO no Discovery: Falha ao ler o arquivo {self.data_file}: {e}")
            return []

        
       
        if not isinstance(data, dict) or not data:
            print("ERRO no Discovery: O JSON carregado não é um dicionário ou está vazio.")
            return []

        devices = []
        
      
        for ip, device_data in data.items():
            
        
            device_data['management_ip'] = ip
            
            devices.append(device_data)
    
        return devices

    def filter_devices(self, devices: List[Dict], criteria: Dict) -> List[Dict]:
        """
        Filtra a lista de dispositivos com base em critérios.
        (Esta função não é usada pelo main.py, mas a mantemos.)
        """
        filtered_devices = []
        for device in devices:
            if all(device.get(key) == value for key, value in criteria.items()):
                filtered_devices.append(device)
        return filtered_devices
