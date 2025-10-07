from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from dotenv import load_dotenv
import resources.database_connection as database_connection

import json

from email.message import EmailMessage
import os
import smtplib
import random

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
user = None

@app.route('/',methods=["GET","POST"])
def inicio ():
    global user,mensagem
    if request.method == "POST":
        nif = request.form.get('nif')
        senha = request.form.get('senha')

        values  = [nif,senha]
        user = conectBD('SELECT id, nif, senha, nome FROM funcionarios WHERE ativo=1 AND nif=%s AND senha=%s;',1,values)
        
        if user:
            mensagem[0]=f"bem vindo! {user[3]}"
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
            # salvando pedido de autorizacao no banco
            """
            alunoID = request.form.get('id-aluno')
            caso = request.form.get('caso')
            atividade = request.form.get('atividade')
            dia = request.form.get('data')
            hora = request.form.get('horario')
            motivo = request.form.get('motivo')
            motivo = motivo if motivo else 'não há um motivo'
            obs = request.form.get('obs')
            userID = user[0] #docente
            """
            cursoID = request.form.get('curso')

            #conectBD('INSERT INTO entrada_saida (caso, id_aluno, atividade, id_curso, data_ocorrencia, horario, motivo, obs, id_docente) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);',0,(caso,alunoID,atividade,cursoID,dia,hora,motivo,obs,userID))
            notInt = conectBD(f'SELECT notification FROM cursos WHERE id = {cursoID};',1)
            conectBD(f'UPDATE cursos SET notification = {notInt[0]+1}  WHERE id = {cursoID};')
            # verificando se é preciso alertar o responsavel
            """
            estado = request.form.get('estado')
            emailResp = request.form.get('emailResp')
            solicitarCod = request.form.get('receber_codigo')
            docente = "SENAI bot."
            msgEmail = ''
            if estado == 'true':
                if caso=='Saída' and solicitarCod == 'sim':
                    msgEmail = 'solicitação do aluno com código [XXXXXX]'
                else:
                    msgEmail = 'solicitação do aluno sem código'
                callEmail(emailResp,docente,f"Solicitação de {'Saída'if caso == 'Saída' else 'Entrada'}",msgEmail)
            """
        listCursos = conectBD('SELECT id,nome FROM cursos WHERE ativo = 1;',2)
        alunos = conectBD('SELECT * FROM alunos WHERE ativo=1;',2)
        msg()
        return render_template('autorizacao.html',bd=json.dumps(alunos,default=str),listaCursos = listCursos, hello=mensagem[0])
    return redirect(url_for('sair'))

@app.route('/cursos',methods=["GET","POST"])
def cursos ():
    global user
    if user:
        if request.method == "POST":
            curso = request.form.get('nome')

            conectBD(f'INSERT INTO cursos (nome) VALUES ("{curso}");')
            return redirect(url_for('cursos'))
        
        listCursos = conectBD('SELECT id,nome,notification FROM cursos WHERE ativo = 1;',2)

        return render_template('cursos.html', lista = listCursos, lista2 = json.dumps(listCursos,default=str))
    return redirect(url_for('sair'))

@app.route('/alunos',methods=["GET","POST"])
def alunos ():
    global user
    if user:
        if request.method == "POST":
            return
        return render_template('alunos.html')
    return redirect(url_for('sair'))

@app.route('/registros/<int:id>',methods=["GET","POST"])
def registros (id):
    global user
    if user:
        if request.method == "POST":
            nome = request.form.get('nome')
            conectBD(f'UPDATE cursos SET nome = "{nome}" WHERE id = {id};')
            return redirect(url_for('registros',id=id))
        conectBD(f'UPDATE cursos SET notification = 0  WHERE id = {id};')
        curso = conectBD(f'SELECT nome FROM cursos WHERE id = {id};',1)[0]
        auth_alunos = conectBD(f'SELECT id,caso,id_aluno,atividade,data_ocorrencia,horario,motivo,obs,id_docente,resolvido FROM entrada_saida WHERE id_curso = {id} AND ativo = 1;',2)

        return render_template('registros.html',curso=json.dumps([id,curso],default=str),lista=[id,curso],auth_alunos=json.dumps(auth_alunos,default=str))
    return redirect(url_for('sair'))

@app.route('/deletando-curso/<int:id>',methods=["GET"])
def deleteCurso (id):
    global user
    if user:
        conectBD(f'UPDATE cursos SET ativo = 0 WHERE id = {id};')
        return jsonify({'redirect_url': url_for('cursos')})
    return redirect(url_for('sair'))



#salvar imagem no banco
@app.route('/32',methods=["GET","POST"])
def inicio3 ():
    if request.method == "POST":
        imagem = request.files['img']
        if imagem:
            nome = imagem.filename
            tipo = imagem.content_type
            dados = imagem.read()
            conectBD('INSERT INTO imagens (nome, tipo, dados) VALUES (%s, %s, %s)',0,(nome,tipo,dados))
        return redirect(url_for('inicio'))
    return render_template('testes.html')

#printar a imagem
@app.route('/imagem/<int:id>')
def exibir_imagem(id):
    resultado = conectBD('SELECT tipo, dados FROM imagens WHERE id = %s',1,(id,))
    if resultado:
        tipo, dados = resultado
        print('testando código> ',tipo)
        response = make_response(dados)
        response.headers.set('Content-Type', tipo)
        return response
    else:
        return 'Imagem não encontrada', 404

@app.route('/sair')
def sair ():
    global user
    user = None
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)