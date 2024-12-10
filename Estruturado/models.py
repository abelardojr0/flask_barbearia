# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Barbeiro(db.Model):
    __tablename__ = 'barbeiros'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    
    atendimentos = db.relationship('Atendimento', backref='barbeiro', lazy=True)

    def __repr__(self):
        return f"<Barbeiro {self.nome}>"

class Servico(db.Model):
    __tablename__ = 'servicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    percentual = db.Column(db.Numeric(5, 2), nullable=False)

    atendimentos = db.relationship('Atendimento', backref='servico', lazy=True)

    def __repr__(self):
        return f"<Servico {self.nome}>"

class Atendimento(db.Model):
    __tablename__ = 'atendimentos'
    
    id = db.Column(db.Integer, primary_key=True)
    data_servico = db.Column(db.DateTime, nullable=False)
    
    id_barbeiro = db.Column(db.Integer, db.ForeignKey('barbeiros.id'), nullable=False)
    id_servico = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)

    def __repr__(self):
        return f"<Atendimento {self.id}>"
