from flask import Flask
from view.auth_routes import auth_routes

app = Flask(__name__)
app.secret_key = '5f1c43ab971e432e91b8d91441e94fd7'

# Registra o Blueprint de autenticação
app.register_blueprint(auth_routes)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5000)