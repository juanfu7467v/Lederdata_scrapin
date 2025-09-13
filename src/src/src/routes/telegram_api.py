from flask import Blueprint, jsonify, request
from telethon.sync import TelegramClient
from telethon.errors import RPCError
import os
import asyncio
from ..telegram_client import send_command_and_wait

telegram_bp = Blueprint('telegram_api', __name__)

@telegram_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"success": True, "message": "ok"})

@telegram_bp.route('/reniec/<dni>', methods=['GET'])
def reniec(dni):
    loop = asyncio.new_event_loop()
    try:
        result = loop.run_until_complete(send_command_and_wait(f"/ficha{dni}"))
        return jsonify({"success": True, "data": {"text": result}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        loop.close()

@telegram_bp.route('/defuncion/<dni>', methods=['GET'])
def defuncion(dni):
    loop = asyncio.new_event_loop()
    try:
        result = loop.run_until_complete(send_command_and_wait(f"/defuncion{dni}"))
        return jsonify({"success": True, "data": {"text": result}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        loop.close()

@telegram_bp.route('/command', methods=['POST'])
def custom_command():
    data = request.get_json() or {}
    cmd = data.get('command')
    if not cmd:
        return jsonify({"success": False, "error": "command required"}), 400
    loop = asyncio.new_event_loop()
    try:
        result = loop.run_until_complete(send_command_and_wait(cmd))
        return jsonify({"success": True, "data": {"text": result}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        loop.close()
