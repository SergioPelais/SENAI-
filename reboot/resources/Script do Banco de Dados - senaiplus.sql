DROP DATABASE if EXISTS SENAIplus;
CREATE DATABASE if NOT EXISTS SENAIplus;
USE SENAIplus;

DROP TABLE if EXISTS funcionarios;
CREATE TABLE if NOT EXISTS funcionarios (
	id INT(11) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(id),
	nome VARCHAR(255),
	nif INT(7),
	senha VARCHAR(255),
	autoridade INT (1) DEFAULT 0,
	ativo INT(11) NOT NULL DEFAULT 1
);

DROP TABLE if EXISTS EntradaSaída;
CREATE TABLE if NOT EXISTS EntradaSaída (
	id INT(11) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(id),
	caso VARCHAR(7) CHECK (caso IN ('Saída', 'Entrada')),
	nome VARCHAR(255),
	atividade VARCHAR(3) CHECK (atividade IN ('CAI', 'CT', 'FIC')),
	curso VARCHAR(255),
	data_ocorrencia DATE,
	horario TIME,
	motivo TEXT,
	obs TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	ativo INT(11) NOT NULL DEFAULT 1
);

DROP TABLE if EXISTS alunos;
CREATE TABLE if NOT EXISTS alunos (
	id INT(11) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(id),
	nome VARCHAR(255),
	data_nascimento DATE,
	cpf VARCHAR(11),
	email_resp VARCHAR(255),
	telefone_resp INT(18),
	ativo INT(11) NOT NULL DEFAULT 1
);