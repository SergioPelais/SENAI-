from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import random
import resources.database_connection as database_connection

def conectBD(SQL,opcao=0,valor=''):
    data = ''
    connection = database_connection.open_connection()
    cursor = connection.cursor(buffered=True)
    if valor == '':
        cursor.execute(SQL)
    else:
        cursor.execute(SQL,valor)

    match opcao:
        case 0: connection.commit()
        case 1: data = cursor.fetchall()
        case 2: data = cursor.fetchone()
        
    cursor.close()
    connection.close()
    return data

#Servidor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Senai@791'

# Carrega variáveis de ambiente
load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")

#Variáveis vazias
numero = 0
msg2 = ''
msglogin = ''

msg = ["",0]
def msgError():
    global msg
    if msg[1] == 0:
        msg[1] = 1
    else:
        msg[0] = ""
        msg[1] = 0

@app.route('/')
def inicio ():
    global msg
    msgError()
    return render_template('index.html', msg=msg[0])

@app.route('/autenticar', methods=["GET", "POST"])
def autenticar():
    msg[1] = 0
    if request.method == 'POST':

        nif = request.form['nif']
        senha = request.form['senha']

        valor = [nif,senha]
        SQL = 'SELECT id, autoridade FROM funcionarios WHERE nif = %s AND senha = %s'
        resultado = conectBD(SQL,2,valor)

        if resultado and resultado[1] == 0:
            msg[0] = 'Login realizado com sucesso'
            return redirect(url_for('listagem'))
        elif resultado and resultado[1] == 1:
            msg[0] = 'Login realizado com sucesso'
            return redirect(url_for('formulario'))
        elif resultado and resultado[1] == 2:
            msg[0] = 'Login realizado com sucesso'
            return redirect(url_for('formulario'))
        else:
            msg[0] = 'NIF ou senha inválidos'
            return redirect(url_for('inicio'))
    return render_template('index.html')


@app.route('/listagem')
def listagem ():
    return render_template('tela_listagem.html')

@app.route('/formulario')
def formulario ():
    return render_template('formulario.html')

@app.route("/enviar", methods=["GET", "POST"])
def envio():
    global numero, msg2, nome_aluno, email_destinatario_aluno, curso_aluno, data_aluno, opcao_aluno, telefone_aluno, horario_aluno
    resultado = None

    if request.method == "POST":

        horario_aluno = request.form["horario"]
        nome_aluno = request.form["nome"]
        email_destinatario_aluno = request.form["email_destinatario"]
        curso_aluno = request.form["curso"]
        data_aluno = request.form["data"]
        opcao_aluno = request.form["opcao"]
        telefone_aluno = request.form["telefone"]

        remetente = "SENAI Testes"
        assunto = "Saída e entrada"
        numero = random.randint(1000, 9999)
        mensagem = "O aluno " , nome_aluno , " irá sair as " , horario_aluno , ". Informe o código abaixo para que possa efetuar a saída" , numero
        
        try:    
            email = EmailMessage()
            email["Subject"] = assunto
            email["From"] = EMAIL_REMETENTE
            email["To"] = email_destinatario_aluno
            corpo = f"Mensagem de: {remetente}\n\n{mensagem}"
            email.set_content(corpo)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
                smtp.send_message(email)

            resultado = "E-mail enviado com sucesso!"
        except Exception as e:
            resultado = f"Erro ao enviar e-mail: {str(e)}"

    return  redirect(url_for('login', resultado = resultado))

@app.route('/tela1')
def login ():
    global msg2
    return render_template('tela1.html', msg=msg[0])

@app.route('/conferir', methods=["GET", "POST"])
def conferir ():
    global numero
    
    cod = request.form['codigo']
    
    print(cod,' == ', numero)
    if str(cod) == str(numero):
        msg[0] = "Código válido"
        msg[1] = 0

        valor = (nome_aluno, telefone_aluno, email_destinatario_aluno, curso_aluno, opcao_aluno, data_aluno, horario_aluno)
        SQL = f'INSERT INTO alunos (nome, telefone, email_destinatario, curso, opcao, data_ocorrencia, horario) VALUES {valor}'
        conectBD(SQL)
        return render_template('tela2.html')
    
    else:
        msg[0] = "Código inválido"
        msg[1] = 0
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)