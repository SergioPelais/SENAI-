import time
from functools import wraps
from flask import session, redirect, url_for, flash

# Tentativas de login e bloqueio
tentativas_login = {}
bloqueados = {}
TEMPO_BLOQUEIO = 60  # segundos
MAX_ERROS = 5

def registrar_tentativa(nome):
    agora = time.time()
    if nome not in tentativas_login:
        tentativas_login[nome] = {"erros": 0, "ultimo": agora}
    reg = tentativas_login[nome]
    if agora - reg["ultimo"] > TEMPO_BLOQUEIO:
        reg["erros"] = 0
    reg["erros"] += 1
    reg["ultimo"] = agora
    if reg["erros"] >= MAX_ERROS:
        bloqueados[nome] = agora + TEMPO_BLOQUEIO
        return True
    return False

def verificar_bloqueio(nome):
    agora = time.time()
    if nome in bloqueados:
        if agora > bloqueados[nome]:
            bloqueados.pop(nome)
            tentativas_login[nome]["erros"] = 0
            return False
        return True
    return False

# Decorator para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario' not in session:
            flash(["Faça login primeiro!",'login'])
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated
