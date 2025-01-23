import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
import requests
from authlib.integrations.requests_client import OAuth2Session

class OAuthManager:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

    def get_oauth_session(self):
        client_id = self.config["oauth"]["client_id"]
        client_secret = self.config["oauth"]["client_secret"]
        redirect_uri = self.config["oauth"]["redirect_uri"]
        return OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

    def get_auth_url(self):
        oauth_session = self.get_oauth_session()
        auth_url = self.config["oauth"]["provider"]["auth_url"]
        return oauth_session.create_authorization_url(auth_url, access_type="offline")

    def fetch_token(self, code):
        oauth_session = self.get_oauth_session()
        token_url = self.config["oauth"]["provider"]["token_url"]
        token = oauth_session.fetch_token(token_url, code=code)
        
        # Guardar el refresh token
        if "refresh_token" in token:
            token["refresh_token"] = token["refresh_token"]
        return token

    def refresh_access_token(self, refresh_token):
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
