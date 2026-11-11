# 🌸 WhatsApp Waifus Auto-Bot (Madotsu 5 / RolêSP)

Bot de automação pessoal via **WebSockets direto** (sem navegador pesado, consumindo apenas ~50MB de RAM) para envio automático dos comandos periódicos do sistema de Waifus do **Bot Madotsu 5**.

---

## 📋 Tabela de Comandos e Intervalos (Conforme o Guia)

| Comando | Onde usar | Quantidade / Intervalo | Modo VIP | Função |
| :--- | :--- | :--- | :--- | :--- |
| `m.roll` | Grupo | **5 rolls a cada 2 horas** | **9 rolls a cada 2 horas** | Rola personagem aleatório comum, rara, épica, lendária e mítica. |
| `m.rroll` | Grupo | **5 rolls a cada 12 horas** | *(igual)* | Rola com taxas aumentadas para raridades raras ou superiores. |
| `m.checkin` | Grupo / Bot | **1 vez a cada 24 horas** | *(2 dias de tolerância)* | Mantém a sequência (*streak*) diária no perfil. |

---

## 🛡️ Anti-Flood & Simulação Humana
Para cumprir as diretrizes da comunidade e evitar avisos/bloqueios por spam, o bot:
- Não envia todos os rolls de uma vez só: ele aguarda um **delay aleatório humanizado** (entre 3 e 6 segundos) entre cada `m.roll` e `m.rroll`.
- Desconecta de forma segura e reconecta automaticamente se a rede oscilar.

---

## 🚀 Como Executar Localmente

### 1. Configurar o `.env`
Abra o arquivo `.env` e configure o destino:
```env
# Se for mandar no seu próprio número ou privado:
TARGET_CHAT=5511999999999

# OU se for mandar diretamente dentro do Grupo do WhatsApp:
# TARGET_CHAT=1203630XXXXXXXXX@g.us

# Se você tem VIP no Madotsu:
IS_VIP=false
```

> 💡 **Dica para descobrir o ID do seu Grupo:**  
> Ao iniciar o bot, envie `!grupos` pelo WhatsApp para ele. O bot responderá com uma lista de todos os seus grupos e seus respectivos IDs (`@g.us`). Basta copiar e colar no `TARGET_CHAT`.

### 2. Iniciar o Bot

```bash
cd whatsapp-reminder-bot
python bot.py
```

1. Na primeira execução, o **QR Code** será exibido no seu terminal.
2. No celular: **WhatsApp > Aparelhos Conectados > Conectar um Aparelho** e escaneie.
3. A sessão será salva localmente em `session.sqlite3` (você só escaneia uma vez).

---

## 💬 Comandos Interativos no WhatsApp

Você pode enviar comandos para o bot pelo próprio WhatsApp:
- `!status` - Exibe os próximos horários exatos de `m.roll`, `m.rroll` e `m.checkin`, e o total já enviado.
- `!roll` - Executa o ciclo de `m.roll` imediatamente.
- `!rroll` - Executa o ciclo de `m.rroll` imediatamente.
- `!checkin` - Executa o `m.checkin` imediatamente.
- `!grupos` - Lista todos os seus grupos e seus respectivos IDs.
- `!ajuda` - Exibe o menu de ajuda.

---

## ☁️ Deploy 24/7 na Nuvem (VPS Gratuita)

Como o bot consome apenas **~50MB de RAM**, ele roda perfeitamente em qualquer VPS gratuita, como **Oracle Cloud Always Free** ou servidores de baixo custo (Hetzner, Hostinger).

Usando Docker:
```bash
docker compose up -d
docker compose logs -f
```

---

## 📄 Licença
Distribuído sob a licença MIT.
