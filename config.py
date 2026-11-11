import os
import re
from datetime import timedelta
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

def clean_phone_number(raw_phone: str) -> str:
    """
    Remove caracteres não numéricos e formata o número para o padrão internacional.
    Exemplo: +55 (11) 98765-4321 -> 5511987654321
    """
    digits_only = re.sub(r"\D", "", raw_phone or "")
    return digits_only

# Configurações do Alvo e Mensagem
TARGET_PHONE = clean_phone_number(os.getenv("TARGET_PHONE", ""))
REMINDER_MESSAGE = os.getenv(
    "REMINDER_MESSAGE", 
    "🔔 *Lembrete Automático*\n\nNão se esqueça da sua atividade programada! 🚀"
)

# Intervalo de envio (suporta horas e minutos para testes)
try:
    INTERVAL_HOURS = float(os.getenv("REMINDER_INTERVAL_HOURS", "2"))
except ValueError:
    INTERVAL_HOURS = 2.0

try:
    INTERVAL_MINUTES = float(os.getenv("REMINDER_INTERVAL_MINUTES", "0"))
except ValueError:
    INTERVAL_MINUTES = 0.0

# Se horas e minutos forem 0, define padrão para 1 hora
TOTAL_SECONDS = int(INTERVAL_HOURS * 3600 + INTERVAL_MINUTES * 60)
if TOTAL_SECONDS <= 0:
    TOTAL_SECONDS = 3600

# Executar imediatamente ao conectar?
RUN_IMMEDIATELY = os.getenv("RUN_IMMEDIATELY", "false").strip().lower() in ("true", "1", "yes", "sim")

# Caminho do banco SQLite de sessão do WhatsApp
DATABASE_PATH = os.getenv("DATABASE_PATH", "session.sqlite3")

# Validação inicial
def validate_config() -> bool:
    if not TARGET_PHONE:
        print("\n⚠️  [ATENÇÃO] A variável TARGET_PHONE não está definida no arquivo .env!")
        print("👉 Preencha com seu número completo (DDI + DDD + Número), por exemplo: 5511999999999\n")
        return False
    return True
