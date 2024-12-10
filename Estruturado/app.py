# app.py
from flask import Flask, request, jsonify
from Adaptação.config import Config
from models import db, Barbeiro, Servico, Atendimento
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# CRUD para Barbeiros
@app.route('/barbeiros', methods=['GET'])
def get_barbeiros():
    barbeiros = Barbeiro.query.all()
    return jsonify([{
        'id': barbeiro.id,
        'nome': barbeiro.nome,
        'cpf': barbeiro.cpf,
        'telefone': barbeiro.telefone
    } for barbeiro in barbeiros])

@app.route('/barbeiros', methods=['POST'])
def add_barbeiro():
    data = request.get_json()
    new_barbeiro = Barbeiro(
        nome=data['nome'],
        cpf=data['cpf'],
        telefone=data['telefone']
    )
    db.session.add(new_barbeiro)
    db.session.commit()
    return jsonify({'id': new_barbeiro.id}), 201

@app.route('/barbeiros/<int:id>', methods=['PUT'])
def update_barbeiro(id):
    data = request.get_json()
    barbeiro = Barbeiro.query.get(id)
    if barbeiro:
        barbeiro.nome = data['nome']
        barbeiro.cpf = data['cpf']
        barbeiro.telefone = data['telefone']
        db.session.commit()
        return jsonify({'message': 'Barbeiro atualizado com sucesso!'})
    return jsonify({'message': 'Barbeiro não encontrado!'}), 404

@app.route('/barbeiros/<int:id>', methods=['DELETE'])
def delete_barbeiro(id):
    barbeiro = Barbeiro.query.get(id)
    if barbeiro:
        db.session.delete(barbeiro)
        db.session.commit()
        return jsonify({'message': 'Barbeiro deletado com sucesso!'})
    return jsonify({'message': 'Barbeiro não encontrado!'}), 404

# CRUD para Serviços
@app.route('/servicos', methods=['GET'])
def get_servicos():
    servicos = Servico.query.all()
    return jsonify([{
        'id': servico.id,
        'nome': servico.nome,
        'descricao': servico.descricao,
        'valor': str(servico.valor),
        'percentual': str(servico.percentual)
    } for servico in servicos])

@app.route('/servicos', methods=['POST'])
def add_servico():
    data = request.get_json()
    new_servico = Servico(
        nome=data['nome'],
        descricao=data['descricao'],
        valor=data['valor'],
        percentual=data['percentual']
    )
    db.session.add(new_servico)
    db.session.commit()
    return jsonify({'id': new_servico.id}), 201

@app.route('/servicos/<int:id>', methods=['PUT'])
def update_servico(id):
    data = request.get_json()
    servico = Servico.query.get(id)
    if servico:
        servico.nome = data['nome']
        servico.descricao = data['descricao']
        servico.valor = data['valor']
        servico.percentual = data['percentual']
        db.session.commit()
        return jsonify({'message': 'Serviço atualizado com sucesso!'})
    return jsonify({'message': 'Serviço não encontrado!'}), 404

@app.route('/servicos/<int:id>', methods=['DELETE'])
def delete_servico(id):
    servico = Servico.query.get(id)
    if servico:
        db.session.delete(servico)
        db.session.commit()
        return jsonify({'message': 'Serviço deletado com sucesso!'})
    return jsonify({'message': 'Serviço não encontrado!'}), 404

# CRUD para Atendimentos
@app.route('/atendimentos', methods=['GET'])
def get_atendimentos():
    atendimentos = Atendimento.query.all()
    return jsonify([{
        'id': atendimento.id,
        'data_servico': atendimento.data_servico,
        'id_barbeiro': atendimento.id_barbeiro,
        'id_servico': atendimento.id_servico
    } for atendimento in atendimentos])

@app.route('/atendimentos', methods=['POST'])
def add_atendimento():
    data = request.get_json()
    new_atendimento = Atendimento(
        data_servico=datetime.strptime(data['data_servico'], '%Y-%m-%d %H:%M:%S'),
        id_barbeiro=data['id_barbeiro'],
        id_servico=data['id_servico']
    )
    db.session.add(new_atendimento)
    db.session.commit()
    return jsonify({'id': new_atendimento.id}), 201

@app.route('/atendimentos/<int:id>', methods=['PUT'])
def update_atendimento(id):
    data = request.get_json()
    atendimento = Atendimento.query.get(id)
    if atendimento:
        atendimento.data_servico = datetime.strptime(data['data_servico'], '%Y-%m-%d %H:%M:%S')
        atendimento.id_barbeiro = data['id_barbeiro']
        atendimento.id_servico = data['id_servico']
        db.session.commit()
        return jsonify({'message': 'Atendimento atualizado com sucesso!'})
    return jsonify({'message': 'Atendimento não encontrado!'}), 404

@app.route('/atendimentos/<int:id>', methods=['DELETE'])
def delete_atendimento(id):
    atendimento = Atendimento.query.get(id)
    if atendimento:
        db.session.delete(atendimento)
        db.session.commit()
        return jsonify({'message': 'Atendimento deletado com sucesso!'})
    return jsonify({'message': 'Atendimento não encontrado!'}), 404

if __name__ == '__main__':
    app.run(debug=True)
