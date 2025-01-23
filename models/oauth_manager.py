import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
import requests
from authlib.integrations.requests_client import OAuth2Session


class OAuthManager:
    def __init__(self, config_path="config.yaml"):
        """
        Inicializa el administrador de OAuth cargando la configuración desde un archivo YAML.
        """
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)
        self.scope = self.config["oauth"].get("scope", "")  # Cargar el scope desde la configuración
        self.revoke_url = self.config["oauth"]["provider"]["revoke_url"]

    def get_oauth_session(self):
        """
        Configura y retorna una sesión OAuth2 con los detalles del cliente y el scope.
        """
        client_id = self.config["oauth"]["client_id"]
        client_secret = self.config["oauth"]["client_secret"]
        redirect_uri = self.config["oauth"]["redirect_uri"]
        return OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri, scope=self.scope)

    def get_auth_url(self):
        """
        Genera la URL de autorización para iniciar el flujo OAuth2.
        """
        oauth_session = self.get_oauth_session()
        auth_url = self.config["oauth"]["provider"]["auth_url"]
        return oauth_session.create_authorization_url(auth_url, access_type="offline")

    def fetch_token(self, code):
        """
        Intercambia el código de autorización por un token de acceso.
        """
        oauth_session = self.get_oauth_session()
        token_url = self.config["oauth"]["provider"]["token_url"]
        token = oauth_session.fetch_token(token_url, code=code)

        # Guardar el refresh token si está presente
        if "refresh_token" in token:
            token["refresh_token"] = token["refresh_token"]
        return token

    def refresh_access_token(self, refresh_token):
        """
        Refresca el token de acceso utilizando el refresh token.
        """
        client_id = self.config["oauth"]["client_id"]
        client_secret = self.config["oauth"]["client_secret"]
        token_url = self.config["oauth"]["provider"]["token_url"]

        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }

        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al refrescar el token: {response.json()}")

    def get_user_info(self, token):
        """
        Obtiene la información del usuario autenticado utilizando el token de acceso.
        """
        user_info_url = self.config["oauth"]["provider"]["user_info_url"]
        response = requests.get(user_info_url, headers={"Authorization": f"Bearer {token['access_token']}"}).json()
        return response

    def revoke_token(self, token):
        """
        Revoca un token de acceso para cerrar sesión correctamente.

        Args:
            token (dict): El token que contiene el access_token.

        Raises:
            Exception: Si ocurre un error al intentar revocar el token.
        """
        if "access_token" not in token:
            raise ValueError("El token no contiene un access_token válido.")

        access_token = token["access_token"]
        response = requests.post(
            self.revoke_url,
            params={"token": access_token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            print("Token revocado correctamente.")
        else:
            raise Exception(f"Error al revocar el token: {response.status_code} {response.text}")
