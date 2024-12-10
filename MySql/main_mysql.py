from flask import Flask, jsonify, request
from db_mysql import fazerConexao

app = Flask(__name__)

# Rotas para Barbeiros
@app.route('/barbeiros', methods=['GET'])
def get_barbeiros():
    conexao = fazerConexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM barbeiros")
    lista_de_barbeiros = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(lista_de_barbeiros)

# Rota para buscar um único barbeiro
@app.route('/barbeiros/<int:id>', methods=['GET'])
def get_barbeiro(id):
    conexao = fazerConexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM barbeiros WHERE id = %s", (id,))
    barbeiro_encontrado = cursor.fetchone()  
    cursor.close()
    conexao.close()
    
    if barbeiro_encontrado:
        return jsonify(barbeiro_encontrado)  
    else:
        return jsonify({'erro': 'Barbeiro não encontrado'}), 404  

@app.route('/barbeiros', methods=['POST'])
def create_barbeiro():
    data = request.json
    conexao = fazerConexao()
    cursor = conexao.cursor()
    consulta = "INSERT INTO barbeiros (nome, cpf, telefone) VALUES (%s, %s, %s)"
    cursor.execute(consulta, (data['nome'], data['cpf'], data['telefone']))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'message': 'Barbeiro criado com sucesso!'}), 201

@app.route('/barbeiros/<int:id>', methods=['PUT'])
def update_barbeiro(id):
    data = request.json
    conexao = fazerConexao()
    cursor = conexao.cursor()
    consulta = "UPDATE barbeiros SET nome = %s, cpf = %s, telefone = %s WHERE id = %s"
    cursor.execute(consulta, (data['nome'], data['cpf'], data['telefone'], id))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'message': 'Barbeiro atualizado com sucesso!'})

@app.route('/barbeiros/<int:id>', methods=['DELETE'])
def delete_barbeiro(id):
    conexao = fazerConexao()
    cursor = conexao.cursor()
    consulta = "DELETE FROM barbeiros WHERE id = %s"
    cursor.execute(consulta, (id))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'message': 'Barbeiro deletado com sucesso!'})

# Rotas para Serviços
@app.route('/servicos', methods=['GET'])
def get_servicos():
    conexao = fazerConexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM servicos")
    servicos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(servicos)



# Rota para buscar um único serviço
@app.route('/servicos/<int:id>', methods=['GET'])
def get_servico(id):
    conexao = fazerConexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM servicos WHERE id = %s", (id,))
    servico_encontrado = cursor.fetchone()  
    cursor.close()
    conexao.close()
    
    if servico_encontrado:
        return jsonify(servico_encontrado)  
    else:
        return jsonify({'erro': 'Serviço não encontrado'}), 404  
    

@app.route('/servicos', methods=['POST'])
def create_servico():
    data = request.json
    conexao = fazerConexao()
    cursor = conexao.cursor()
    consulta = "INSERT INTO servicos (nome, descricao, valor, percentual_barbeiro) VALUES (%s, %s, %s, %s)"
    cursor.execute(consulta, (data['nome'], data['descricao'], data['valor'], data['percentual_barbeiro']))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'message': 'Serviço criado com sucesso!'}), 201



@app.route('/servicos/<int:id>', methods=['PUT'])
def update_servico(id):
    data = request.json
    conexao = fazerConexao()
    cursor = conexao.cursor()
    consulta = """
    UPDATE servicos 
    SET nome = %s, descricao = %s, valor = %s, percentual_barbeiro = %s 
    WHERE id = %s
    """
    cursor.execute(consulta, (data['nome'], data['descricao'], data['valor'], data['percentual_barbeiro'], id))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'message': 'Serviço atualizado com sucesso!'})

@app.route('/servicos/<int:id>', methods=['DELETE'])
def delete_servico(id):
    conexao = fazerConexao()
    cursor = conexao.cursor()
    consulta = "DELETE FROM servicos WHERE id = %s"
    cursor.execute(consulta, (id))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'message': 'Serviço deletado com sucesso!'})



# Rotas para Atendimentos
@app.route('/atendimentos', methods=['GET'])
def get_atendimentos():
    conexao = fazerConexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id, a.data_servico, b.nome AS barbeiro, s.nome AS servico
        FROM atendimentos a
        JOIN barbeiros b ON a.id_barbeiro = b.id
        JOIN servicos s ON a.id_servico = s.id
    """)
    atendimentos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(atendimentos)


@app.route('/atendimentos/<int:id>', methods=['GET'])
def get_atendimento(id):
    conexao = fazerConexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id, a.data_servico, b.nome AS barbeiro, s.nome AS servico
        FROM atendimentos a
        JOIN barbeiros b ON a.id_barbeiro = b.id
        JOIN servicos s ON a.id_servico = s.id
        WHERE a.id = %s
    """, (id,))
    
    atendimento = cursor.fetchone()  
    cursor.close()
    conexao.close()
    
    if atendimento:
        return jsonify(atendimento)
    else:
        return jsonify({'message': 'Atendimento não encontrado'}), 404



@app.route('/atendimentos', methods=['POST'])
def create_atendimento():
    data = request.json
    conexao = fazerConexao()
    cursor = conexao.cursor()
    consulta = "INSERT INTO atendimentos (id_barbeiro, id_servico, data_servico) VALUES (%s, %s, %s)"
    cursor.execute(consulta, (data['id_barbeiro'], data['id_servico'], data['data_servico']))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'message': 'Atendimento registrado com sucesso!'}), 201





@app.route('/relatorio/faturamento-mensal', methods=['GET'])
def relatorio_faturamento_mensal():
    mes = request.args.get('mes', type=int)
    ano = request.args.get('ano', type=int)

    if not mes or not ano:
        return jsonify({'error': 'Informe os parâmetros "mes" e "ano" para o relatório.'}), 400

    conexao = fazerConexao()
    cursor = conexao.cursor(dictionary=True)

    # Consulta para calcular os valores
    consulta = """
        SELECT 
            b.id AS id_barbeiro,
            b.nome AS Nome_Barbeiro,
            COUNT(a.id) AS quantidade_servicos,
            SUM(s.valor) AS total_servicos,
            SUM(s.valor * s.percentual / 100) AS valor_a_receber
        FROM 
            atendimentos a
        JOIN barbeiros b ON a.id_barbeiro = b.id
        JOIN servicos s ON a.id_servico = s.id
        WHERE 
            MONTH(a.data_servico) = %s AND YEAR(a.data_servico) = %s
        GROUP BY 
            b.id
    """
    cursor.execute(consulta, (mes, ano))
    barbeiros = cursor.fetchall()

    # Calcula o faturamento total da barbearia
    faturamento_total = sum(b['total_servicos'] for b in barbeiros)

    cursor.close()
    conexao.close()

    return jsonify({
        'mes': mes,
        'ano': ano,
        'faturamento_total': faturamento_total,
        'barbeiros': barbeiros
    })


if __name__ == '__main__':
    app.run(debug=True)






