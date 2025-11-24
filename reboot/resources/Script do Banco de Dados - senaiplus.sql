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
	autoridade INT (1) DEFAULT 1, -- 3_coordenador; 2_vigia; 1_professor
	cursos_fixados VARCHAR(255)DEFAULT '[]',
	ativo INT(11) NOT NULL DEFAULT 1
);

DROP TABLE if EXISTS entrada_saida;
CREATE TABLE if NOT EXISTS entrada_saida (
	id INT(11) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(id),
	caso VARCHAR(7) CHECK (caso IN ('Saída', 'Entrada')),
	id_aluno INT(11),
	atividade VARCHAR(3) CHECK (atividade IN ('CAI', 'CT', 'FIC')),
	id_curso INT(11),
	data_ocorrencia DATE,
	horario TIME,
	motivo TEXT,
	obs TEXT NULL,
	id_docente INT(11),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	ativo INT(11) NOT NULL DEFAULT 1
);

DROP TABLE if EXISTS status_auth;
CREATE TABLE if NOT EXISTS status_auth (
	id INT(11) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(id),
	id_auth INT(11), -- autorização
	cenario INT(1) DEFAULT 1, -- em andamento, pendente, concluido
	visto INT (11), -- id do guarita ou professor
	aprovado INT(11), -- id do coordenador(a)
	cod INT(7) DEFAULT 0, -- código de validacao
	at_alert_resp TIMESTAMP NULL, -- horário-notificado-responsável
	at_aprovado_resp TIMESTAMP NULL, -- horário-aprovado-responsável
	at_visto TIMESTAMP NULL, -- horário do visto
	at_aprovado TIMESTAMP NULL, -- horário da aprovação
	at_docente TIMESTAMP NULL, -- hórario aprovado pelo docente
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
   tipo_img TEXT,
   dados_img LONGBLOB,
	ativo INT(11) NOT NULL DEFAULT 1
);

DROP TABLE if EXISTS cursos;
CREATE TABLE if NOT EXISTS cursos (
	id INT(11) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(id),
	nome VARCHAR(255),
	notification INT(11)DEFAULT 0,
	cenarios VARCHAR(255)DEFAULT '[0,0,0]',
	ativo INT(11) NOT NULL DEFAULT 1
);

DROP TABLE if EXISTS notification;
CREATE TABLE if NOT EXISTS notification (
	id INT(11) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(id),
	nome VARCHAR(255),
	id_curso INT(11),
	auth VARCHAR(7) CHECK (caso IN ('Saída', 'Entrada')),
	acao VARCHAR(255),
	ativo INT(11) NOT NULL DEFAULT 1
);