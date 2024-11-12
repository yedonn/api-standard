import socket
import consul
from app.core.config import settings

consul_client = consul.Consul(host='consul', port=settings.CONSUL_PORT)
service_cache = {}

def register_service():
    try:
        consul_client.agent.service.register(
            name=settings.SERVICE_NAME.lower().replace(' ', '-'),
            service_id=f"{settings.SERVICE_NAME.lower().replace(' ', '-')}-1",
            address=socket.gethostbyname(socket.gethostname()),
            port=settings.SERVICE_PORT,
            check=consul.Check.http(f"http://{socket.gethostbyname(socket.gethostname())}:{settings.SERVICE_PORT}/healthcheck", interval="10s")
        )
        print("Service registered successfully.")
    except Exception as e:
        print(f"Failed to register service: {e}")

def get_service_url(service_name: str) -> str:
    services = consul_client.agent.services()
    for service in services.values():
        if service['Service'] == service_name:
            return f"http://{service['Address']}:{service['Port']}"
    return None

def update_service_cache():
    global service_cache
    services = consul_client.catalog.services()[1]
    for service_name in services.keys():
        service_url = get_service_url(service_name)
        if service_url:
            service_cache[service_name] = service_url
