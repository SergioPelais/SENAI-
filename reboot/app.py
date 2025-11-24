from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session, flash
from flask_bcrypt import Bcrypt
from datetime import timedelta, datetime
from utils.logging_config import log_auditoria
from utils.security import login_required, registrar_tentativa, verificar_bloqueio

from dotenv import load_dotenv
import resources.database_connection as database_connection

import json,ast
from email.message import EmailMessage
import os
import smtplib
import random
from collections import Counter
import secrets
import hashlib

# configuração por variáveis
def gerar_token():
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return token, token_hash
# tempo de espera da ação do aluno
hora_limit = 0 # 0 - 23
min_limit = 20 # 0 - 59

qunat_rep = 3 # quantidade de vezes que um aluno pode solicitar um pedido no mes

#carrega a função para consulta do banco de dados 
conectBD = database_connection.consultaBD

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

        resultado = "Responsável notificado com sucesso!"
    except Exception as e:
        resultado = f"Erro ao enviar e-mail"
        print({str(e)})

    return resultado

# configurando flask
app = Flask(__name__)
app.secret_key = "uma_chave_secreta_qualquer_tipo_1234567890_ou_sls_vc_q_decide_mas_acho_bom_tirar_a_roupa_do_varal_antes_da_chuva_chegar_slk"
app.permanent_session_lifetime = timedelta(minutes=480)#480
bcrypt = Bcrypt(app)

# ===== ROTAS DE AUTENTICAÇÃO =====
@app.route("/", methods=["GET", "POST"])
def index():
    # Lembrar usuário via cookie
    if "usuario" in session:
        return redirect(url_for("auth"))

    usuario_cookie = request.cookies.get("remember_user")
    if usuario_cookie:
        session['usuario'] = conectBD(f'SELECT id, nif, senha, nome, autoridade FROM funcionarios WHERE ativo=1 AND id = {usuario_cookie}',1)
        log_auditoria(session['usuario'][3], "login_cookie")
        return redirect(url_for("auth"))

    if request.method == "POST":
        nif = request.form['nif']
        senha = request.form['senha']
        lembrar = request.form.get("lembrar")

        values  = [nif,senha]
        user = conectBD('SELECT id, nif, senha, nome, autoridade FROM funcionarios WHERE ativo=1 AND nif=%s AND senha=%s;',1,values)

        if verificar_bloqueio(nif):
            flash(["Você está bloqueado! Tente novamente em 1 minuto.",'login'])
            return redirect(url_for('index'))
        
        if user:
            session.permanent = True
            session['usuario'] = user
            log_auditoria(user[3], "login_sucesso")

            resp = make_response(redirect(url_for("auth")))
            if lembrar:
                resp.set_cookie("remember_user",f"{session['usuario'][0]}", max_age=60*60*24*7)

            flash([f"Bem vindo! {user[3]}",'hello'])
            return resp

        if registrar_tentativa(nif):
            flash(["Excesso de tentativas! Bloqueado por 1 minuto.",'login'])
            return redirect(url_for('index'))

        flash(["Usuário ou senha incorretos.",'login'])
        return redirect(url_for('index'))

    return render_template("index.html")

@app.route("/logout")
@login_required
def logout():
    usuario = session['usuario']
    log_auditoria(usuario[3], "logout")
    session.clear()
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie("remember_user")
    flash(["Você saiu.",'login'])
    return resp

