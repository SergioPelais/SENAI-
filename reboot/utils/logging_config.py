import os
import logging
from logging.handlers import TimedRotatingFileHandler
import json
from datetime import datetime
from flask import request

# Cria diretório de logs
os.makedirs('logs', exist_ok=True)

# Logger do sistema
APP_LOG_FILE = 'logs/app.log'
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.INFO)
app_handler = TimedRotatingFileHandler(APP_LOG_FILE, when='midnight', interval=1, backupCount=30, encoding='utf-8')
app_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
app_logger.addHandler(app_handler)

# Logger de auditoria em JSON
AUDIT_LOG_FILE = 'logs/auditoria.log'
audit_logger = logging.getLogger('audit_logger')
audit_logger.setLevel(logging.INFO)
audit_handler = TimedRotatingFileHandler(AUDIT_LOG_FILE, when='midnight', interval=1, backupCount=90, encoding='utf-8')
audit_handler.setFormatter(logging.Formatter('%(message)s'))
audit_logger.addHandler(audit_handler)

def log_auditoria(usuario, acao):
    """Registra uma ação de auditoria em JSON."""
    data_log = {
        "usuario": usuario,
        "acao": acao,
        "ip": request.remote_addr,
        "timestamp": datetime.now().isoformat()
    }
    audit_logger.info(json.dumps(data_log))