from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from utils.database import Database
from respones.respones import send_welcome, send_main_menu

router = Router()
db = Database()

@router.message(CommandStart())
async def cmd_start(message: Message):
    
    if not await db.user_exists(message.from_user.id):
        await db.add_user(user_id=message.from_user.id, username=message.from_user.username)
    await send_welcome(message) 
    await send_main_menu(message)
