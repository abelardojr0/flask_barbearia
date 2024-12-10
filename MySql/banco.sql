CREATE DATABASE barbearia;

USE barbearia;

-- Tabela Barbeiro
CREATE TABLE barbeiros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    telefone VARCHAR(15) NOT NULL
);

-- Tabela Serviços
CREATE TABLE servicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    valor DECIMAL(10, 2) NOT NULL,
    percentual FLOAT NOT NULL
);

-- Tabela Atendimentos
CREATE TABLE atendimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_servico DATETIME NOT NULL,
    id_barbeiro INT NOT NULL,
    id_servico INT NOT NULL,
    FOREIGN KEY (id_barbeiro) REFERENCES barbeiros(id),
    FOREIGN KEY (id_servico) REFERENCES servicos(id)
);




INSERT INTO barbeiros (nome, cpf, telefone) VALUES 
('João Silva', '12345678901', '999999999'),
('Maria Oliveira', '98765432102', '988888888'),
('Carlos Santos', '11223344556', '977777777'),
('Ana Costa', '55667788999', '966666666'),
('Pedro Lima', '12312312312', '955555555'),
('Fernanda Alves', '98798798798', '944444444');



INSERT INTO servicos (nome, descricao, valor, percentual) VALUES 
('Corte de cabelo', 'Corte masculino ou feminino', 50.00, 50),
('Barba', 'Aparar ou fazer a barba', 30.00, 0.40),
('Pintura de cabelo', 'Pintura para cobrir fios brancos', 80.00, 60),
('Alisamento', 'Alisamento de cabelo', 120.00, 55),
('Luzes', 'Luzes no cabelo', 100.00, 20);



INSERT INTO atendimentos (id_barbeiro, id_servico, data_servico) VALUES 
(1, 1, '2024-11-20 14:00:00'),  -- João fez um corte de cabelo
(2, 3, '2024-11-22 10:30:00');  -- Maria fez pintura de cabelo


SELECT * FROM barbeiros;

SELECT * FROM servicos;

SELECT * FROM atendimentos;
