from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from dotenv import load_dotenv
import resources.database_connection as database_connection

import json,ast

from email.message import EmailMessage
import os
import smtplib
import random
from datetime import datetime

#carrega a função para consulta do banco de dados 
conectBD = database_connection.consultaBD
#Servidor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Senai@791'

# Carrega variáveis de ambiente
load_dotenv()
# Configurando comunicação via email
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
def callEmail(emailDestina='', remetente='', assunto='', mensagem=''):
    try:    
        email = EmailMessage()
        email["Subject"] = assunto
        email["From"] = EMAIL_REMETENTE
        email["To"] = emailDestina
        corpo = f"Mensagem de: {remetente}\n\n{mensagem}"
        email.set_content(corpo)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
            smtp.send_message(email)

        resultado = "E-mail enviado com sucesso!"
    except Exception as e:
        resultado = f"Erro ao enviar e-mail: {str(e)}"
    print(resultado)
    return resultado

# nova função para tratamento de notificações, mas ainda está em teste
mensagem = ['',0]
def msg(cod=1):
    if mensagem[0]!='':
        if mensagem[1] >= cod:
            mensagem[0]=''
            mensagem[1]=0
        else:
            mensagem[1]+=1
    return mensagem[0]

# conta do usuario ativo
user =  (4, 2345678, '1234', 'fabio', 3)

@app.route('/',methods=["GET","POST"])
def inicio ():
    global user,mensagem
    user = None

    if request.method == "POST":
        nif = request.form.get('nif')
        senha = request.form.get('senha')

        values  = [nif,senha]
        user = conectBD('SELECT id, nif, senha, nome, autoridade FROM funcionarios WHERE ativo=1 AND nif=%s AND senha=%s;',1,values)

        if user:
            if user[4] != 2:
                mensagem[1]=0
                mensagem[0]=f"bem vindo! {user[3]}"
            if user[4] == 2:
                return redirect(url_for('registroGeral'))
            return redirect(url_for('auth'))
        
        mensagem[0]="Login ou senha, incorretos!"
        mensagem[1]=0
        return redirect(url_for('inicio'))
    msg()
    return render_template('index.html', alert=mensagem[0])

@app.route('/auth',methods=["GET", "POST"])
def auth ():
    global user, mensagem
    if user:
        if request.method == "POST":
            alunoID = request.form.get('id-aluno')
            caso = request.form.get('caso')
            atividade = request.form.get('atividade')
            dia = request.form.get('data')
            hora = request.form.get('horario')
            motivo = request.form.get('motivo')
            motivo = motivo if motivo else 'não há um motivo'
            obs = request.form.get('obs')
            userID = user[0] #docente
            cursoID = request.form.get('curso')

            try:
                alunoID = int(alunoID)
            except (ValueError, TypeError):
                listCursos = conectBD('SELECT id,nome FROM cursos WHERE ativo = 1;', 2)
                alunos = conectBD('SELECT id,nome,data_nascimento,email_resp,telefone_resp FROM alunos WHERE ativo=1;', 2)

                mensagem[0]='Aluno não encontrado'
                mensagem[1]=0
                return redirect(url_for('auth'))

            alunoExiste = conectBD('SELECT id FROM alunos WHERE id = %s AND ativo = 1;', 1, (alunoID,))
            if not alunoExiste:
                listCursos = conectBD('SELECT id,nome FROM cursos WHERE ativo = 1;', 2)
                alunos = conectBD('SELECT id,nome,data_nascimento,email_resp,telefone_resp FROM alunos WHERE ativo=1;', 2)
                return redirect(url_for('auth'))


            #salvando autorizacao no banco de dados
            id_auth = conectBD('INSERT INTO entrada_saida (caso, id_aluno, atividade, id_curso, data_ocorrencia, horario, motivo, obs, id_docente) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);',3,(caso,alunoID,atividade,cursoID,dia,hora,motivo,obs,userID))

            #tratamento de comunicacao do estado da autorizacao
            id_status = conectBD(f'INSERT INTO status_auth (id_auth) VALUES ({id_auth});',3)
            if user[4]==3:
                tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                conectBD(f'UPDATE status_auth SET aprovado={user[0]}, at_aprovado = "{tempo}" WHERE id={id_status}')

            #atualizando informações do curso que recebeu a autorizacao
            notInt = conectBD(f'SELECT notification FROM cursos WHERE id = {cursoID};',1)
            cenarios = [0,0,0,0,0] #[em espera, confirmado, pendente, negado, vulneravel]
            for i in range(len(cenarios)):
                cenarios[i] = conectBD(f'SELECT COUNT(*) FROM status_auth WHERE cenario = {i+1};',1)[0]
            conectBD(f'UPDATE cursos SET notification = {notInt[0]+1}, cenarios = "{cenarios}"  WHERE id = {cursoID};')

            # verificando se é preciso alertar o responsavel
            estado = request.form.get('estado')
            emailResp = request.form.get('emailResp')
            solicitarCod = request.form.get('receber_codigo')
            docente = "SENAI bot."
            msgEmail = ''
            if estado == 'true':
                if caso=='Saída' and solicitarCod == 'sim':
                    numero = random.randint(1000000, 9999999)
                    msgEmail = f'solicitação do aluno com código [{numero}]'
                    conectBD(f'UPDATE status_auth SET cod = {numero}, cenario = 5 WHERE id = {id_status}')
                    #callEmail(emailResp,docente,f"Solicitação de {'Saída'if caso == 'Saída' else 'Entrada'}",msgEmail)
                    mensagem[0] = id_auth
                    mensagem[1] = 0
                    return redirect(url_for('registroGeral'))
                else:
                    msgEmail = 'solicitação do aluno sem código'
                    conectBD(f'UPDATE status_auth SET cod = 2 WHERE id = {id_status}')

                callEmail(emailResp,docente,f"Solicitação de {'Saída'if caso == 'Saída' else 'Entrada'}",msgEmail)

            return redirect(url_for('auth'))
        listCursos = conectBD('SELECT id,nome FROM cursos WHERE ativo = 1;',2)
        alunos = conectBD('SELECT id,nome,data_nascimento,email_resp,telefone_resp FROM alunos WHERE ativo=1;',2)
        msg()
        return render_template('autorizacao.html',bd=json.dumps(alunos,default=str),listaCursos = listCursos, hello=mensagem[0], user=user)
    return redirect(url_for('inicio'))

