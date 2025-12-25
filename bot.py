import os
import re
import requests
from telethon import TelegramClient, events
import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import traceback

PHONE = os.environ.get("PHONE")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION", "anon")
CHANNEL = os.environ.get("CHANNEL", "https://t.me/promotop")
PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.environ.get("PUSHOVER_API_TOKEN")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    "./logs/bot.log",
    when="midnight",
    backupCount=5
)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

def excecao_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = excecao_handler

def enviar_notificacao(mensagem, link):
    url = "https://api.pushover.net/1/messages.json"
    dados = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": mensagem,
        "title": "Promoção encontrada",
        "url": link,
        "url_title": "Ver no canal",
        "priority": 1,
        "sound": "cashregister",
    }
    resposta = requests.post(url, data=dados)
    return resposta.status_code == 200

client = TelegramClient(SESSION, API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNEL))
async def handler(event):
    texto = event.raw_text.lower()
    # if "controle" in texto and "xbox" in texto:
    #     precos = re.findall(r"r\$\s*([0-9]+(?:,[0-9]{2})?)", texto)
    #     precos_float = []
    #     for p in precos:
    #         p = p.replace(",", ".")  # transformar vírgula em ponto para float
    #         try:
    #             precos_float.append(float(p))
    #         except ValueError:
    #             continue
    #     if precos_float and min(precos_float) < 300:
    #         username = "promotop"
    #         message_id = event.id
    #         link = f"https://t.me/{username}/{message_id}"
    #         logging.info("Oferta Controle Xbox encontrada! Enviando notificacao...")
    #         enviar_notificacao("Controle Xbox:", link)

    if "LG" in texto and "ultragear" in texto and "UltraWide" in texto:
        precos = re.findall(r"r\$\s*([0-9]+(?:,[0-9]{2})?)", texto)
        precos_float = []
        for p in precos:
            p = p.replace(",", ".")  # transformar vírgula em ponto para float
            try:
                precos_float.append(float(p))
            except ValueError:
                continue
        if precos_float and min(precos_float) < 1600:
            username = "promotop"
            message_id = event.id
            link = f"https://t.me/{username}/{message_id}"
            logging.info("Oferta Monitor! Enviando notificacao...")
            enviar_notificacao("Monitor LG UltraGear:", link)

    if "JBL" in texto and "SB580" in texto:
        username = "promotop"
        message_id = event.id
        link = f"https://t.me/{username}/{message_id}"
        logging.info("Oferta Soundbar encontrada! Enviando notificacao...")
        enviar_notificacao("Soundbar JBL:", link)

    if "cupom" in texto and "livre" in texto:
        matches = re.findall(r"(\d+)\s*%", texto)
        porcentagens = [int(n) for n in matches]
        if porcentagens and max(porcentagens) >= 20:
            username = "promotop"
            message_id = event.id
            link = f"https://t.me/{username}/{message_id}"
            logging.info("Cupom Mercado Livre encontrado! Enviando notificacao...")
            enviar_notificacao("Cupom Mercado Livre:", link)

    if "cupom" in texto and "amazon" in texto:
        username = "promotop"
        message_id = event.id
        link = f"https://t.me/{username}/{message_id}"
        logging.info("Cupom Amazon encontrado! Enviando notificacao...")
        enviar_notificacao("Cupom Amazon:", link)

    if "cupom" in texto and "kabum" in texto:
        username = "promotop"
        message_id = event.id
        link = f"https://t.me/{username}/{message_id}"
        logging.info("Cupom KaBuM encontrado! Enviando notificacao...")
        enviar_notificacao("Cupom KaBuM:", link)

    if "iPhone 16e" in texto and not "shopee" in texto:
        precos = re.findall(r"r\$\s*([0-9]+(?:,[0-9]{2})?)", texto)
        precos_float = []
        for p in precos:
            p = p.replace(",", ".")  # transformar vírgula em ponto para float
            try:
                precos_float.append(float(p))
            except ValueError:
                continue
        if precos_float and min(precos_float) < 3100:
            username = "promotop"
            message_id = event.id
            link = f"https://t.me/{username}/{message_id}"
            logging.info("Oferta iPhone 16e! Enviando notificacao...")
            enviar_notificacao("iPhone 16e:", link)

    if "iPhone 16 " in texto and "128" in texto and not "iPhone 16 Pro" in texto and not "shopee" in texto:
        precos = re.findall(r"r\$\s*([0-9]+(?:,[0-9]{2})?)", texto)
        precos_float = []
        for p in precos:
            p = p.replace(",", ".")  # transformar vírgula em ponto para float
            try:
                precos_float.append(float(p))
            except ValueError:
                continue
        if precos_float and min(precos_float) < 4100:
            username = "promotop"
            message_id = event.id
            link = f"https://t.me/{username}/{message_id}"
            logging.info("Oferta iPhone 16! Enviando notificacao...")
            enviar_notificacao("iPhone 16:", link)

    if "NVME" in texto and re.findall(r"\b(1\s*TB|2\s*TB|NV3)\b", texto, flags=re.IGNORECASE) and not "shopee" in texto:
        username = "promotop"
        message_id = event.id
        link = f"https://t.me/{username}/{message_id}"
        logging.info("Oferta NVMe encontrada! Enviando notificacao...")
        enviar_notificacao("SSD NVMe:", link)

    passou, win_flag = verifica_notebook_oferta(texto)
    if passou:
        username = "promotop"
        message_id = event.id
        link = f"https://t.me/{username}/{message_id}"
        logging.info("Oferta Notebook encontrada! Enviando notificacao...")
        enviar_notificacao("Oferta Notebook:", link)

def verifica_notebook_oferta(texto):
    t = texto
    inclui_notebook = 'notebook' in t
    inclui_512gb = re.search(r'\b512\s*gb\b', t)  # aceita com ou sem espaço(s) entre 512 e gb
    exclui = any(x in t for x in ['gamer', 'predator', 'linux', 'keepos', 'shopee'])
    win_flag = any(w in t for w in ['windows 11', 'win 11', 'w11'])
    return inclui_notebook and inclui_512gb and not exclui, win_flag

client.start(phone=PHONE)
logging.info("Bot iniciado. Aguardando mensagens...")
client.run_until_disconnected()