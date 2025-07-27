import os
from dotenv import load_dotenv
import psycopg2
from authlib.integrations.flask_client import OAuth
from flask import Flask

class AuthConfig:
    def __init__(self, app: Flask):
        self.app = app
        load_dotenv()
        self.conn = None
        self.ambiente = os.getenv("AMBIENTE", "local")
        self._registrar_oauth()

    def conectar_db(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        return self.conn

    def _registrar_oauth(self):
        oauth = OAuth(self.app)

        prefixo = self.ambiente.upper()
        client_id = os.getenv(f"{prefixo}_GOOGLE_CLIENT_ID")
        client_secret = os.getenv(f"{prefixo}_GOOGLE_CLIENT_SECRET")
        redirect_uri = os.getenv(f"{prefixo}_GOOGLE_REDIRECT_URI")

        oauth.register(
            name='google',
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )

        self.oauth = oauth
        self.redirect_uri = redirect_uri
