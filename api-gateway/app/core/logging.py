import logging
import json
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),  # Horodatage ISO 8601
            "level": record.levelname,
            "message": record.getMessage(),
            "trace_id": record.__dict__.get('trace_id', 'N/A'),  # Ajoute trace_id si disponible
            "name": record.name
        }
        return json.dumps(log_record)

def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Handler pour la sortie en JSON
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(JSONFormatter())
    logger.addHandler(json_handler)

    return logger

logger = configure_logger()

# Fonction pour loguer les messages en incluant le trace_id depuis request.state
def log_message(request: Request, message: str, level: str):
    trace_id = getattr(request.state, "trace_id", "N/A")  # Récupérer trace_id depuis request.state
    log_data = {
        "message": message,
        "trace_id": trace_id
    }

    if level == "info":
        logger.info(json.dumps(log_data))
    elif level == "error":
        logger.error(json.dumps(log_data))
    else:
        logger.log(logging.DEBUG, json.dumps(log_data))