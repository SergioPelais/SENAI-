from flask import Flask, request, render_template_string
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Formulário de E-mail</title>
</head>
<body>
    <h2>Enviar E-mail</h2>
    <form method="POST">
        <label for="nome">Seu Nome:</label><br>
        <input type="text" id="nome" name="nome" required><br><br>

        <label for="email_destinatario">E-mail do Destinatário:</label><br>
        <input type="email" id="email_destinatario" name="email_destinatario" required><br><br>

        <label for="assunto">Assunto:</label><br>
        <input type="text" id="assunto" name="assunto" required><br><br>

        <label for="mensagem">Mensagem:</label><br>
        <textarea id="mensagem" name="mensagem" rows="6" cols="40" required></textarea><br><br>

        <button type="submit">Enviar</button>
    </form>
    {% if resultado %}
        <p><strong>{{ resultado }}</strong></p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def formulario():
    resultado = None

    if request.method == "POST":
        nome = request.form["nome"]
        email_destinatario = request.form["email_destinatario"]
        assunto = request.form["assunto"]
        mensagem = request.form["mensagem"]

        try:
            msg = EmailMessage()
            msg["Subject"] = assunto
            msg["From"] = EMAIL_REMETENTE
            msg["To"] = email_destinatario
            corpo = f"Mensagem de: {nome}\n\n{mensagem}"
            msg.set_content(corpo)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
                smtp.send_message(msg)

            resultado = "E-mail enviado com sucesso!"
        except Exception as e:
            resultado = f"Erro ao enviar e-mail: {str(e)}"

    return render_template_string(HTML_FORM, resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
