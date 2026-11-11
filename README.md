# 🌸 WhatsApp Waifus Auto-Bot (Madotsu 5 / RolêSP)

Bot de automação pessoal via **WebSockets direto** (sem navegador pesado, consumindo apenas ~50MB de RAM) para envio automático dos comandos periódicos do sistema de Waifus do **Bot Madotsu 5 diretamente no PRIVADO do bot**, com **trava de segurança contra envio em grupos** e **pings automáticos para o seu número pessoal**.

---

## 🔒 Trava de Segurança: Grupos 100% Bloqueados

Para evitar qualquer risco de spam, flood ou penalidades no **grupo principal da comunidade**:
- Todos os comandos (`m.roll`, `m.rroll`, `m.checkin`) são enviados **estritamente para o número privado do Bot Madotsu** (`MADOTSU_PHONE`).
- O código possui uma **trava rígida** que impede qualquer envio para identificadores de grupo (`@g.us`). Se alguém tentar configurar um grupo, o bot recusa a inicialização por segurança.

---

## 🔔 Pings e Avisos no seu WhatsApp Pessoal

Sempre que o bot disparar uma rotina no privado do Madotsu, ele envia automaticamente um resumo para o seu número pessoal (`NOTIFY_PHONE`):
- 🎲 **Quando rola `m.roll`:** Envia aviso com quantidade de rolls enviados no privado, horário e data/hora do próximo ciclo.
- 💎 **Quando rola `m.rroll`:** Envia confirmação dos rolls de alta taxa.
- 📅 **Quando envia `m.checkin`:** Avisa que sua streak diária foi mantida.
- 🟢 **Quando o bot liga na VPS:** Envia ping avisando que está online e operando.

---

## 📋 Tabela de Comandos e Intervalos (Conforme o Guia)

| Comando | Destino | Quantidade / Intervalo | Modo VIP | Função |
| :--- | :--- | :--- | :--- | :--- |
| `m.roll` | **Privado do Madotsu** | **5 rolls a cada 2 horas** | **9 rolls a cada 2 horas** | Rola personagem aleatório comum, rara, épica, lendária e mítica. |
| `m.rroll` | **Privado do Madotsu** | **5 rolls a cada 12 horas** | *(igual)* | Rola com taxas aumentadas para raridades raras ou superiores. |
| `m.checkin` | **Privado do Madotsu** | **1 vez a cada 24 horas** | *(2 dias de tolerância)* | Mantém a sequência (*streak*) diária no perfil. |

---

## 🛡️ Anti-Flood & Simulação Humana
- Aguarda um **delay aleatório humanizado** (entre 3 e 6 segundos) entre cada `m.roll` e `m.rroll`.
- Desconecta de forma segura e reconecta automaticamente se a rede da VPS oscilar.

---

## 🚀 Configuração do `.env`

No arquivo `.env`:

```env
# 1. Número PRIVADO do bot Madotsu (apenas números, DDI + DDD + Telefone):
MADOTSU_PHONE=5511999999999

# 2. Seu número pessoal para receber os Pings e Avisos a cada disparo:
NOTIFY_PHONE=5511988887777
ENABLE_NOTIFY=true

# 3. Assinatura VIP no Madotsu (true: 9 rolls | false: 5 rolls):
IS_VIP=false
```

---

## 💬 Comandos Interativos no WhatsApp

Você pode enviar comandos para o bot pelo próprio WhatsApp:
- `!ping` - Responde imediatamente com o status da VPS e os próximos horários.
- `!status` - Exibe os próximos horários exatos de `m.roll`, `m.rroll` e `m.checkin`, e o total já enviado.
- `!roll` - Executa o ciclo de `m.roll` imediatamente no privado do Madotsu.
- `!rroll` - Executa o ciclo de `m.rroll` imediatamente no privado do Madotsu.
- `!checkin` - Executa o `m.checkin` imediatamente no privado do Madotsu.
- `!ajuda` - Exibe o menu de ajuda.

---

## ☁️ Deploy 24/7 na VPS (Docker)

1. Clone o projeto na sua VPS:
   ```bash
   git clone https://github.com/yan-fab/whatsapp-reminder-bot.git
   cd whatsapp-reminder-bot
   cp .env.example .env
   nano .env # configure MADOTSU_PHONE e NOTIFY_PHONE
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