@app.route('/cursos',methods=["GET","POST"])
def cursos ():
    global user
    if user:
        if request.method == "POST":
            curso = request.form.get('nome')

            conectBD(f'INSERT INTO cursos (nome) VALUES ("{curso}");')
            return redirect(url_for('cursos'))
        
        data = conectBD('SELECT id,nome,notification,cenarios FROM cursos WHERE ativo = 1;',2)
        listCursos = [list(i) for i in data]
        for i,item in enumerate(listCursos):
            listCursos[i][3] = ast.literal_eval(item[3])

        return render_template('cursos.html', lista = listCursos, lista2 = json.dumps(listCursos,default=str), user=user)
    return redirect(url_for('inicio'))

@app.route('/registros/<int:id>',methods=["GET","POST"])
def registros (id):
    global user
    if user:
        if request.method == "POST":
            nome = request.form.get('nome')
            conectBD(f'UPDATE cursos SET nome = "{nome}" WHERE id = {id};')
            return redirect(url_for('registros',id=id))
        
        conectBD(f'UPDATE cursos SET notification = 0  WHERE id = {id};')

        curso = conectBD(f'SELECT nome,notification FROM cursos WHERE id = {id};',1)[0]
    
        data = conectBD(f'SELECT id,caso,id_aluno,atividade,data_ocorrencia,horario,motivo,obs,id_docente FROM entrada_saida WHERE id_curso = {id} AND ativo = 1;',2)
        auth_alunos = [list(i) for i in data]

        for i,item in enumerate(auth_alunos):
            auth_alunos[i][2] = [item[2],conectBD(f"SELECT nome FROM alunos WHERE id={item[2]};",1)[0]]
            auth_alunos[i][8] = conectBD(f"SELECT nome FROM funcionarios WHERE id={item[8]};",1)[0]
        
        data2 = conectBD(f'SELECT id, id_auth, cenario, visto, aprovado, cod, at_visto, at_aprovado FROM status_auth WHERE ativo=1 ',2)
        data_status = [list(i) for i in data2]
        for i,item in enumerate(data_status):
            if item[3]:
                data_status[i][3] = conectBD(f"SELECT nome FROM funcionarios WHERE id={item[3]};",1)[0]
            if item[4]:
                data_status[i][4] = conectBD(f"SELECT nome FROM funcionarios WHERE id={item[4]};",1)[0]

        return render_template('registros.html',curso=json.dumps([id,curso],default=str),lista=[id,curso],auth_alunos=json.dumps(auth_alunos,default=str),data_status=json.dumps(data_status,default=str), user=user)
    return redirect(url_for('inicio'))

