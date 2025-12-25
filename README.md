# Telegram Promo Watcher Bot

Este projeto monitora um canal público do Telegram em busca de promoções específicas (ex.: controle Xbox, notebooks, SSDs) e envia notificações via Pushover. O bot roda em Docker, usando Telethon, e utiliza um arquivo de sessão do Telegram para autenticação.

## Pré-requisitos

- Python 3.11+ instalado localmente.
- Docker e Docker Compose
- Conta no Telegram (para autenticar e gerar o arquivo de sessão) e token de API no Telegram para autenticar como usuário, não bot
  - `API_ID`
  - `API_HASH`
- Conta no Pushover (para notificações push)
  - `PUSHOVER_USER_KEY`
  - `PUSHOVER_API_TOKEN`
  
## Funcionalidades

- Monitoramento de mensagens em canal do Telegram.
- Filtros por palavras-chave, preço, porcentagem de desconto.
- Exclusão de termos indesejados (ex.: Gamer, Linux, Shopee, etc.).
- Envio de notificações via Pushover.
- Logs com rotacionamento.

## Preparação do ambiente

### 1. Copie `example.env` para `.env` e edite com suas credenciais

```text
PHONE=+0000000000000
API_ID=...
API_HASH=...
SESSION=anon
CHANNEL=https://t.me/seucanal
PUSHOVER_USER_KEY=...
PUSHOVER_API_TOKEN=...
TZ=...
```

### 2. Gere o arquivo de sessão (`anon.session`)

Antes de subir o container, é preciso autenticar sua conta Telegram localmente para gerar o arquivo de sessão do Telethon, para depois reutilizar no Docker. Por conta do 2FA, há prompts interativos durante a primeira execução, os quais não é possível responder na execução do container.

#### Criar o ambiente virtual (venv)

No diretório do projeto, crie e ative o venv:

```bash
python -m venv .tg-watcher
source .tg-watcher/bin/activate
```

#### Instalar as dependências

```bash
pip install -r requirements.txt
```

#### Rodar o script para gerar a sessão

```bash
python bot.py
```

Digite o código enviado pelo Telegram para um de seus dispositivos e, se necessário, a senha 2FA. Ao final, será criado um arquivo como `anon.session` na raiz do projeto.

#### Desative o venv quando terminar

```bash
deactivate
```

### 3. Para rodar via Docker Compose

```bash
docker-compose up --build -d
```

É recomendado montar um volume para persistência dos arquivos `.session` e de logs:

```yaml
volumes:
  - ./anon.session:/app/anon.session
  - ./logs/bot.log:/app/logs/bot.log
```

Edite o *bind* conforme desejado.

## Execução local (sem Docker)

Se quiser rodar o bot diretamente (por exemplo, para debug):

1. Ative o venv.
2. Garanta que o `.env` está configurado.
3. Execute:

```bash
python3 bot.py
```

### Logs

O bot é pouco verboso e costuma criar um evento de log para cada mensagem recebida. Cada condição cria um evento próprio. Em caso de problemas no código, o logging está configurado para capturar todos os tracebacks que venham a ocorrer. Entretanto o processo do bot não para de rodar, sendo possível mantê-lo funcionando em caso de problemas, mas sendo necessário consultar os logs para identificar o problema.

O arquivo `bot.log` será rotacionado diariamente, mantendo 5 arquivos antigos. Caso deseje alterar essa configuração, confira o `TimedRotatingFileHandler` no código `bot.py`.

## Personalização de Filtros

Os filtros (palavras-chave, blacklists, etc) podem ser ajustados no arquivo `bot.py`, conforme as suas necessidades.

## Exemplos de expressões regulares usadas

Alguns exemplos de regex utilizados neste projeto para filtrar promoções:

### Preços com ou sem centavos

Captura valores como `R$ 299` ou `R$ 299,99`:

```python
precos = re.findall(r"r$\s*([0-9]+(?:,[0-9]{2})?)", texto.lower())
```

### Porcentagens (ex.: 20% ou mais)

Extrai todos os números seguidos de `%` para depois filtrar em Python (ex.: ≥ 20):

```python
matches = re.findall(r"(\d+)\s*%", texto)
porcentagens = [int(n) for n in matches]
if porcentagens and max(porcentagens) >= 20:
# Pelo menos um desconto de 20% ou mais
```

### Capacidade 512 GB (com ou sem espaço)

Garante que “512 GB” ou “512GB” sejam detectados:

```python
tem_512 = re.search(r"\b512\s*gb\b", texto.lower()) is not None
```

### Combinação com outros filtros

Os regex normalmente são usados junto com checagens simples de substring:

```python
t = texto.lower()
eh_notebook_512 = "notebook" in t and re.search(r"\b512\s*gb\b", t)
tem_palavra_bloqueada = any(x in t for x in ["gamer", "linux", "keepos", "shopee"])
if eh_notebook_512 and not tem_palavra_bloqueada:
# Mensagem relevante para alerta
```

Esses exemplos podem ser adaptados conforme novos filtros forem adicionados (outros tamanhos, modelos, faixas de preço, etc.).

## Observações

- Proteja seu `.env` e `.session` (nunca commit em repo público).
- Se trocar de máquina/servidor, leve junto o arquivo `.session` para manter a mesma sessão.

## TO DO

- [ ] Monitorar multiplos canais.
- [ ] Disparo para mútiplos serviços de notificação, com opção de seleção para cada condição monitorada.
