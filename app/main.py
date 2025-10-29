import json
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

try:
    from app.netbox_client import NetBoxClient
    from app.discovery import DeviceDiscovery
except ImportError as e:
    print(f"Erro de importação: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Erro ao inicializar o script: {e}")
    sys.exit(1)


def run_discovery():
    """
    Função principal para executar a descoberta e atualização do NetBox.
    """
    print("Iniciando o script de descoberta...")

    data_file_path = os.path.join(project_root, 'simulated_snmp_data.json')
    print(f"Carregando dados de: {data_file_path}")

    try:
        netbox_client = NetBoxClient()
    except ValueError as e:
        print(f"ERRO FATAL ao inicializar o NetBox Client: {e}")
        return
    except Exception as e:
        print(f"ERRO FATAL inesperado no NetBox Client: {e}")
        return

    try:
        discovery_client = DeviceDiscovery(data_file=data_file_path)
        print("Módulo de descoberta (discovery) inicializado.")
    except Exception as e:
        print(f"ERRO CRÍTICO ao iniciar o discovery: {e}")
        return

    try:
        print("Executando a descoberta de dispositivos (lendo o JSON)...")
        devices = discovery_client.discover_devices()
        if not devices:
             print("Nenhum dispositivo encontrado no arquivo JSON.")
             return
        print(f"Descoberta concluída. {len(devices)} dispositivos encontrados no arquivo.")
    except Exception as e:
        print(f"Erro durante a fase de descoberta (discover_devices): {e}")
        return

    print("\nIniciando atualização no NetBox...")
    if not devices:
        print("Nenhum dispositivo para atualizar.")
        return

    success_count = 0
    fail_count = 0

    for device in devices:
        try:
            device_name = device.get('sysName', 'Nome desconhecido')
            print(f"  -> Processando dispositivo: {device_name}")

            if 'name' not in device and 'sysName' in device:
                device['name'] = device['sysName']
            
            netbox_client.update_or_create_device(device)
            
            print(f"     [OK] Dispositivo '{device_name}' atualizado/criado.")
            success_count += 1
            
        except Exception as e:
            
            print(f"     [ERRO] Falha ao processar o dispositivo '{device_name}'.")
            fail_count += 1

    print("\n--- Processamento Concluído ---")
    print(f"Sucesso: {success_count} dispositivos")
    print(f"Falhas:  {fail_count}")
    print("---------------------------------")


if __name__ == "__main__":
    run_discovery()