@app.route('/deletando-curso/<int:id>',methods=["GET"])
def deleteCurso (id):
    global user
    if user:
        conectBD(f'UPDATE cursos SET ativo = 0 WHERE id = {id} AND ativo = 1;')
        conectBD(f'UPDATE entrada_saida SET ativo = 0 WHERE id_curso = {id} AND ativo = 1;')
        id_auth = [e[0] for e in conectBD(f'SELECT id FROM entrada_saida WHERE id_curso = {id} AND ativo = 1;',2)]
        if len(id_auth):
            conectBD(f'UPDATE status_auth SET ativo = 0 WHERE id_auth IN {tuple(id_auth)} AND ativo = 1;')

        return jsonify({'redirect_url': url_for('cursos')})
    return redirect(url_for('inicio'))

@app.route('/alunos/<int:id>',methods=["GET","POST"])
@app.route('/alunos',methods=["GET","POST"])
def alunos (id=0):
    global user
    aluno = ''
    if user:
        if request.method == "POST":
            nome = request.form.get('nome')
            nasc = request.form.get('data')
            cpf = request.form.get('cpf')
            email = request.form.get('email')
            tell = request.form.get('tell')
            
            imagem = request.files['img']
            if imagem:
                tipo = imagem.content_type
                dados = imagem.read()
            match id:
                case 0:
                    if imagem:
                        conectBD('INSERT INTO alunos (nome, data_nascimento, cpf, email_resp, telefone_resp, tipo_img, dados_img) VALUES (%s, %s, %s, %s, %s, %s, %s);',0,(nome,nasc,cpf,email,tell,tipo,dados))
                    else:
                        conectBD('INSERT INTO alunos (nome, data_nascimento, cpf, email_resp, telefone_resp) VALUES (%s, %s, %s, %s, %s);',0,(nome,nasc,cpf,email,tell))
                case _:
                    if imagem:
                        conectBD('UPDATE alunos SET nome = %s, data_nascimento = %s, cpf = %s, email_resp = %s, telefone_resp = %s, tipo_img = %s, dados_img = %s WHERE id = %s;',0,(nome,nasc,cpf,email,tell,tipo,dados,id))
                    else:
                        conectBD('UPDATE alunos SET nome = %s, data_nascimento = %s, cpf = %s, email_resp = %s, telefone_resp = %s WHERE id = %s;',0,(nome,nasc,cpf,email,tell,id))

            return redirect(url_for('alunos'))
        
        aluno = conectBD(f'SELECT nome, data_nascimento, cpf, email_resp, telefone_resp FROM alunos WHERE id={id};',1)
        lista_alunos = conectBD('SELECT id, nome FROM alunos WHERE ativo=1;',2)
        return render_template('alunos.html',listaAlunos=json.dumps(lista_alunos,default=str),edit=id,aluno=aluno)
    return redirect(url_for('inicio'))

@app.route('/deletando-aluno/<int:id>',methods=["GET"])
def deleteAluno (id):
    global user
    if user:
        conectBD(f'UPDATE alunos SET ativo = 0 WHERE id = {id};')
        return redirect(url_for('alunos'))
    return redirect(url_for('inicio'))

#printar a imagem do aluno
@app.route('/imagem/<int:id>')
def exibir_imagem(id):
    resultado = conectBD('SELECT tipo_img, dados_img FROM alunos WHERE id = %s',1,(id,))
    if resultado:
        tipo, dados = resultado
        response = make_response(dados)
        response.headers.set('Content-Type', tipo)
        return response
    else:
        return 'Imagem não encontrada', 404
    
