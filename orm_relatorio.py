from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Barbeiro(db.Model):
    __tablename__ = 'barbeiros'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

class Servico(db.Model):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    percentual = db.Column(db.Float, nullable=False)  # Percentual em formato decimal (ex.: 0.5)

class Atendimento(db.Model):
    __tablename__ = 'atendimentos'
    id = db.Column(db.Integer, primary_key=True)
    id_barbeiro = db.Column(db.Integer, db.ForeignKey('barbeiros.id'), nullable=False)
    id_servico = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    data_servico = db.Column(db.Date, nullable=False)

    barbeiro = db.relationship('Barbeiro', backref='atendimentos')
    servico = db.relationship('Servico', backref='atendimentos')




from sqlalchemy import func
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/relatorio/faturamento-mensal', methods=['GET'])
def relatorio_faturamento_mensal():
    mes = request.args.get('mes', type=int)
    ano = request.args.get('ano', type=int)

    if not mes or not ano:
        return jsonify({'error': 'Informe os parâmetros "mes" e "ano" para o relatório.'}), 400

    # Consulta utilizando ORM
    resultado = (
        db.session.query(
            Barbeiro.id.label('id_barbeiro'),
            Barbeiro.nome.label('Nome_Barbeiro'),
            func.count(Atendimento.id).label('quantidade_servicos'),
            func.sum(Servico.valor).label('total_servicos'),
            func.sum(Servico.valor * Servico.percentual).label('valor_a_receber')
        )
        .join(Atendimento, Atendimento.id_barbeiro == Barbeiro.id)
        .join(Servico, Atendimento.id_servico == Servico.id)
        .filter(func.month(Atendimento.data_servico) == mes)
        .filter(func.year(Atendimento.data_servico) == ano)
        .group_by(Barbeiro.id)
        .all()
    )

    # Faturamento total
    faturamento_total = sum(r.total_servicos for r in resultado)

    # Formatar os dados
    barbeiros = [
        {
            'id_barbeiro': r.id_barbeiro,
            'barbeiro': r.Nome_Barbeiro,
            'quantidade_servicos': r.quantidade_servicos,
            'total_servicos': f"{r.total_servicos:.2f}",
            'valor_a_receber': f"{r.valor_a_receber:.2f}"
        }
        for r in resultado
    ]

    return jsonify({
        'mes': mes,
        'ano': ano,
        'faturamento_total': f"{faturamento_total:.2f}",
        'barbeiros': barbeiros
    })
