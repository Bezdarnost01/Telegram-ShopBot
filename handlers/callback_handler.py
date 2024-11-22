from aiogram import Router
from aiogram.types import CallbackQuery
from utils.database import Database
from aiogram import F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from handlers.query_handler import AdminStates
from respones.respones import (send_main_menu_call, send_profile_page, send_items_list, 
                               send_item_details, buy_item, send_admin_menu_call, send_items_management_menu,
                               send_balance_management_form, send_user_management_form, send_user_list,
                               send_items_list_admin)

router = Router()
db = Database()

@router.callback_query(F.data == 'back_to_main')
async def back_to_main_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await send_main_menu_call(callback)
    await state.clear()

@router.callback_query(F.data == 'hide')
async def profile_message(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()

@router.callback_query(F.data == 'profile')
async def profile_message(callback: CallbackQuery):
    await callback.message.delete()
    await send_profile_page(callback)

@router.callback_query(lambda c: c.data.startswith("items_page_"))
async def paginate_items(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    await callback.answer()
    await send_items_list(callback, page=page)

@router.callback_query(lambda c: c.data == "items_list")
async def show_items(callback: CallbackQuery):
    await callback.answer()
    await send_items_list(callback, page=1)

@router.callback_query(lambda c: c.data.startswith("item_"))
async def item_details_handler(callback: CallbackQuery):
    await callback.answer()
    await send_item_details(callback)

@router.callback_query(lambda c: c.data.startswith("buy_"))
async def buy_item_handler(callback: CallbackQuery):
    await callback.answer()
    await buy_item(callback)

@router.callback_query(lambda c: c.data == "admin_menu")
async def admin_menu_handler(callback: CallbackQuery):
    await callback.message.delete()
    await send_admin_menu_call(callback)

@router.callback_query(lambda c: c.data == "show_user_list")
async def admin_menu_handler(callback: CallbackQuery):
    await callback.answer()
    await send_user_list(callback)

@router.callback_query(lambda c: c.data == "show_items_list_admin")
async def admin_menu_handler(callback: CallbackQuery):
    await callback.answer()
    await send_items_list_admin(callback)

@router.callback_query(F.data == "add_item")
async def add_item_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите данные для добавления товара в формате:\n\n<code>Название | Описание | Цена | Данные | Количество</code>", parse_mode="HTML")
    await state.set_state(AdminStates.add_item)

@router.callback_query(F.data == "edit_item")
async def edit_item_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ID товара, который хотите изменить:")
    await state.set_state(AdminStates.edit_item_id)

@router.callback_query(F.data == "delete_item")
async def delete_item_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ID товара, который хотите удалить:")
    await state.set_state(AdminStates.delete_item)

@router.callback_query(lambda c: c.data == "manage_items")
async def manage_items_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await send_items_management_menu(callback)
    await state.set_state(AdminStates.manage_items)

@router.callback_query(lambda c: c.data == "manage_balance")
async def manage_balance_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await send_balance_management_form(callback)
    await state.set_state(AdminStates.update_balance)

@router.callback_query(lambda c: c.data == "manage_users")
async def manage_users_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await send_user_management_form(callback)
    await state.set_state(AdminStates.ban_unban_user)