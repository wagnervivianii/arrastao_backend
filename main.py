from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from models import db, Usuario, AutenticacaoLocal
from view.auth_routes import auth_routes

import os

# Carrega variáveis de ambiente
load_dotenv()

# Instancia o app
app = Flask(__name__)
CORS(app)

# Configurações de segurança
app.secret_key = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Configuração do banco PostgreSQL com SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicia extensões
jwt = JWTManager(app)
db.init_app(app)

# Blueprints
app.register_blueprint(auth_routes)

# Rota simples de status
@app.route("/")
def index():
    return "API online: Smollan Brasil Tech"

# Rota de teste de banco
@app.route("/test-db")
def test_db():
    try:
        usuarios = db.session.execute("SELECT * FROM usuarios LIMIT 5").fetchall()
        return jsonify([dict(u) for u in usuarios])
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota /register
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not nome or not email or not senha:
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "E-mail já cadastrado."}), 409

    novo_usuario = Usuario(nome=nome, email=email)
    db.session.add(novo_usuario)
    db.session.commit()

    senha_hash = generate_password_hash(senha)
    auth = AutenticacaoLocal(id_usuario=novo_usuario.id, senha_hash=senha_hash)
    db.session.add(auth)
    db.session.commit()

    return jsonify({
        "mensagem": "Usuário registrado com sucesso!",
        "id": novo_usuario.id,
        "nome": novo_usuario.nome,
        "email": novo_usuario.email
    }), 201

# Executa o app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
