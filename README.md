# 🌸 WhatsApp Waifus Auto-Bot (Madotsu 5 / RolêSP)

Bot de automação pessoal via **WebSockets direto** (sem navegador pesado, consumindo apenas ~50MB de RAM) para envio automático dos comandos periódicos do sistema de Waifus do **Bot Madotsu 5**, com **notificações e pings automáticos para o seu número pessoal**.

---

## 🔔 Pings e Avisos no seu WhatsApp Pessoal

Sempre que o bot disparar uma rotina na VPS, ele envia automaticamente um resumo para o seu número pessoal (`NOTIFY_PHONE`):
- 🎲 **Quando rola `m.roll`:** Envia aviso com quantidade de rolls enviados, horário e data/hora do próximo ciclo.
- 💎 **Quando rola `m.rroll`:** Envia confirmação dos rolls de alta taxa.
- 📅 **Quando envia `m.checkin`:** Avisa que sua streak diária foi mantida.
- 🟢 **Quando o bot liga na VPS:** Envia ping avisando que está online e operando.

Você também pode enviar **`!ping`** no WhatsApp para testar a resposta do bot a qualquer momento.

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
- Não envia todos os rolls de uma vez só: aguarda um **delay aleatório humanizado** (entre 3 e 6 segundos) entre cada `m.roll` e `m.rroll`.
- Desconecta de forma segura e reconecta automaticamente se a rede da VPS oscilar.

---

## 🚀 Configuração do `.env`

No arquivo `.env`:

```env
# 1. Destino dos comandos do jogo (Madotsu ou Grupo de Waifus):
TARGET_CHAT=5511999999999

# 2. Seu número pessoal para receber os Pings e Avisos a cada disparo:
NOTIFY_PHONE=5511988887777
ENABLE_NOTIFY=true

# 3. Assinatura VIP no Madotsu:
IS_VIP=false
```

---

## 💬 Comandos Interativos no WhatsApp

Você pode enviar comandos para o bot pelo próprio WhatsApp:
- `!ping` - Responde imediatamente com o status da VPS e os próximos horários.
- `!status` - Exibe os próximos horários exatos de `m.roll`, `m.rroll` e `m.checkin`, e o total já enviado.
- `!roll` - Executa o ciclo de `m.roll` imediatamente.
- `!rroll` - Executa o ciclo de `m.rroll` imediatamente.
- `!checkin` - Executa o `m.checkin` imediatamente.
- `!grupos` - Lista todos os seus grupos e seus respectivos IDs (`@g.us`).
- `!ajuda` - Exibe o menu de ajuda.

---

## ☁️ Deploy 24/7 na VPS (Docker)

1. Clone o projeto na sua VPS:
   ```bash
   git clone https://github.com/yan-fab/whatsapp-reminder-bot.git
   cd whatsapp-reminder-bot
   cp .env.example .env
   nano .env # configure TARGET_CHAT e NOTIFY_PHONE
   ```

2. Suba com Docker:
   ```bash
   docker compose up -d
   ```

3. Escaneie o QR Code no terminal SSH:
   ```bash
   docker compose logs -f
   ```
   Aponte o WhatsApp do celular (**Aparelhos Conectados > Conectar um Aparelho**). Após conectar, pressione `Ctrl + C`.

---

## 📄 Licença
Distribuído sob a licença MIT.
