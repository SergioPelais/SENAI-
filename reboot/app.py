from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import resources.database_connection as database_connection

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

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")


msgRep = False
def msg(mensagem):
    global msgRep
    msgRep = not msgRep
    return mensagem if msgRep else ''

@app.route('/',methods=["GET", "POST"])
def inicio ():

    return render_template('index.html', )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)