@app.route('/visto/<int:id>/<int:id_status>/<int:ativo>', methods=['POST'])
def visto(id,id_status,ativo):
    global user
    cenarios = [0,0,0,0,0] 
    for i in range(len(cenarios)):
        cenarios[i] = conectBD(f'SELECT COUNT(*) FROM status_auth WHERE cenario = {i+1};',1)[0]
        conectBD(f'UPDATE cursos SET cenarios = "{cenarios}"  WHERE id = {id};')
    tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if user[4] == 2:
        conectBD(f'UPDATE status_auth SET cenario = {ativo}, visto = {user[0]}, at_visto = "{tempo}" WHERE id = {id_status};')
    elif user[4] == 3:
        conectBD(f'UPDATE status_auth SET aprovado = {user[0]}, at_aprovado = "{tempo}" WHERE id = {id_status};')

    if id != 0:
        return jsonify({'redirect_url': url_for('registros',id=id)})
    return jsonify({'redirect_url': url_for('registroGeral')})

@app.route('/registros',methods=["GET","POST"])
def registroGeral ():
    global user, mensagem
    if user:
        data = conectBD(f'SELECT id,caso,id_aluno,atividade,data_ocorrencia,horario,motivo,obs,id_docente, id_curso FROM entrada_saida WHERE ativo = 1;',2)
        auth_alunos = [list(i) for i in data]
        for i,item in enumerate(auth_alunos):
            auth_alunos[i][2] = [item[2],conectBD(f"SELECT nome FROM alunos WHERE id={item[2]};",1)[0]]
            auth_alunos[i][8] = conectBD(f"SELECT nome FROM funcionarios WHERE id={item[8]};",1)[0]
            auth_alunos[i][9] = [item[9],conectBD(f"SELECT nome FROM cursos WHERE id={item[9]};",1)[0]]
        
        data2 = conectBD(f'SELECT id, id_auth, cenario, visto, aprovado, cod, at_visto, at_aprovado FROM status_auth WHERE ativo=1 ',2)
        data_status = [list(i) for i in data2]
        for i,item in enumerate(data_status):
            if item[3]:
                data_status[i][3] = conectBD(f"SELECT nome FROM funcionarios WHERE id={item[3]};",1)[0]
            if item[4]:
                data_status[i][4] = conectBD(f"SELECT nome FROM funcionarios WHERE id={item[4]};",1)[0]
        msg()
        return render_template('registrosAll.html',auth_alunos=json.dumps(auth_alunos,default=str),data_status=json.dumps(data_status,default=str), user=user, id_modal = mensagem[0])
    return redirect(url_for('inicio'))

@app.route('/limpar/<int:id>',methods=["GET","POST"])
def limpar (id):
    lista_ids = conectBD('SELECT id, id_auth FROM status_auth WHERE aprovado IS NOT NULL AND visto IS NOT NULL AND ativo = 1;',2)
    id_status = [e[0] for e in lista_ids]
    id_auht = [e[1] for e in lista_ids]
    if len(id_status) and len(id_auht):
        conectBD('UPDATE status_auth SET ativo = 0 WHERE id IN (%s);',0,id_status)
        conectBD('UPDATE entrada_saida SET ativo = 0 WHERE id IN (%s);',0,id_auht)
    return jsonify({'redirect_url': url_for('registros',id=id)})

@app.route('/limpar',methods=["GET","POST"])
def limpar2 ():
    lista_ids = conectBD('SELECT id, id_auth FROM status_auth WHERE aprovado IS NOT NULL AND visto IS NOT NULL AND ativo = 1;',2)
    id_status = [e[0] for e in lista_ids]
    id_auht = [e[1] for e in lista_ids]
    if len(id_status) and len(id_auht):
        conectBD('UPDATE status_auth SET ativo = 0 WHERE id IN (%s);',0,id_status)
        conectBD('UPDATE entrada_saida SET ativo = 0 WHERE id IN (%s);',0,id_auht)
    return jsonify({'redirect_url': url_for('registroGeral')})

@app.route('/verificacao',methods=["GET","POST"])
def verificacao ():
    if request.method == "POST":
        id = request.form.get('id')
        cod = request.form.get('cod')
        id_status = request.form.get('id_status')

        pass_cod = conectBD(f'SELECT cod FROM status_auth WHERE id = {id_status}',1)[0]

        if pass_cod == int(cod):
            conectBD(f'UPDATE status_auth SET cod = 1 WHERE id = {id_status}')
            conectBD(f'UPDATE status_auth SET cenario = 1 WHERE id = {id_status};')
    
        if id!='0':
            return redirect(url_for('registros',id=id))
    return redirect(url_for('registroGeral'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 