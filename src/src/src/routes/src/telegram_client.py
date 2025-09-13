import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, RPCError

API_ID = int(os.environ.get("TELEGRAM_API_ID", "0"))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
PHONE = os.environ.get("TELEGRAM_PHONE_NUMBER", "")
BOT_USERNAME = os.environ.get("TARGET_BOT", "@LEDERDATA_OFC_BOT")
SESSION_FILE = os.environ.get("TELETHON_SESSION", "telethon.session")

# Timeout settings
DEFAULT_TIMEOUT = int(os.environ.get("TELEGRAM_TIMEOUT", 20))

async def send_command_and_wait(command, timeout=DEFAULT_TIMEOUT):
    """
    Envia un comando al bot y espera la respuesta más reciente.
    Devuelve el texto del mensaje de respuesta (conciso).
    """
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.start(phone=PHONE)
    try:
        # envia el comando direct to bot (mejor usar username)
        entity = await client.get_entity(BOT_USERNAME)
        await client.send_message(entity, command)
        # esperar por la próxima respuesta del bot (timeout configurable)
        @client.on(events.NewMessage(from_users=entity))
        async def handler(event):
            # guarda el texto y desconecta
            handler.msg = event.message.message
            await client.disconnect()

        # run until disconnected or timeout
        try:
            await client.run_until_disconnected(timeout=timeout)
        except TypeError:
            # some telethon versions don't accept timeout param for run_until_disconnected
            await asyncio.sleep(timeout)
            await client.disconnect()

        # return captured message
        return getattr(handler, 'msg', '')
    finally:
        if client.is_connected():
            await client.disconnect()
