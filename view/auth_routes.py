from flask import Blueprint, jsonify
from controller.auth_controller import processar_callback
from auth_config import AuthConfig
from flask import Flask

# Instancia local apenas para registrar OAuth e conexão
app_temp = Flask(__name__)
app_temp.secret_key = 'chave_temp'
auth = AuthConfig(app_temp)
oauth = auth.oauth
redirect_uri = auth.redirect_uri
conectar_db = auth.conectar_db

# Criar Blueprint
auth_routes = Blueprint('auth', __name__)

@auth_routes.route("/login_google")
def login_google():
    return oauth.google.authorize_redirect(redirect_uri=redirect_uri)

@auth_routes.route("/callback")
def callback():
    resposta, status = processar_callback(oauth, redirect_uri, conectar_db)
    return jsonify(resposta), status
