import consul
import socket
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
