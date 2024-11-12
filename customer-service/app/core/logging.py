import logging
import json
from datetime import datetime
from fastapi import Request

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),  # Horodatage ISO 8601
            "level": record.levelname,
            "message": record.getMessage(),
            "trace_id": getattr(record, 'trace_id', 'N/A'),  # Ajoute trace_id si disponible
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

def log_message(request: Request, message: str, level: str = "info"):
    trace_id = getattr(request.state, "trace_id", "N/A")  # Récupérer trace_id depuis request.state

    if level == "info":
        logger.info(message, extra={"trace_id": trace_id})
    elif level == "error":
        logger.error(message, extra={"trace_id": trace_id})
    else:
        logger.log(logging.DEBUG, message, extra={"trace_id": trace_id})
