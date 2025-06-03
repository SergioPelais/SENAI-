from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import random

# Carrega variáveis de ambiente
load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")

app = Flask(__name__)
alo = 0

app.config['SECRET_KEY'] = 'Senai@791'
 
@app.route('/')
def inicio ():
    return render_template('index.html')

@app.route('/formulario')
def formulario ():
    return render_template('formulario.html')

@app.route("/enviar", methods=["GET", "POST"])
def envio():
    resultado = None

    if request.method == "POST":
        remetente = "SENAI Testes"
        horario = request.form["horario"]
        nome = request.form["nome"]
        email_destinatario = request.form["email_destinatario"]
        assunto = "Saída e entrada"
        numero = random.randint(100000, 999999)
        mensagem = "O aluno " , nome , " irá sair as " , horario , ". Informe o código abaixo para que possa efetuar a saída" , numero
        

        try:
            
            msg = EmailMessage()
            msg["Subject"] = assunto
            msg["From"] = EMAIL_REMETENTE
            msg["To"] = email_destinatario
            corpo = f"Mensagem de: {remetente}\n\n{mensagem}"
            msg.set_content(corpo)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
                smtp.send_message(msg)

            resultado = "E-mail enviado com sucesso!"
        except Exception as e:
            resultado = f"Erro ao enviar e-mail: {str(e)}"

    return redirect(url_for('login', resultado = resultado))

@app.route('/tela1')
def login ():
    return render_template('tela1.html')

@app.route('/acessar')
def acessar ():
    return render_template('tela2.html')


if __name__ == '__main__':
    app.run(debug=True) 