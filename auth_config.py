import json
import psycopg2
from authlib.integrations.flask_client import OAuth
from flask import Flask


class AuthConfig:
    def __init__(self, app: Flask, caminho_config_db='config.json', caminho_config_auth='config_auth.json'):
        self.app = app
        self._carregar_configuracoes(caminho_config_db, caminho_config_auth)
        self.conn = None
        self._registrar_oauth()

    def _carregar_configuracoes(self, caminho_db, caminho_auth):
        with open(caminho_db) as f:
            self.db_cfg = json.load(f)

        with open(caminho_auth) as f:
            auth_cfg = json.load(f)
            ambiente = auth_cfg["ambiente"]
            self.auth_cfg = auth_cfg[ambiente]

    def conectar_db(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(
                dbname=self.db_cfg["dbname"],
                user=self.db_cfg["user"],
                password=self.db_cfg["password"],
                host=self.db_cfg["host"],
                port=self.db_cfg["port"]
            )
        return self.conn

    def _registrar_oauth(self):
        oauth = OAuth(self.app)
        oauth.register(
            name='google',
            client_id=self.auth_cfg["client_id"],
            client_secret=self.auth_cfg["client_secret"],
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        self.oauth = oauth
        self.redirect_uri = self.auth_cfg["redirect_uri"]




