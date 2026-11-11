import os
import re
from dotenv import load_dotenv
from neonize.proto.Neonize_pb2 import JID
from neonize.utils import build_jid

# Carrega as variáveis do arquivo .env
load_dotenv()

def clean_phone_number(raw_phone: str) -> str:
    """Remove caracteres não numéricos de um número de telefone."""
    return re.sub(r"\D", "", raw_phone or "")

# Número privado do bot de destino (NUNCA ID de grupo)
RAW_TARGET = os.getenv(
    "TARGET_BOT_PHONE", 
    os.getenv("TARGET_CHAT", os.getenv("TARGET_PHONE", ""))
).strip()
TARGET_BOT_PHONE = clean_phone_number(RAW_TARGET)

# Trava de segurança: detectar se alguém tentou passar um ID de grupo
IS_GROUP_TARGET = "@g.us" in RAW_TARGET.lower()

def get_target_jid() -> JID:
    """
    Retorna estritamente o JID privado do bot de destino (@s.whatsapp.net).
    Bloqueia categoricamente qualquer tentativa de envio para grupos (@g.us).
    """
    if IS_GROUP_TARGET or not TARGET_BOT_PHONE:
        raise ValueError(
            "❌ [TRAVA DE SEGURANÇA] Envio para grupos (@g.us) está estritamente bloqueado! "
            "Configure apenas o número privado do bot de destino."
        )
    return build_jid(TARGET_BOT_PHONE)

# Seu número pessoal para receber Pings e Avisos quando o bot disparar
NOTIFY_PHONE = clean_phone_number(os.getenv("NOTIFY_PHONE", os.getenv("ADMIN_PHONE", "")))
ENABLE_NOTIFY = os.getenv("ENABLE_NOTIFY", "true").strip().lower() in ("true", "1", "yes", "sim")

def get_notify_jid() -> JID | None:
    """Retorna o JID do número pessoal do dono se configurado."""
    if NOTIFY_PHONE:
        return build_jid(NOTIFY_PHONE)
    return None

# Configurações VIP
IS_VIP = os.getenv("IS_VIP", "false").strip().lower() in ("true", "1", "yes", "sim")

# Quantidade de rolls por ciclo:
# VIP: 9 rolls a cada 2h | Comum: 5 rolls a cada 2h
ROLL_COUNT = int(os.getenv("ROLL_COUNT", "9" if IS_VIP else "5"))

# Quantidade de rrolls por ciclo: 5 a cada 12h
RROLL_COUNT = int(os.getenv("RROLL_COUNT", "5"))

# Intervalos em horas
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

# Garante que o diretório do banco de dados exista (especialmente no Docker)
db_dir = os.path.dirname(DATABASE_PATH)
if db_dir:
    os.makedirs(db_dir, exist_ok=True)

def validate_config() -> bool:
    if IS_GROUP_TARGET:
        print("\n🚫 [BLOQUEIO DE SEGURANÇA ATIVADO]")
        print("Detectado ID de grupo (@g.us) no arquivo .env!")
        print("Os comandos m.roll e m.rroll NÃO PODEM ser enviados para grupos para evitar flood.")
        print("👉 Preencha a variável TARGET_BOT_PHONE apenas com o número privado do bot de destino (ex: 5511999999999).\n")
        return False

    if not TARGET_BOT_PHONE:
        print("\n⚠️  [ATENÇÃO] A variável TARGET_BOT_PHONE não está configurada no .env!")
        print("👉 Preencha com o número privado do bot de destino (DDI + DDD + Número), por exemplo: 5511999999999.\n")
        return False

    return True
