from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from controller.auth_controller import processar_callback
from auth_config import AuthConfig
from flask import Flask

# Blueprint de autenticação
auth_routes = Blueprint("auth_routes", __name__)

# Instância temporária apenas para registrar o OAuth2 (não interfere no app principal)
app_temp = Flask(__name__)
app_temp.secret_key = 'chave_temp'  # OK para uso isolado com Authlib
auth = AuthConfig(app_temp)
oauth = auth.oauth
redirect_uri = auth.redirect_uri
conectar_db = auth.conectar_db

#  Login com usuário e senha
@auth_routes.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    # Validação temporária (substituir pela sua regra real)
    if usuario == "admin" and senha == "123":
        token = create_access_token(identity=usuario)
        return jsonify(access_token=token), 200

    return jsonify({"msg": "Usuário ou senha inválido"}), 401

# Rota protegida com JWT
@auth_routes.route("/dados-protegidos", methods=["GET"])
@jwt_required()
def dados():
    usuario = get_jwt_identity()
    return jsonify(msg=f"Bem-vindo, {usuario}. Este conteúdo é protegido.")

# Login com Google
@auth_routes.route("/login_google")
def login_google():
    return oauth.google.authorize_redirect(redirect_uri=redirect_uri)

#Callback do Google
@auth_routes.route("/callback")
def callback():
    resposta, status = processar_callback(oauth, redirect_uri, conectar_db)
    return jsonify(resposta), status
