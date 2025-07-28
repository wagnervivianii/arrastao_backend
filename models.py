from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    nivel_permissao = db.Column(db.String(50), default='usuario')
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow)

class AutenticacaoLocal(db.Model):
    __tablename__ = 'autenticacao_local'

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    senha_hash = db.Column(db.Text, nullable=False)

class AutenticacaoGoogle(db.Model):
    __tablename__ = 'autenticacao_google'

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    google_sub = db.Column(db.String(255), unique=True, nullable=False)

class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    token = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    expira_em = db.Column(db.DateTime)