@app.route('/auth',methods=["GET", "POST"])
@login_required
def auth ():
    user = session['usuario']
    if user[4] == 2:
        return redirect(url_for('registros'))
    if request.method == "POST":
        cursoID = request.form.get('curso')
        estado = request.form.get('estado')
        caso = request.form.get('caso')
        alunoID = request.form.get('id-aluno')
        atividade = request.form.get('atividade')
        dia = request.form.get('data')
        hora = request.form.get('horario')
        motivo = request.form.get('motivo')
        motivo = motivo if motivo else 'não tem'
        obs = request.form.get('obs')
        userID = user[0] #docente
        
        try:
            alunoID = int(alunoID)
        except (ValueError, TypeError):
            listCursos = conectBD('SELECT id,nome FROM cursos WHERE ativo = 1;', 2)
            alunos = conectBD('SELECT id,nome,data_nascimento,email_resp,telefone_resp FROM alunos WHERE ativo=1;', 2)

            flash(["Aluno não encontrado", 'aluno'])
            
            return redirect(url_for('auth'))

        alunoExiste = conectBD('SELECT id,nome FROM alunos WHERE id = %s AND ativo = 1;', 1, (alunoID,))
        if not alunoExiste:
            listCursos = conectBD('SELECT id,nome FROM cursos WHERE ativo = 1;', 2)
            alunos = conectBD('SELECT id,nome,data_nascimento,email_resp,telefone_resp FROM alunos WHERE ativo=1;', 2)
            return redirect(url_for('auth'))

        # verificando se é preciso alertar o responsavel
        emailResp = request.form.get('emailResp')
        solicitarCod = request.form.get('receber_codigo')
        docente = "SENAI bot."
        msgEmail = ''
        numero = 0

        if estado == 'true' and caso=='Saída':
            if solicitarCod == 'sim':
                numero = random.randint(1000000, 9999999)
                token = gerar_token()
                msgEmail = f'Prezado(a) responsável, O(a) aluno(a) {alunoExiste[1]} solicitou saída antecipada da escola na data {dia} às {hora}, fora do horário padrão. Por se tratar de estudante menor de idade, solicitamos que confirme a autorização acessando o link: http://192.168.1.227:5000/autorizar-pelo-responsavel?token={token[1]} Sua resposta é necessária para que possamos liberar ou negar a saída. Atenciosamente, Escola SENAI "Luíz Massa"'
            else:
                numero = 2
                msgEmail = f'Prezado(a) responsável, O(A) aluno(a) {alunoExiste[1]} realizou uma solicitação de saída antecipada na data {dia} às {hora}. Consta em nosso sistema que a autorização foi confirmada diretamente pelo responsável, sem a necessidade de código de validação. Caso esta confirmação não tenha sido feita por você, por favor entre em contato com a coordenação imediatamente. Atenciosamente, Escola SENAI "Luíz Massa"'
        else:
            if caso == 'Saída':
                msgEmail = f'Prezado(a) responsável, Informamos que o(a) aluno(a) {alunoExiste[1]} solicitou saída antecipada da escola na data {dia} às {hora}, fora do horário regular. Solicitamos que confirme esta informação e esteja ciente da responsabilidade em relação à saída do(a) estudante. Atenciosamente, Escola SENAI "Luíz Massa"'
            else:
                msgEmail = f'Prezado(a) responsável, Informamos que o(a) aluno(a) {alunoExiste[1]} entrou na escola em horário diferente do início regular das aulas, no dia {dia}. O atraso foi registrado às {hora}. Pedimos atenção especial quanto aos horários escolares para garantir o bom andamento do aprendizado. Atenciosamente, Escola SENAI "Luíz Massa"'
        status = callEmail(emailResp,docente,f"Solicitação de {'Saída'if caso == 'Saída' else 'Entrada'}",msgEmail)
        
        if status != 'Responsável notificado com sucesso!' and len(f'{numero}') == 7:
            flash(["A autorização falhou: o responsável não recebeu a notificação. Contate-o externamente e refaça o processo sem marcar - Solicitar código de validação -",'email-error'])
            return redirect(url_for('auth'))
        else:
            flash([status,'email'])

        #salvando autorizacao no banco de dados e puxando o id criado
        id_auth = conectBD('INSERT INTO entrada_saida (caso, id_aluno, atividade, id_curso, data_ocorrencia, horario, motivo, obs, id_docente) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);',3,(caso,alunoID,atividade,cursoID,dia,hora,motivo,obs,userID))
        
        #tratamento de comunicacao do estado da autorizacao
        id_status = conectBD(f'INSERT INTO status_auth (id_auth) VALUES ({id_auth});',3)
        tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if status == 'Responsável notificado com sucesso!':
            conectBD(f'UPDATE status_auth SET at_alert_resp = "{tempo}" WHERE id={id_status};')
        if numero != 0:
            if len(f'{numero}')==7:
                conectBD(f'UPDATE status_auth SET cod = {numero}, token = "{token[1]}" WHERE id={id_status};')
            else:
                conectBD(f'UPDATE status_auth SET cod = {numero} WHERE id={id_status};')

        if user[4]==3:
            conectBD(f'UPDATE status_auth SET aprovado={user[0]}, at_aprovado = "{tempo}", at_docente = "{tempo}" WHERE id={id_status}')
        else:
            conectBD(f'UPDATE status_auth SET at_docente = "{tempo}" WHERE id={id_status};')

        #atualizando informações do curso que recebeu a autorizacao
        upCurso = conectBD(f'SELECT notification, cenarios FROM cursos WHERE id = {cursoID};',1)
        newCenario = ast.literal_eval(upCurso[1]) #[em espera, concluido, pendente, vulneravel]

        if estado == 'true':
            newCenario[2] += 1
        else:
            newCenario[0] += 1

        conectBD(f'UPDATE cursos SET cenarios = "{newCenario}", notification = {upCurso[0]+1} WHERE id = {cursoID};')
        #if len(f'{numero}') == 7 and status == 'Responsável notificado com sucesso!':
        #    flash([id_auth,'modal'])
        #    return redirect(url_for('registros',id=cursoID))
        return redirect(url_for('auth'))
    listCursos = conectBD('SELECT id,nome FROM cursos WHERE ativo = 1;',2)
    alunos = conectBD('SELECT id,nome,data_nascimento,email_resp,telefone_resp FROM alunos WHERE ativo=1;',2)
    menu = request.args.get('menu')
    return render_template('autorizacao.html',bd=json.dumps(alunos,default=str),listaCursos = listCursos, user=user,menu=menu)

