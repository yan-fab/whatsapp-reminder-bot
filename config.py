import os
import re
from dotenv import load_dotenv
from neonize.proto.Neonize_pb2 import JID
from neonize.utils import build_jid

# Carrega as variáveis do arquivo .env
load_dotenv()

# Destino das mensagens (pode ser seu número pessoal ou o JID do Grupo)
# Exemplo número pessoal: 5511999999999
# Exemplo grupo: 120363048999999999@g.us
TARGET_CHAT = os.getenv("TARGET_CHAT", os.getenv("TARGET_PHONE", "")).strip()

def get_target_jid(raw_target: str = TARGET_CHAT) -> JID:
    """
    Identifica se o destino é um grupo (@g.us) ou um número pessoal (@s.whatsapp.net)
    e retorna o JID correspondente pronto para envio no Neonize.
    """
    raw = (raw_target or "").strip()
    if "@g.us" in raw:
        group_user = raw.replace("@g.us", "")
        return JID(User=group_user, Server="g.us")
    elif "@s.whatsapp.net" in raw:
        digits = re.sub(r"\D", "", raw.replace("@s.whatsapp.net", ""))
        return build_jid(digits)
    else:
        digits = re.sub(r"\D", "", raw)
        return build_jid(digits)

# Configurações VIP
IS_VIP = os.getenv("IS_VIP", "false").strip().lower() in ("true", "1", "yes", "sim")

# Quantidade de rolls por ciclo:
# VIP: 9 rolls a cada 2h | Comum: 5 rolls a cada 2h
ROLL_COUNT = int(os.getenv("ROLL_COUNT", "9" if IS_VIP else "5"))

# Quantidade de rrolls por ciclo: 5 a cada 12h
RROLL_COUNT = int(os.getenv("RROLL_COUNT", "5"))

# Intervalos em horas (conforme comandos_waifus.md)
INTERVAL_ROLL_HOURS = float(os.getenv("INTERVAL_ROLL_HOURS", "2"))        # m.roll a cada 2 horas
INTERVAL_RROLL_HOURS = float(os.getenv("INTERVAL_RROLL_HOURS", "12"))     # m.rroll a cada 12 horas
INTERVAL_CHECKIN_HOURS = float(os.getenv("INTERVAL_CHECKIN_HOURS", "24")) # m.checkin a cada 24 horas

# Delays humanizados entre cada envio consecutivo (em segundos) para evitar bloqueio/flood
DELAY_MIN = float(os.getenv("DELAY_MIN", "3.0"))
DELAY_MAX = float(os.getenv("DELAY_MAX", "6.0"))

# Habilitar ou desabilitar comandos individualmente
ENABLE_ROLL = os.getenv("ENABLE_ROLL", "true").strip().lower() in ("true", "1", "yes", "sim")
ENABLE_RROLL = os.getenv("ENABLE_RROLL", "true").strip().lower() in ("true", "1", "yes", "sim")
ENABLE_CHECKIN = os.getenv("ENABLE_CHECKIN", "true").strip().lower() in ("true", "1", "yes", "sim")

# Disparar um primeiro ciclo de comandos assim que conectar?
RUN_IMMEDIATELY = os.getenv("RUN_IMMEDIATELY", "true").strip().lower() in ("true", "1", "yes", "sim")

# Caminho do banco SQLite de sessão do WhatsApp
DATABASE_PATH = os.getenv("DATABASE_PATH", "session.sqlite3")

def validate_config() -> bool:
    if not TARGET_CHAT:
        print("\n⚠️  [ATENÇÃO] A variável TARGET_CHAT não está configurada no .env!")
        print("👉 Preencha com o número (ex: 5511999999999) ou o ID do Grupo (ex: 1203630XXXXXXXX@g.us).\n")
        return False
    return True
