from flask import Flask, request, jsonify
import psycopg2


app = Flask(__name__)

# Função para conectar ao banco de dados PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='barbearia',
        user='postgres',
        password='10081995Ab.'
    )
    return conn

# CRUD para Barbeiros
@app.route('/barbeiros', methods=['GET'])
def get_barbeiros():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM barbeiros;')
    barbeiros = cur.fetchall()
    cur.close()
    conn.close()
    barbeiros_json = []
    for barbeiro_da_vez in barbeiros:
        objeto = {
        "id": barbeiro_da_vez[0],
        'nome': barbeiro_da_vez[1],
        'cpf': barbeiro_da_vez[2],
        'telefone': barbeiro_da_vez[3]
        }
        barbeiros_json.append(objeto)
    return jsonify(barbeiros_json)

@app.route('/barbeiros', methods=['POST'])
def add_barbeiro():
    data = request.get_json()
    nome = data['nome']
    cpf = data['cpf']
    telefone = data['telefone']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO barbeiros (nome, cpf, telefone) VALUES (%s, %s, %s) RETURNING id;',
                (nome, cpf, telefone))
    new_barbeiro_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_barbeiro_id}), 201

@app.route('/barbeiros/<int:id>', methods=['PUT'])
def update_barbeiro(id):
    data = request.get_json()
    nome = data['nome']
    cpf = data['cpf']
    telefone = data['telefone']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE barbeiros SET nome = %s, cpf = %s, telefone = %s WHERE id = %s;',
                (nome, cpf, telefone, id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Barbeiro atualizado com sucesso!"})

@app.route('/barbeiros/<int:id>', methods=['DELETE'])
def delete_barbeiro(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM barbeiros WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Barbeiro deletado com sucesso!"})

# CRUD para Serviços
@app.route('/servicos', methods=['GET'])
def get_servicos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM servicos;')
    servicos = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(servicos)

@app.route('/servicos', methods=['POST'])
def add_servico():
    data = request.get_json()
    nome = data['nome']
    descricao = data['descricao']
    valor = data['valor']
    percentual = data['percentual']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO servicos (nome, descricao, valor, percentual) VALUES (%s, %s, %s, %s) RETURNING id;',
                (nome, descricao, valor, percentual))
    new_servico_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_servico_id}), 201

@app.route('/servicos/<int:id>', methods=['PUT'])
def update_servico(id):
    data = request.get_json()
    nome = data['nome']
    descricao = data['descricao']
    valor = data['valor']
    percentual = data['percentual']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE servicos SET nome = %s, descricao = %s, valor = %s, percentual = %s WHERE id = %s;',
                (nome, descricao, valor, percentual, id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Serviço atualizado com sucesso!"})

@app.route('/servicos/<int:id>', methods=['DELETE'])
def delete_servico(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM servicos WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Serviço deletado com sucesso!"})

# CRUD para Atendimentos
@app.route('/atendimentos', methods=['GET'])
def get_atendimentos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM atendimentos;')
    atendimentos = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(atendimentos)

@app.route('/atendimentos', methods=['POST'])
def add_atendimento():
    data = request.get_json()
    id_barbeiro = data['id_barbeiro']
    id_servico = data['id_servico']
    data_servico = data['data_servico']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO atendimentos (id_barbeiro, id_servico, data_servico) VALUES (%s, %s, %s) RETURNING id;',
                (id_barbeiro, id_servico, data_servico))
    new_atendimento_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_atendimento_id}), 201

@app.route('/atendimentos/<int:id>', methods=['PUT'])
def update_atendimento(id):
    data = request.get_json()
    id_barbeiro = data['id_barbeiro']
    id_servico = data['id_servico']
    data_servico = data['data_servico']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE atendimentos SET id_barbeiro = %s, id_servico = %s, data_servico = %s WHERE id = %s;',
                (id_barbeiro, id_servico, data_servico, id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Atendimento atualizado com sucesso!"})

@app.route('/atendimentos/<int:id>', methods=['DELETE'])
def delete_atendimento(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM atendimentos WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Atendimento deletado com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
