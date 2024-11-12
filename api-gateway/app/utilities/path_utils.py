# Configuration des exclusions avec expressions régulières pour chaque méthode HTTP
import re


EXCLUDED_PATHS = {
    "GET": [
        re.compile(r"^api_docs$"),
        re.compile(r"^docs$"),
        re.compile(r"^healthcheck$"),
        # Ajouter d'autres motifs pour les endpoints GET à exclure ici
    ],
    "POST": [
        re.compile(r"^api/v1/users$"),
        re.compile(r"^api/v1/auth/login$"),
        re.compile(r"^api/v1/auth/request-otp$"),
        re.compile(r"^api/v1/auth/verify-otp$"),
        # Ajouter d'autres motifs pour les endpoints POST à exclure ici
    ],
    "PUT": [
        re.compile(r"^api/v1/auth/reset-password$"),
        # Ajouter d'autres motifs pour les endpoints PUT à exclure ici
    ],
    "DELETE": [
        # Ajouter d'autres motifs pour les endpoints DELETE à exclure ici
    ],
    "PATCH": [
        # Ajouter d'autres motifs pour les endpoints PATCH à exclure ici
    ],
    "OPTIONS": [
        # Ajouter d'autres motifs pour les endpoints OPTIONS à exclure ici
    ],
    "HEAD": [
        # Ajouter d'autres motifs pour les endpoints HEAD à exclure ici
    ]
}