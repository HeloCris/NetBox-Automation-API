# NetBox Automation API

Este projeto é uma API REST projetada para automatizar a documentação da infraestrutura de rede, descobrindo dispositivos e atualizando o inventário do NetBox. Ele fornece endpoints para a descoberta de dispositivos e se integra com a API do NetBox para gerenciar as informações dos dispositivos de rede.

## Features

- Descoberta de dispositivos usando dados SNMP
- Integração com o NetBox para gerenciamento de inventário
- Endpoints de API RESTful para interação

## Estrutura do Projeto
## Project Structure

```
netbox-automation-api
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api.py
│   ├── discovery.py
│   ├── netbox_client.py
│   └── config.py
├── tests
│   ├── __init__.py
│   ├── test_api.py
│   └── test_discovery.py
├── requirements.txt
└── README.md
```

## Instruções de Configuração

1. Clone o repositório:
   ```
   git clone <repository-url>
   cd netbox-automation-api
   ```
2. Crie um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Instale as dependências necessárias:
   ```
   pip install -r requirements.txt
   
## Uso

Para executar a aplicação, execute o seguinte comando:
```
python app/main.py
```

A API estará disponível em `http://localhost:8000`.

## Endpoints da API

- `POST /api/v1/discover`: Inicia o processo de descoberta de dispositivos.

## Decisões de Design

- A aplicação foi construída usando uma estrutura modular para separar as responsabilidades, facilitando a manutenção e extensão.
- O uso de uma API RESTful permite fácil integração com outras ferramentas e sistemas.

## Contribuição

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request para quaisquer melhorias ou correções de bugs.