@app.route('/cursos',methods=["GET","POST"])
@login_required
def cursos ():
    user = session['usuario']
    if user[4] == 2:
        return redirect(url_for('registros'))
    if request.method == "POST":
        curso = request.form.get('nome')

        conectBD(f'INSERT INTO cursos (nome) VALUES ("{curso}");')
        return redirect(url_for('cursos'))
        
    data = conectBD('SELECT id,nome,notification,cenarios FROM cursos WHERE ativo = 1;',2)
    listCursos = [list(i) for i in data]
    for i,item in enumerate(listCursos):
        listCursos[i][3] = ast.literal_eval(item[3])

        idAuth = conectBD(f'SELECT id FROM entrada_saida WHERE id_curso={listCursos[i][0]};',2)
        idAuth = list(map(lambda x: x[0],idAuth))
        if len(idAuth):
            idAuth = ",".join(map(str, idAuth))
            quant_1 = conectBD(f'SELECT COUNT(*) FROM status_auth WHERE cenario = 1 AND id_auth IN ({idAuth});',1)[0]
            quant_2 = conectBD(f'SELECT COUNT(*) FROM status_auth WHERE cenario = 2 AND id_auth IN ({idAuth});',1)[0]
            quant_3 = conectBD(f'SELECT COUNT(*) FROM status_auth WHERE cenario = 3 AND id_auth IN ({idAuth});',1)[0]
            vetor = [quant_1,quant_2,quant_3]

            conectBD(f'UPDATE cursos SET cenarios="{vetor}" WHERE id = {listCursos[i][0]};')

    return render_template('cursos.html', lista = listCursos, lista2 = json.dumps(listCursos,default=str), user=user)

@app.route('/deletando-curso/<int:id>',methods=["GET"])
@login_required
def deleteCurso (id):
    conectBD(f'UPDATE cursos SET ativo = 0 WHERE id = {id} AND ativo = 1;')
    conectBD(f'UPDATE entrada_saida SET ativo = 0 WHERE id_curso = {id} AND ativo = 1;')
    id_auth = [e[0] for e in conectBD(f'SELECT id FROM entrada_saida WHERE id_curso = {id} AND ativo = 1;',2)]
    if len(id_auth):
        conectBD(f'UPDATE status_auth SET ativo = 0 WHERE id_auth IN {tuple(id_auth)} AND ativo = 1;')

    return redirect(url_for('cursos'))

@app.route('/alunos/<int:id>',methods=["GET","POST"])
@app.route('/alunos',methods=["GET","POST"])
@login_required
def alunos (id=0):
    user = session['usuario']
    if user[4] == 2:
        return redirect(url_for('registros'))
    elif user[4] == 1: return redirect(url_for('auth'))
    aluno = ''
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

@app.route('/deletando-aluno/<int:id>',methods=["GET"])
def deleteAluno (id):
    conectBD(f'UPDATE alunos SET ativo = 0 WHERE id = {id};')
    return redirect(url_for('alunos'))

