# ⏰ WhatsApp Reminder Bot (Web/Socket)

Bot de automação pessoal para envio de lembretes periódicos a cada **X horas** diretamente para o seu WhatsApp pessoal.

Construído em **Python** utilizando **Neonize** (uma engine nativa de WebSockets do WhatsApp Multi-Device baseada em `whatsmeow` do Go), consumindo apenas cerca de **~50MB de memória RAM** (sem navegadores pesados como Puppeteer/Chromium).

---

## ✨ Recursos

- ⚡ **Ultra-leve:** Consome apenas ~50MB de RAM, perfeito para rodar 24/7 em instâncias gratuitas da nuvem (Oracle Cloud Always Free).
- 🔄 **Conexão Direta por WebSocket:** Sem Chrome ou Selenium. Comunica diretamente com os servidores do WhatsApp.
- 📲 **Login Único por QR Code:** O QR Code é desenhado no terminal no primeiro acesso. Depois disso, a sessão fica salva em `session.sqlite3` e reconecta automaticamente.
- ⏱️ **Agendamento Flexível:** Configure o intervalo de horas (ou minutos para testes rápidos).
- 💬 **Comandos Interativos:** Se você responder ao bot no WhatsApp, ele reconhece comandos como:
  - `!status` - Mostra tempo ativo, último envio e próximo lembrete.
  - `!lembrete` - Dispara um lembrete manual teste imediatamente.
  - `!ajuda` - Lista os comandos disponíveis.

---

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
- Python 3.10 ou superior instalado.

### 2. Instalação das Dependências

Abra o terminal na pasta do projeto:

```bash
# Crie e ative o ambiente virtual (opcional, mas recomendado)
python -m venv .venv

# No Windows (PowerShell):
.\.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate

# Instale os pacotes:
pip install -r requirements.txt
```

### 3. Configuração do `.env`

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o `.env` com suas informações:

```env
# Seu número com DDI (55 para Brasil) + DDD + Telefone (apenas números)
TARGET_PHONE=5511999999999

# Intervalo em horas entre cada envio (ex: 2 para a cada 2 horas)
REMINDER_INTERVAL_HOURS=2

# Mensagem do lembrete (suporta formatação WhatsApp: *negrito*, _itálico_)
REMINDER_MESSAGE=🔔 *Lembrete Automático*\n\nHora de fazer uma pausa, beber água e revisar as tarefas! 🚀

# Enviar o primeiro lembrete assim que conectar? (true/false)
RUN_IMMEDIATELY=true
```

### 4. Executando o Bot

```bash
python bot.py
```

1. Na **primeira execução**, um QR Code será impresso no seu terminal.
2. No seu celular, abra o WhatsApp: **Configurações / Aparelhos Conectados > Conectar um Aparelho**.
3. Aponte a câmera para o QR Code no terminal.
4. Pronto! O bot confirmará a conexão e iniciará o cronômetro do lembrete.

---

## ☁️ Deploy 24/7 na Nuvem (VPS Grátis)

### Opção 1: Oracle Cloud Always Free (Recomendada)
A Oracle Cloud oferece instâncias gratuitas para sempre com 1GB a 24GB de RAM.

1. Crie uma VM com Ubuntu 22.04 / 24.04.
2. Clone seu repositório na VPS:
   ```bash
   git clone https://github.com/yan-fab/whatsapp-reminder-bot.git
   cd whatsapp-reminder-bot
   cp .env.example .env
   nano .env # preencha seus dados
   ```
3. Suba com Docker Compose:
   ```bash
   docker compose up -d
   ```
4. Veja os logs e escaneie o QR Code:
   ```bash
   docker compose logs -f
   ```

### Opção 2: Como Serviço no Linux (Systemd)
Se preferir rodar sem Docker na VPS:

1. Crie o serviço systemd:
   ```bash
   sudo nano /etc/systemd/system/whatsapp-bot.service
   ```
2. Adicione a configuração:
   ```ini
   [Unit]
   Description=WhatsApp Reminder Bot
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/whatsapp-reminder-bot
   ExecStart=/home/ubuntu/whatsapp-reminder-bot/.venv/bin/python bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```
3. Ative e inicie:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable whatsapp-bot
   sudo systemctl start whatsapp-bot
   ```

---

## 🛡️ Segurança & Boas Práticas

- **Uso Pessoal:** Este bot foi desenhado para enviar mensagens para o **seu próprio número**. O envio de mensagens para terceiros em massa sem consentimento pode levar a restrições no WhatsApp.
- **Sessão:** O arquivo `session.sqlite3` armazena as chaves de criptografia da sua sessão. Ele já está listado no `.gitignore` para nunca ser enviado ao GitHub.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.
