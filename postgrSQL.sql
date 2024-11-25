-- Criar o banco de dados
CREATE DATABASE barbearia;

-- Tabela Barbeiros
CREATE TABLE barbeiros (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL, -- CPF com tamanho fixo
    telefone VARCHAR(15) NOT NULL
);

-- Tabela Serviços
CREATE TABLE servicos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT, -- Para texto mais longo
    valor NUMERIC(10, 2) NOT NULL, -- Para valores monetários
    percentual NUMERIC(5, 2) NOT NULL -- Percentual com mais precisão
);

-- Tabela Atendimentos
CREATE TABLE atendimentos (
    id SERIAL PRIMARY KEY,
    data_servico TIMESTAMP NOT NULL, -- Data e hora
    id_barbeiro INT NOT NULL,
    id_servico INT NOT NULL,
    FOREIGN KEY (id_barbeiro) REFERENCES barbeiros(id) ON DELETE CASCADE, -- Deleta atendimentos se o barbeiro for excluído
    FOREIGN KEY (id_servico) REFERENCES servicos(id) ON DELETE CASCADE -- Deleta atendimentos se o serviço for excluído
);

-- Inserir dados na tabela Barbeiros
INSERT INTO barbeiros (nome, cpf, telefone) VALUES 
('João Silva', '12345678901', '999999999'),
('Maria Oliveira', '98765432102', '988888888'),
('Carlos Santos', '11223344556', '977777777'),
('Ana Costa', '55667788999', '966666666'),
('Pedro Lima', '12312312312', '955555555'),
('Fernanda Alves', '98798798798', '944444444');

-- Inserir dados na tabela Serviços
INSERT INTO servicos (nome, descricao, valor, percentual) VALUES 
('Corte de cabelo', 'Corte masculino ou feminino', 50.00, 50.00),
('Barba', 'Aparar ou fazer a barba', 30.00, 40.00),
('Pintura de cabelo', 'Pintura para cobrir fios brancos', 80.00, 60.00),
('Alisamento', 'Alisamento de cabelo', 120.00, 55.00),
('Luzes', 'Luzes no cabelo', 100.00, 20.00);

-- Inserir dados na tabela Atendimentos
INSERT INTO atendimentos (id_barbeiro, id_servico, data_servico) VALUES 
(1, 1, '2024-11-20 14:00:00'), -- João fez um corte de cabelo
(2, 3, '2024-11-22 10:30:00'); -- Maria fez pintura de cabelo

-- Consultar dados
SELECT * FROM barbeiros;
SELECT * FROM servicos;
SELECT * FROM atendimentos;
