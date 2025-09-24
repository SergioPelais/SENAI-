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

DROP TABLE if EXISTS alunos;
CREATE TABLE if NOT EXISTS alunos (
	id INT(11) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(id),
	caso INT (1) DEFAULT 0,
	nome VARCHAR(255),
	telefone_resp INT(18),
	email_resp VARCHAR(255),
	curso VARCHAR(255),
	data_ocorrencia DATE,
	horario TIME, 
	ativo INT(11) NOT NULL DEFAULT 1
);
