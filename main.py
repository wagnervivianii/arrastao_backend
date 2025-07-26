from flask import Flask
from view.auth_routes import auth_routes
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do .env

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Registra o Blueprint de autenticação
app.register_blueprint(auth_routes)

# Rota principal para status
@app.route("/")
def index():
    return "API online: Smollan Brasil Tech"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
