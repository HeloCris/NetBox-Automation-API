import os
import requests
from typing import Optional, Dict, Any

class NetBoxClient:
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None, verify: bool = True):
        """
        Inicializa o cliente.
        Tenta pré-carregar IDs essenciais para a criação de dispositivos.
        """
        self.base_url = (base_url or os.getenv("NETBOX_URL") or "").rstrip("/")
        self.token = token or os.getenv("NETBOX_TOKEN")
        self.verify = verify

        if not self.base_url or not self.token:
            raise ValueError("NETBOX_URL e NETBOX_TOKEN devem estar configurados.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

        self.endpoints = {
            "devices": f"{self.base_url}/api/dcim/devices/",
            "sites": f"{self.base_url}/api/dcim/sites/",
            "device_roles": f"{self.base_url}/api/dcim/device-roles/",
            "device_types": f"{self.base_url}/api/dcim/device-types/",
            "manufacturers": f"{self.base_url}/api/dcim/manufacturers/",
        }

        print("NetBox Client inicializado!")
        
        
        self.site_cache = {}
        
        
        try:
            self.default_ids = self._get_default_ids()
            print("IDs padrão (Site, Role, Type) carregados com sucesso.")
        except Exception as e:
            print(f"ERRO FATAL: Não foi possível carregar os IDs padrão (Descoberto).")
            print("Por favor, crie no NetBox (via GUI):")
            print(" 1. Manufacturer (Fabricante) com nome 'Descoberto'")
            print(" 2. Device Type (Tipo) com nome 'Descoberto' (usando o Manufacturer acima)")
            print(" 3. Device Role (Função) com nome 'Descoberto'")
            print(f"Erro original: {e}")
            raise 

    def _request(self, method: str, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Função de requisição interna.
        AGORA LEVANTA EXCEÇÃO EM CASO DE ERRO.
        """
        try:
            resp = self.session.request(method, url, verify=self.verify, timeout=30, **kwargs)
            
            resp.raise_for_status() 
            
          
            if resp.status_code == 204 or not resp.text:
                return {}
            
            return resp.json()
        except requests.RequestException as exc:
            print(f"Erro na requisição NetBox ({method} {url}): {exc}")
            
            if exc.response is not None:
                try:
                    print(f"Detalhe do Erro: {exc.response.json()}")
                except requests.exceptions.JSONDecodeError:
                    print(f"Detalhe do Erro: {exc.response.text}")
            
            
            raise exc

    def _find_id_by_name(self, endpoint_key: str, name: str) -> Optional[int]:
        """Função genérica para encontrar o ID de um objeto pelo nome."""
        url = self.endpoints[endpoint_key]
        try:
            
            resp = self._request("GET", url, params={"name": name})
            if resp and resp.get("count", 0) > 0:
                return resp["results"][0]["id"]
        except requests.RequestException:
           
            print(f"Aviso: Falha ao buscar '{name}' em {endpoint_key}. A requisição pode falhar.")
        return None

    def _get_or_create_id(self, endpoint_key: str, name: str, payload: Dict[str, Any]) -> Optional[int]:
        """Tenta encontrar, se não achar, tenta criar."""
        found_id = self._find_id_by_name(endpoint_key, name)
        if found_id:
            return found_id
        
      
        print(f"Criando recurso padrão '{name}' em {endpoint_key}...")
        try:
            resp = self._request("POST", self.endpoints[endpoint_key], json=payload)
            if resp and "id" in resp:
                print(f"Recurso '{name}' criado com ID: {resp['id']}")
                return resp["id"]
        except requests.RequestException as e:
            print(f"Falha CRÍTICA ao tentar criar recurso padrão '{name}': {e}")
            raise 
        
        
        raise Exception(f"Não foi possível criar o recurso padrão '{name}'")


    def _get_default_ids(self) -> Dict[str, int]:
        """
        Busca os IDs dos objetos padrão que usaremos como fallback.
        Se não existirem, tenta criá-los.
        """
       
        mf_id = self._get_or_create_id(
            "manufacturers", "Descoberto",
            {"name": "Descoberto", "slug": "descoberto"}
        )

       
        dt_id = self._get_or_create_id(
            "device_types", "Descoberto",
            {"name": "Descoberto", "slug": "descoberto", "manufacturer": mf_id}
        )
        
        dr_id = self._get_or_create_id(
            "device_roles", "Descoberto",
            {"name": "Descoberto", "slug": "descoberto", "color": "9e9e9e"}
        )

        site_id = self._get_or_create_id(
            "sites", "Descoberto",
            {"name": "Descoberto", "slug": "descoberto"}
        )

        if not all([mf_id, dt_id, dr_id, site_id]):
            raise Exception("Falha ao obter todos os IDs padrão. Verifique as permissões do token.")

        return {"device_type": dt_id, "role": dr_id, "site": site_id}


    def get_site_id(self, site_name: str) -> int:
        """
        Busca o ID do Site. Se não achar, usa o ID padrão "Descoberto".
        """
        if not site_name:
            return self.default_ids["site"]
            
       
        if site_name in self.site_cache:
            return self.site_cache[site_name]
        
       
        found_id = self._find_id_by_name("sites", site_name)
        if found_id:
            self.site_cache[site_name] = found_id
            return found_id
        
        
        print(f"Aviso: Site '{site_name}' não encontrado. Usando 'Descoberto' como padrão.")
        return self.default_ids["site"]

    def get_device_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        params = {"name": name}
        resp = self._request("GET", self.endpoints["devices"], params=params)
        
        if not resp: 
            return None
            
        results = resp.get("results") if isinstance(resp, dict) else None
        if results and len(results) > 0:
            return results[0]
        return None

    def _prepare_payload(self, device_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara o payload final, mapeando e adicionando IDs obrigatórios.
        """
        
        location_str = device_data.get("sysLocation")
        
        
        payload = {
            "name": device_data.get("name"), 
            "site": self.get_site_id(location_str),
            "role": self.default_ids["role"],
            "device_type": self.default_ids["device_type"],
            
            "primary_ip4": None, 
        }
        
        
        payload = {k: v for k, v in payload.items() if v is not None}
        return payload

    def create_device(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        print(f"Criando dispositivo: {payload.get('name')}")
        return self._request("POST", self.endpoints["devices"], json=payload)

    def update_device(self, device_id: int, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.endpoints['devices']}{device_id}/"
        print(f"Atualizando dispositivo id={device_id} nome={payload.get('name')}")
        return self._request("PATCH", url, json=payload)

    def update_or_create_device(self, device_data: Dict[str, Any]):
        """
        Tenta encontrar dispositivo pelo 'name'. Se existir atualiza, senão cria.
        A lógica de erro agora é tratada pela exceção do _request.
        """
        name = device_data.get("name")
        if not name:
            print("Erro: device_data deve conter o campo 'name'.")
            raise ValueError(f"Dados do dispositivo inválidos: sem 'name'. Dados: {device_data}")

        payload = self._prepare_payload(device_data)

        existing = self.get_device_by_name(name)
        if existing and isinstance(existing, dict) and existing.get("id"):
            
            payload.pop("name", None) 
            self.update_device(existing["id"], payload)
        else:
           
            self.create_device(payload)
        
      

