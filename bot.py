import os
import sys
import time
import random
import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from neonize.client import NewClient
from neonize.events import ConnectedEv, DisconnectedEv, LoggedOutEv, PairStatusEv, MessageEv
from neonize.utils import extract_text

from config import (
    TARGET_CHAT,
    get_target_jid,
    NOTIFY_PHONE,
    ENABLE_NOTIFY,
    get_notify_jid,
    IS_VIP,
    ROLL_COUNT,
    RROLL_COUNT,
    INTERVAL_ROLL_HOURS,
    INTERVAL_RROLL_HOURS,
    INTERVAL_CHECKIN_HOURS,
    DELAY_MIN,
    DELAY_MAX,
    ENABLE_ROLL,
    ENABLE_RROLL,
    ENABLE_CHECKIN,
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
logger = logging.getLogger("WaifusBot")

# Instancia o cliente do WhatsApp
client = NewClient(DATABASE_PATH)

# Instancia o agendador em segundo plano
scheduler = BackgroundScheduler()

# Estatísticas em memória
stats = {
    "started_at": datetime.now(),
    "rolls_sent": 0,
    "rrolls_sent": 0,
    "checkins_sent": 0,
    "last_roll": None,
    "last_rroll": None,
    "last_checkin": None,
}


def send_command(command: str):
    """Envia um único comando de texto para o destino configurado (Madotsu/Grupo)."""
    jid = get_target_jid()
    logger.info(f"📤 Enviando comando: '{command}' para {TARGET_CHAT}")
    client.send_message(to=jid, message=command)


def notify_owner(message_text: str):
    """Envia um ping/aviso informativo para o seu número pessoal quando o bot disparar."""
    if not ENABLE_NOTIFY or not NOTIFY_PHONE:
        return

    notify_jid = get_notify_jid()
    if not notify_jid:
        return

    try:
        logger.info(f"🔔 Enviando aviso/ping para seu número pessoal: {NOTIFY_PHONE}")
        client.send_message(to=notify_jid, message=message_text)
    except Exception as e:
        logger.error(f"Falha ao enviar aviso para número pessoal ({NOTIFY_PHONE}): {e}")


def sleep_humanized():
    """Aguarda um intervalo aleatório entre envios para evitar flood/bloqueio."""
    delay = random.uniform(DELAY_MIN, DELAY_MAX)
    time.sleep(delay)


def get_job_next_run(job_id: str) -> str:
    """Retorna o horário formatado do próximo disparo de um job."""
    job = scheduler.get_job(job_id)
    if job and job.next_run_time:
        return job.next_run_time.strftime("%d/%m %H:%M:%S")
    return "Desativado"


def execute_roll(source: str = "Agendado"):
    """
    Executa a rotina de m.roll:
    - 5 rolls a cada 2h (ou 9 se VIP)
    - Pequeno delay humanizado entre cada envio
    - Envia aviso/ping para o seu número pessoal ao concluir
    """
    if not ENABLE_ROLL:
        return

    logger.info(f"🎲 [ROTINA m.roll] Iniciando ciclo ({source}): {ROLL_COUNT} rolls...")
    sucessos = 0

    for i in range(1, ROLL_COUNT + 1):
        try:
            send_command("m.roll")
            stats["rolls_sent"] += 1
            stats["last_roll"] = datetime.now()
            sucessos += 1
            logger.info(f"   ↳ Roll {i}/{ROLL_COUNT} enviado com sucesso.")
            
            if i < ROLL_COUNT:
                sleep_humanized()
        except Exception as e:
            logger.error(f"Erro ao enviar roll {i}: {e}")
            break

    # Notifica o seu número pessoal
    agora = datetime.now().strftime("%H:%M:%S")
    proximo = get_job_next_run("job_roll")
    aviso = (
        f"🎲 *[Waifus Bot - Ping]*\n\n"
        f"Ciclo de *m.roll* disparado com sucesso!\n"
        f"• *Quantidade:* {sucessos}/{ROLL_COUNT} rolls enviados para `{TARGET_CHAT}`\n"
        f"• *Origem:* {source}\n"
        f"• *Horário:* {agora}\n"
        f"• *Próximo envio:* {proximo}"
    )
    notify_owner(aviso)


def execute_rroll(source: str = "Agendado"):
    """
    Executa a rotina de m.rroll:
    - 5 rolls com maiores taxas a cada 12h
    - Delay humanizado entre cada envio
    - Envia aviso/ping para o seu número pessoal ao concluir
    """
    if not ENABLE_RROLL:
        return

    logger.info(f"💎 [ROTINA m.rroll] Iniciando ciclo ({source}): {RROLL_COUNT} rrolls...")
    sucessos = 0

    for i in range(1, RROLL_COUNT + 1):
        try:
            send_command("m.rroll")
            stats["rrolls_sent"] += 1
            stats["last_rroll"] = datetime.now()
            sucessos += 1
            logger.info(f"   ↳ RRoll {i}/{RROLL_COUNT} enviado com sucesso.")
            
            if i < RROLL_COUNT:
                sleep_humanized()
        except Exception as e:
            logger.error(f"Erro ao enviar rroll {i}: {e}")
            break

    agora = datetime.now().strftime("%H:%M:%S")
    proximo = get_job_next_run("job_rroll")
    aviso = (
        f"💎 *[Waifus Bot - Ping]*\n\n"
        f"Ciclo de *m.rroll* disparado com sucesso!\n"
        f"• *Quantidade:* {sucessos}/{RROLL_COUNT} rrolls enviados para `{TARGET_CHAT}`\n"
        f"• *Origem:* {source}\n"
        f"• *Horário:* {agora}\n"
        f"• *Próximo envio:* {proximo}"
    )
    notify_owner(aviso)


def execute_checkin(source: str = "Agendado"):
    """
    Executa a rotina de m.checkin:
    - 1 vez a cada 24 horas para manter o streak diário
    - Envia aviso/ping para o seu número pessoal
    """
    if not ENABLE_CHECKIN:
        return

    logger.info(f"📅 [ROTINA m.checkin] Enviando checkin diário ({source})...")
    try:
        send_command("m.checkin")
        stats["checkins_sent"] += 1
        stats["last_checkin"] = datetime.now()
        logger.info("   ↳ m.checkin enviado com sucesso!")

        agora = datetime.now().strftime("%H:%M:%S")
        proximo = get_job_next_run("job_checkin")
        aviso = (
            f"📅 *[Waifus Bot - Ping]*\n\n"
            f"Comando *m.checkin* enviado com sucesso para manter sua streak diária!\n"
            f"• *Destino:* `{TARGET_CHAT}`\n"
            f"• *Horário:* {agora}\n"
            f"• *Próximo checkin:* {proximo}"
        )
        notify_owner(aviso)
    except Exception as e:
        logger.error(f"Erro ao enviar checkin: {e}")


@client.event(ConnectedEv)
def on_connected(c: NewClient, event: ConnectedEv):
    logger.info("=" * 60)
    logger.info("🟢 Conectado ao WhatsApp com sucesso via WebSocket!")
    logger.info(f"🎯 Destino dos rolls (Madotsu/Grupo): {TARGET_CHAT}")
    logger.info(f"📱 Número pessoal para avisos/pings: {NOTIFY_PHONE or 'Não configurado'}")
    logger.info(f"👑 Modo VIP: {'ATIVADO (9 rolls)' if IS_VIP else 'DESATIVADO (5 rolls)'}")
    logger.info("=" * 60)

    if not scheduler.running:
        # Agendamento 1: m.roll (a cada 2 horas)
        if ENABLE_ROLL:
            scheduler.add_job(
                execute_roll,
                trigger="interval",
                hours=INTERVAL_ROLL_HOURS,
                id="job_roll",
                replace_existing=True,
                args=["Ciclo 2h"],
            )

        # Agendamento 2: m.rroll (a cada 12 horas)
        if ENABLE_RROLL:
            scheduler.add_job(
                execute_rroll,
                trigger="interval",
                hours=INTERVAL_RROLL_HOURS,
                id="job_rroll",
                replace_existing=True,
                args=["Ciclo 12h"],
            )

        # Agendamento 3: m.checkin (a cada 24 horas)
        if ENABLE_CHECKIN:
            scheduler.add_job(
                execute_checkin,
                trigger="interval",
                hours=INTERVAL_CHECKIN_HOURS,
                id="job_checkin",
                replace_existing=True,
                args=["Ciclo 24h"],
            )

        scheduler.start()
        logger.info("⏰ Agendadores ativados com sucesso:")
        logger.info(f"   • m.roll:    a cada {INTERVAL_ROLL_HOURS}h (Próximo: {get_job_next_run('job_roll')})")
        logger.info(f"   • m.rroll:   a cada {INTERVAL_RROLL_HOURS}h (Próximo: {get_job_next_run('job_rroll')})")
        logger.info(f"   • m.checkin: a cada {INTERVAL_CHECKIN_HOURS}h (Próximo: {get_job_next_run('job_checkin')})")

        # Notifica o dono que o bot acabou de ligar
        notify_owner(
            f"🟢 *[Waifus Bot - Online]*\n\n"
            f"O bot foi iniciado na VPS e está conectado com sucesso!\n"
            f"• *Destino dos rolls:* `{TARGET_CHAT}`\n"
            f"• *m.roll:* a cada {INTERVAL_ROLL_HOURS}h (Próximo: {get_job_next_run('job_roll')})\n"
            f"• *m.rroll:* a cada {INTERVAL_RROLL_HOURS}h (Próximo: {get_job_next_run('job_rroll')})\n"
            f"• *m.checkin:* a cada {INTERVAL_CHECKIN_HOURS}h (Próximo: {get_job_next_run('job_checkin')})\n\n"
            f"Envie *!ping* ou *!status* a qualquer momento."
        )

        # Disparo inicial opcional
        if RUN_IMMEDIATELY:
            logger.info("🚀 RUN_IMMEDIATELY=true: Executando primeiro ciclo de validação...")
            if ENABLE_ROLL:
                execute_roll("Inicialização")
            if ENABLE_RROLL:
                execute_rroll("Inicialização")
            if ENABLE_CHECKIN:
                execute_checkin("Inicialização")


@client.event(DisconnectedEv)
def on_disconnected(c: NewClient, event: DisconnectedEv):
    logger.warning("🟡 Conexão interrompida. Tentando reconectar...")


@client.event(LoggedOutEv)
def on_logged_out(c: NewClient, event: LoggedOutEv):
    logger.error("🔴 Sessão desvinculada pelo celular! Escaneie o QR Code novamente.")


@client.event(PairStatusEv)
def on_pair_status(c: NewClient, event: PairStatusEv):
    logger.info(f"📲 Pareamento realizado com sucesso: {event.ID.User}")


@client.event(MessageEv)
def on_message(c: NewClient, message: MessageEv):
    """Permite comandos administrativos enviados via WhatsApp."""
    if message.Info.MessageSource.IsFromMe:
        return

    text = extract_text(message.Message).strip()
    if not text:
        return

    cmd = text.lower()

    if cmd in ("!ping", "ping", "/ping"):
        agora = datetime.now().strftime("%H:%M:%S")
        uptime = str(datetime.now() - stats["started_at"]).split(".")[0]
        reply = (
            f"🏓 *Pong!*\n\n"
            f"• *Status:* 🟢 Bot Ativo e Operando na VPS\n"
            f"• *Horário:* {agora}\n"
            f"• *Tempo ativo:* {uptime}\n"
            f"• *Destino dos comandos:* `{TARGET_CHAT}`\n\n"
            f"🕒 *Próximos Envios:*\n"
            f"  🎲 m.roll: {get_job_next_run('job_roll')}\n"
            f"  💎 m.rroll: {get_job_next_run('job_rroll')}\n"
            f"  📅 m.checkin: {get_job_next_run('job_checkin')}"
        )
        c.reply_message(reply, message)

    elif cmd in ("!status", "/status"):
        uptime = str(datetime.now() - stats["started_at"]).split(".")[0]
        reply = (
            f"📊 *Painel do Waifus Auto-Bot*\n\n"
            f"• *Status:* 🟢 Conectado e Ativo\n"
            f"• *Destino:* `{TARGET_CHAT}`\n"
            f"• *Avisos para você:* `{NOTIFY_PHONE or 'Desativado'}`\n"
            f"• *Modo VIP:* {'Sim (9 rolls)' if IS_VIP else 'Não (5 rolls)'}\n\n"
            f"🕒 *Próximos Disparos:*\n"
            f"  🎲 m.roll: {get_job_next_run('job_roll')}\n"
            f"  💎 m.rroll: {get_job_next_run('job_rroll')}\n"
            f"  📅 m.checkin: {get_job_next_run('job_checkin')}\n\n"
            f"📈 *Total Enviados:*\n"
            f"  • Rolls: {stats['rolls_sent']}\n"
            f"  • RRolls: {stats['rrolls_sent']}\n"
            f"  • Checkins: {stats['checkins_sent']}\n"
            f"  • Uptime: {uptime}"
        )
        c.reply_message(reply, message)

    elif cmd == "!roll":
        c.reply_message(f"🎲 Disparando {ROLL_COUNT} rolls manuais para `{TARGET_CHAT}`...", message)
        execute_roll("Manual")

    elif cmd == "!rroll":
        c.reply_message(f"💎 Disparando {RROLL_COUNT} rrolls manuais para `{TARGET_CHAT}`...", message)
        execute_rroll("Manual")

    elif cmd == "!checkin":
        c.reply_message(f"📅 Disparando m.checkin manual para `{TARGET_CHAT}`...", message)
        execute_checkin("Manual")

    elif cmd in ("!grupos", "/grupos"):
        try:
            groups = c.get_joined_groups()
            if not groups:
                c.reply_message("Nenhum grupo encontrado nesta conta.", message)
                return

            linhas = ["📋 *Grupos Encontrados:*", "Copie o ID do grupo desejado para o .env (`TARGET_CHAT`):\n"]
            for g in groups:
                gid = f"{g.JID.User}@g.us"
                name = g.GroupName.Name if g.GroupName.Name else "Sem Nome"
                linhas.append(f"• *{name}*\n  `{gid}`\n")
            
            c.reply_message("\n".join(linhas), message)
        except Exception as e:
            c.reply_message(f"Erro ao listar grupos: {e}", message)

    elif cmd in ("!ajuda", "/ajuda", "help"):
        reply = (
            "📌 *Comandos de Controle do Bot:*\n\n"
            "• `!ping` - Teste de resposta e status rápido\n"
            "• `!status` - Exibe os próximos horários e total enviado\n"
            "• `!roll` - Força envio do ciclo de m.roll agora\n"
            "• `!rroll` - Força envio do ciclo de m.rroll agora\n"
            "• `!checkin` - Força envio do m.checkin agora\n"
            "• `!grupos` - Lista todos os seus grupos e IDs\n"
            "• `!ajuda` - Exibe esta mensagem"
        )
        c.reply_message(reply, message)


def main():
    print("""
    ======================================================
        🌸 WhatsApp Waifus Auto-Bot (Madotsu 5)
        m.roll (2h) | m.rroll (12h) | m.checkin (24h)
        Com Pings e Avisos no seu WhatsApp Pessoal
    ======================================================
    """)

    if not validate_config():
        sys.exit(1)

    logger.info(f"Destino dos comandos: {TARGET_CHAT}")
    logger.info(f"Número para avisos/pings: {NOTIFY_PHONE or 'Desativado'}")
    logger.info(f"Modo VIP: {'Sim (9 rolls)' if IS_VIP else 'Não (5 rolls)'}")
    logger.info("Iniciando conexão WebSocket...")

    try:
        client.connect()
    except KeyboardInterrupt:
        logger.info("\nEncerrando bot...")
    finally:
        if scheduler.running:
            scheduler.shutdown(wait=False)
        logger.info("Bot finalizado.")


if __name__ == "__main__":
    main()
