import os
import sys
import logging
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from neonize.client import NewClient
from neonize.events import ConnectedEv, DisconnectedEv, LoggedOutEv, PairStatusEv, MessageEv
from neonize.utils import build_jid, extract_text

from config import (
    TARGET_PHONE,
    REMINDER_MESSAGE,
    INTERVAL_HOURS,
    INTERVAL_MINUTES,
    TOTAL_SECONDS,
    RUN_IMMEDIATELY,
    DATABASE_PATH,
    validate_config,
)

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("WhatsAppReminderBot")

# Instancia o cliente do WhatsApp (banco SQLite para manter sessão ativa)
client = NewClient(DATABASE_PATH)

# Instancia o agendador em segundo plano
scheduler = BackgroundScheduler()

# Estatísticas em memória
stats = {
    "started_at": datetime.now(),
    "sent_count": 0,
    "last_sent": None,
}

def send_reminder(trigger_source: str = "Agendado"):
    """Função responsável por formatar e enviar o lembrete via WebSocket."""
    if not TARGET_PHONE:
        logger.warning("Número de destino não configurado no .env!")
        return

    now_str = datetime.now().strftime("%H:%M:%S")
    formatted_message = f"{REMINDER_MESSAGE}\n\n🕒 _Horário: {now_str}_"

    try:
        jid = build_jid(TARGET_PHONE)
        logger.info(f"📤 Enviando lembrete ({trigger_source}) para {TARGET_PHONE}...")
        client.send_message(to=jid, message=formatted_message)
        
        stats["sent_count"] += 1
        stats["last_sent"] = datetime.now()
        logger.info(f"✅ Lembrete enviado com sucesso! Total enviados: {stats['sent_count']}")
    except Exception as e:
        logger.error(f"❌ Falha ao enviar lembrete: {e}", exc_info=True)


def get_next_run_str() -> str:
    """Retorna o horário do próximo disparo formatado."""
    jobs = scheduler.get_jobs()
    if jobs and jobs[0].next_run_time:
        return jobs[0].next_run_time.strftime("%d/%m/%Y às %H:%M:%S")
    return "Aguardando agendamento"


@client.event(ConnectedEv)
def on_connected(c: NewClient, event: ConnectedEv):
    logger.info("=" * 55)
    logger.info("🟢 Conectado ao WhatsApp com sucesso via WebSocket!")
    logger.info("=" * 55)

    # Inicia o agendador se ainda não estiver rodando
    if not scheduler.running:
        scheduler.add_job(
            send_reminder,
            trigger="interval",
            seconds=TOTAL_SECONDS,
            id="reminder_job",
            replace_existing=True,
            args=["Agendamento Periódico"],
        )
        scheduler.start()
        logger.info(f"⏰ Agendador iniciado! Intervalo: {TOTAL_SECONDS / 3600:.2f}h ({TOTAL_SECONDS}s)")
        logger.info(f"📅 Próximo lembrete programado para: {get_next_run_str()}")

        # Envia primeiro lembrete de imediato, se configurado
        if RUN_IMMEDIATELY:
            logger.info("🚀 RUN_IMMEDIATELY=true: Disparando primeiro lembrete...")
            send_reminder("Inicialização")


@client.event(DisconnectedEv)
def on_disconnected(c: NewClient, event: DisconnectedEv):
    logger.warning("🟡 Conexão com o WhatsApp foi interrompida. Tentando reconectar...")


@client.event(LoggedOutEv)
def on_logged_out(c: NewClient, event: LoggedOutEv):
    logger.error("🔴 Sessão desconectada/desvinculada pelo celular! Escaneie o QR Code novamente.")


@client.event(PairStatusEv)
def on_pair_status(c: NewClient, event: PairStatusEv):
    logger.info(f"📲 Status de Pareamento: {event.ID.User} conectado com sucesso!")


@client.event(MessageEv)
def on_message(c: NewClient, message: MessageEv):
    """Permite comandos interativos enviados pelo próprio número."""
    # Ignora mensagens enviadas pelo próprio bot para evitar loops
    if message.Info.MessageSource.IsFromMe:
        return

    sender_user = message.Info.MessageSource.Sender.User
    chat_user = message.Info.MessageSource.Chat.User

    # Verifica se a mensagem veio do número alvo autorizado
    if TARGET_PHONE not in (sender_user, chat_user):
        return

    text = extract_text(message.Message).strip()
    if not text:
        return

    cmd = text.lower()
    
    if cmd in ("!status", "/status", "status"):
        uptime = str(datetime.now() - stats["started_at"]).split(".")[0]
        last_str = stats["last_sent"].strftime("%H:%M:%S") if stats["last_sent"] else "Nenhum ainda"
        
        reply = (
            f"🤖 *Status do Bot de Lembretes*\n\n"
            f"• *Status:* 🟢 Conectado e Ativo\n"
            f"• *Intervalo:* A cada {INTERVAL_HOURS}h (ou {TOTAL_SECONDS // 60} min)\n"
            f"• *Próximo envio:* {get_next_run_str()}\n"
            f"• *Total enviados:* {stats['sent_count']}\n"
            f"• *Último envio:* {last_str}\n"
            f"• *Tempo ativo:* {uptime}\n\n"
            f"Envie *!lembrete* para disparar um agora ou *!ajuda*."
        )
        c.reply_message(reply, message)

    elif cmd in ("!lembrete", "/lembrete", "lembrete"):
        c.reply_message("⚡ Enviando lembrete manual solicitado...", message)
        send_reminder("Comando Manual")

    elif cmd in ("!ajuda", "/ajuda", "ajuda", "help"):
        reply = (
            "📌 *Comandos Disponíveis:*\n\n"
            "• *!status* - Exibe o status da conexão e próximo envio.\n"
            "• *!lembrete* - Envia um lembrete teste imediatamente.\n"
            "• *!ajuda* - Mostra este menu de instruções."
        )
        c.reply_message(reply, message)


def main():
    print("""
    ==================================================
        🤖 WhatsApp Reminder Bot (Web/Socket)
        Consumo de memória ultra-baixo (~50MB)
    ==================================================
    """)

    if not validate_config():
        sys.exit(1)

    logger.info(f"Destinatário configurado: {TARGET_PHONE}")
    logger.info(f"Intervalo programado: {TOTAL_SECONDS} segundos ({TOTAL_SECONDS / 3600:.2f}h)")
    logger.info("Iniciando conexão com o WhatsApp...")
    logger.info("👉 Caso seja a primeira vez, o QR Code será exibido abaixo:")

    try:
        # client.connect() conecta aos WebSockets do WhatsApp
        # Se for o primeiro acesso, desenha o QR Code no terminal automaticamente
        client.connect()
    except KeyboardInterrupt:
        logger.info("\nEncerrando bot com segurança...")
    finally:
        if scheduler.running:
            scheduler.shutdown(wait=False)
        logger.info("Bot finalizado.")


if __name__ == "__main__":
    main()
