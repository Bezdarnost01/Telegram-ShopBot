import json
import os

from aiogram import types
from aiogram import F
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from respones.respones import send_admin_menu
from utils.database import Database

db = Database()
router = Router()

with open(os.path.join("config", "config.json"), "r", encoding="utf-8") as settings_file:
    settings = json.load(settings_file)

@router.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    if await db.is_user_blocked(user_id):
        await message.answer("❌ Ваш аккаунт заблокирован. Вы не можете отправлять сообщения.")
        return
    
    if message.text == "админ":
        if message.from_user.id in settings['admin_list']:
            await send_admin_menu(message)