@app.route('/imagem/<int:id>')
def exibir_imagem(id):
    resultado = conectBD('SELECT tipo_img, dados_img FROM alunos WHERE id = %s',1,(id,))
    if resultado:
        if resultado[0]==None or resultado[1]==None:
            resultado= ('image/svg+xml', b'<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#5985E1"><path d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm246-164q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q53 0 100-15.5t86-44.5q-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160Zm0-360q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Zm0-60Zm0 360Z"/></svg>')

        tipo, dados = resultado
        response = make_response(dados)
        response.headers.set('Content-Type', tipo)
        
        return response
    else:
        return '../static/img/edit.svg'
    
@app.route('/registros/<int:id>', methods=["GET","POST"])
@app.route('/registros')
@login_required
def registros (id=0):
    global qunat_rep
    user = session['usuario']
    curso = conectBD(f'SELECT id,nome FROM cursos WHERE id = {id};',1)
    if request.method == "POST":
        nome = request.form['nowName']
        conectBD(f'UPDATE cursos SET nome = "{nome}" WHERE id = {id};')
        return redirect(url_for('registros',id=id))

    return render_template("registros.html",user=user,curso=curso)

@app.route("/get-items/<int:id>", methods=["GET"])
@app.route("/get-items", methods=["GET"])
@login_required
def get_items(id = 0):
    global hora_limit, min_limit
    user = session['usuario']

    mesAno = ast.literal_eval(request.args.get('dt'))

    if id != 0:
        conectBD(f'UPDATE cursos SET notification = 0  WHERE id = {id};')
        data = conectBD(f'SELECT id,caso,id_aluno,atividade,data_ocorrencia,horario,motivo,obs,id_docente,id_curso FROM entrada_saida WHERE id_curso = {id} AND ativo = 1 AND MONTH(created_at) = {mesAno[0]} AND YEAR(created_at) = {mesAno[1]}; ',2)
    else: 
        data = conectBD(f'SELECT id,caso,id_aluno,atividade,data_ocorrencia,horario,motivo,obs,id_docente,id_curso FROM entrada_saida WHERE ativo = 1 AND MONTH(created_at) = {mesAno[0]} AND YEAR(created_at) = {mesAno[1]};',2)
    auth_alunos = [list(i) for i in data]
    
    for i,item in enumerate(auth_alunos):
        auth_alunos[i][2] = [item[2],conectBD(f"SELECT nome FROM alunos WHERE id={item[2]};",1)[0]]
        auth_alunos[i][8] = conectBD(f"SELECT id,nome, autoridade FROM funcionarios WHERE id={item[8]};",1)
        auth_alunos[i][9] = conectBD(f"SELECT nome FROM cursos WHERE id={item[9]};",1)[0]
	
    ids = [item[0] for item in auth_alunos]
    ids = ",".join(map(str, ids))
    
    data2 = conectBD(f'SELECT id, id_auth, cenario, visto, aprovado, cod, at_visto, at_aprovado,at_alert_resp,at_aprovado_resp,at_docente FROM status_auth WHERE ativo=1 AND id_auth IN ({ids})',2) if len(ids) != 0 else []
    data_status = [list(i) for i in data2]

    if user[4] == 2:
        data_status = [e for e in data_status if len(f'{e[5]}') == 1]
        ids2 = [item[1] for item in data_status]
        auth_alunos = [e for e in auth_alunos if e[0] in ids2]

    for i,item in enumerate(data_status):
        if item[3]:
            data_status[i][3] = conectBD(f"SELECT nome,autoridade FROM funcionarios WHERE id={item[3]};",1)
        else:
            data_status[i][3] = False
        if item[4]:
            data_status[i][4] = conectBD(f"SELECT id,nome FROM funcionarios WHERE id={item[4]};",1)
        else:
            data_status[i][4] = False
        
        dt = conectBD(f"SELECT data_ocorrencia,horario FROM entrada_saida WHERE id={data_status[i][1]};",1)
        dt = datetime.strptime(f'{dt[0]} {dt[1]}', '%Y-%m-%d %H:%M:%S')
        tempo = datetime.now()

        if data_status[i][2] == 1:
            cod=1
            if dt.year >= tempo.year:
                if dt.month >= tempo.month:
                    if dt.day >= tempo.day:
                        timeH = dt.hour + hora_limit if dt.hour + hora_limit <= 23 else hora_limit + tempo.hour if hora_limit + tempo.hour <= 23 else hora_limit
                        timeM = dt.minute + min_limit if dt.minute + min_limit <= 59 else min_limit + tempo.minute if min_limit + tempo.minute <= 59 else min_limit
                        if timeH >= tempo.hour:
                            if timeM + min_limit >= tempo.minute:
                                cod=0
            if cod==1:conectBD(f'UPDATE status_auth SET cenario = 3 WHERE id = {data_status[i][0]};')
            
    json_data2 = json.dumps(data_status, default=str)
    json_data = json.dumps(auth_alunos, default=str)
    return jsonify(json_data,json_data2)

