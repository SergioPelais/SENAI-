from flask import Flask, render_template, request, redirect, url_for
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

    return resultado


# nova função para tratamento de notificações, mas ainda está em teste
msgAtivo = False
def msg(mensagem):
    global msgAtivo
    msgAtivo = not msgAtivo
    return mensagem if msgAtivo else ''


@app.route('/',methods=["GET", "POST"])
def inicio ():
    if request.method == "POST":
        estado = request.form['estado']
        caso = request.form['caso']
        emailResp = request.form['emailResp']
        solicitarCod = request.form.get('receber_codigo')


        docente = "SENAI bot."
        msgEmail = ''
        if estado == 'true':
            if caso=='Saída' and solicitarCod == 'sim':
                msgEmail = 'solicitação do aluno com código [XXXXXX]'
            else:
                msgEmail = 'solicitação do aluno sem código'
            callEmail(emailResp,docente,f"Solicitação de {'Saída'if caso == 'Saída' else 'Entrada'}",msgEmail)


    data = conectBD('SELECT * FROM alunos;',1)
    return render_template('autorizacao.html',bd=json.dumps(data,default=str))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)