"""
@app.route('/autorizar-pelo-responsavel/<int:id>', methods=["GET","POST"])
def autorizarPeloResponsavel(id=0):
    id_status = int(request.form['id'])
    codigo = int(request.form['cod'])
    id_auth = request.form['auth']
    cod = conectBD(f'SELECT cod FROM status_auth WHERE id = {id_status};',1)[0]
    if cod==codigo:
        tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conectBD(f'UPDATE status_auth SET cod = 1, at_aprovado_resp = "{tempo}" WHERE id = {id_status};')
    else:
        flash(['Código incorreto!','vulneravel'])
        flash([id_auth,'modal'])

    if id != 0:
        return redirect(url_for('registros',id=id))
    return redirect(url_for('registros'))
"""

@app.route('/autorizar-pelo-responsavel', methods=["GET","POST"])
def autorizarPeloResponsavel():
    token = request.args.get('token')
    if request.method == "POST":
        token = request.form['token']

        cod_select = int(request.form['cod'])
        tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conectBD(f'UPDATE status_auth SET cod = {cod_select}, at_aprovado_resp = "{tempo}" WHERE token = "{token}";')
    else:
        token = request.args.get('token')

    status = conectBD(f'SELECT cod,id_auth,cenario,id FROM status_auth WHERE token = "{token}" AND ativo=1;',1)

    if not status:
        return render_template('comunicado.html',status=None)
    
    status = list(status)
    aluno = conectBD(f"SELECT id_aluno,horario,data_ocorrencia FROM entrada_saida WHERE id={status[1]};",1)
    aluno = [conectBD(f"SELECT nome FROM alunos WHERE id={aluno[0]};",1)[0],aluno[1],aluno[2]]
    status[1]=aluno


    dt = conectBD(f"SELECT data_ocorrencia,horario FROM entrada_saida WHERE id={status[3]};",1)
    dt = datetime.strptime(f'{dt[0]} {dt[1]}', '%Y-%m-%d %H:%M:%S')
    tempo = datetime.now()
    if status[2] == 1:
        cod=1
        if dt.year >= tempo.year:
            if dt.month >= tempo.month:
                if dt.day >= tempo.day:
                    timeH = dt.hour + hora_limit if dt.hour + hora_limit <= 23 else hora_limit + tempo.hour if hora_limit + tempo.hour <= 23 else hora_limit
                    timeM = dt.minute + min_limit if dt.minute + min_limit <= 59 else min_limit + tempo.minute if min_limit + tempo.minute <= 59 else min_limit
                    if timeH >= tempo.hour:
                        if timeM + min_limit >= tempo.minute:
                            cod=0
        if cod==1:conectBD(f'UPDATE status_auth SET cenario = 3 WHERE id = {status[3]};')


    return render_template('comunicado.html',status=status,token=token)

@app.route('/visto/<int:id>/<int:id_status>', methods=["GET","POST"])
@login_required
def visto(id=0,id_status=0):
    user = session['usuario']
    tempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    match user[4]:
        case 3:
            conectBD(f'UPDATE status_auth SET aprovado={user[0]}, at_aprovado="{tempo}" WHERE id = {id_status};')
        case _:
            conectBD(f'UPDATE status_auth SET visto={user[0]}, at_visto="{tempo}", cenario=2 WHERE id = {id_status};')
    
    if id != 0:
        return jsonify({'redirect_url': url_for('registros',id=id)})
    return jsonify({'redirect_url': url_for('registros')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 