import json
import os
from math import ceil

from aiogram import types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from utils.database import Database

db = Database()
with open(os.path.join("config", "config.json"), "r", encoding="utf-8") as settings_file:
    settings = json.load(settings_file)

async def send_welcome(message: Message):
    text = (f"👋 Привет, {message.from_user.first_name}!\n\n"
                  "🔥 Добро пожаловать в GreenMarket.\n")
    await message.answer(text)

async def send_main_menu(message: Message):
    text = ("Добро пожаловать в главное меню:")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
            [InlineKeyboardButton(text="📂 Список товаров", callback_data="items_list")]
        ])
    
    await message.answer(text, reply_markup=keyboard)

async def send_main_menu_call(callback: CallbackQuery):
    text = ("Добро пожаловать в главное меню:")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
            [InlineKeyboardButton(text="📂 Список товаров", callback_data="items_list")]
        ])
    
    await callback.message.answer(text, reply_markup=keyboard)

async def send_profile_page(callback: CallbackQuery):
    user = await db.get_user_info(callback.from_user.id)
    if user:
        text = (
            f"👋 Привет, {callback.from_user.first_name}\n\n"
            f"👤 Ваш ID: <code>{user[1]}</code>\n"
            f"💳 Баланс: <code>{user[3]:.2f}</code> ₽\n\n"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚪 Назад", callback_data="back_to_main")]
        ])
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await callback.message.answer("Профиль не найден. Попробуйте снова.")

async def send_items_list(callback: CallbackQuery, page: int = 1):
    items_per_page = 10
    offset = (page - 1) * items_per_page
    all_items = await db.get_all_items()

    if not all_items:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Скрыть", callback_data="hide")]
        ])
        await callback.answer()
        await callback.message.answer("📂 Товары отсутствуют.", reply_markup=keyboard)
        return

    total_pages = ceil(len(all_items) / items_per_page)
    items_on_page = all_items[offset:offset + items_per_page]

    text = "📂 Список товаров:\n\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for item_id, name, price in items_on_page:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"{name} — {price} ₽", callback_data=f"item_{item_id}")])

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"items_page_{page - 1}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"items_page_{page + 1}"))

    if navigation_buttons:
        keyboard.inline_keyboard.append(navigation_buttons)

    keyboard.inline_keyboard.append([InlineKeyboardButton(text="🚪 Назад", callback_data="back_to_main")])

    await callback.message.answer(text, reply_markup=keyboard)

async def send_items_list_admin(callback: types.CallbackQuery, page: int = 1):
    items_per_page = 10
    offset = (page - 1) * items_per_page
    all_items = await db.get_all_items_admin()

    if not all_items:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Скрыть", callback_data="hide")]
        ])
        await callback.answer()
        await callback.message.answer("📂 Товары отсутствуют.", reply_markup=keyboard)
        return

    total_pages = ceil(len(all_items) / items_per_page)
    items_on_page = all_items[offset:offset + items_per_page]

    text = "📂 Список товаров:\n\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for item_id, name, price, count in items_on_page:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"{item_id} - {name} - {price} ₽ - {count} шт.",
                                                              callback_data=f"item_{item_id}")])

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"items_page_{page - 1}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"items_page_{page + 1}"))

    if navigation_buttons:
        keyboard.inline_keyboard.append(navigation_buttons)

    keyboard.inline_keyboard.append([InlineKeyboardButton(text="🗑 Скрыть", callback_data="hide")])

    await callback.message.answer(text, reply_markup=keyboard)

async def send_user_list(callback: types.CallbackQuery, page: int = 1):
    items_per_page = 10
    offset = (page - 1) * items_per_page
    all_users = await db.get_all_users()

    if not all_users:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Скрыть", callback_data="hide")]
        ])
        await callback.answer()
        await callback.message.answer("📂 Пользователи отсутствуют.", reply_markup=keyboard)
        return

    total_pages = ceil(len(all_users) / items_per_page)
    users_on_page = all_users[offset:offset + items_per_page]

    text = "📂 Список пользователей:\n\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for user_id, username, balance, is_blocked in users_on_page:
        status = "Заблокирован" if is_blocked == 'True' else "Не заблокирован"
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"{username} - {user_id} - {balance} ₽ - {status}",
                                                              callback_data=f"user_{user_id}")])

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"users_page_{page - 1}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"users_page_{page + 1}"))

    if navigation_buttons:
        keyboard.inline_keyboard.append(navigation_buttons)

    keyboard.inline_keyboard.append([InlineKeyboardButton(text="🗑 Скрыть", callback_data="hide")])

    await callback.message.answer(text, reply_markup=keyboard)

async def send_item_details(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    item = await db.get_item_by_id(item_id)

    if not item:
        await callback.message.answer("❌ Товар не найден.")
        return

    item_id, name, price, description, data, count = item

    text = (
        f"📦 <b>{name}</b>\n\n"
        f"💵 Цена: <code>{price}</code> ₽\n"
        f"📄 Описание:\n{description}\n"
        f"📋 В наличии: <code>{count}</code>\n"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Купить", callback_data=f"buy_{item_id}")],
        [InlineKeyboardButton(text="🚪 Назад", callback_data="items_list")]
    ])
    await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")


async def buy_item(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[1])

    item = await db.get_item_by_id(item_id)
    if not item:
        await callback.message.answer("❌ Товар не найден.")
        return

    item_id, name, price, description, data, count = item

    if count <= 0:
        await callback.message.answer("❌ Этот товар больше недоступен.")
        return

    user_id = callback.from_user.id
    user_balance = await db.get_balance(user_id)

    if user_balance < price:
        await callback.message.answer("❌ Недостаточно средств для покупки этого товара.")
        return
    
    await db.deduct_balance(user_id, price)
    await db.update_item_count(item_id, count - 1)

    await callback.message.answer(f"✅ Вы успешно купили <b>{name}</b> за <code>{price}</code> ₽!\n\nВот ваши данные: <code>{data}</code>", parse_mode="HTML")

async def send_admin_menu(message: Message):
    text = "🔧 <b>Админ меню</b>\n\nВыберите действие:"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Список пользователей", callback_data="show_user_list")],
        [InlineKeyboardButton(text="📦 Управление товарами", callback_data="manage_items")],
        [InlineKeyboardButton(text="💰 Управление балансом", callback_data="manage_balance")],
        [InlineKeyboardButton(text="🚫 Бан/Разбан пользователей", callback_data="manage_users")],
        [InlineKeyboardButton(text="🚪 Назад", callback_data="back_to_main")]
    ])
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

async def send_admin_menu_call(callback: CallbackQuery):
    text = "🔧 <b>Админ меню</b>\n\nВыберите действие:"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Список пользователей", callback_data="show_user_list")],
        [InlineKeyboardButton(text="📦 Управление товарами", callback_data="manage_items")],
        [InlineKeyboardButton(text="💰 Управление балансом", callback_data="manage_balance")],
        [InlineKeyboardButton(text="🚫 Бан/Разбан пользователей", callback_data="manage_users")],
        [InlineKeyboardButton(text="🚪 Назад", callback_data="back_to_main")]
    ])
    await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

async def send_items_management_menu(callback: CallbackQuery):
    text = "📦 <b>Управление товарами</b>\n\nВыберите действие:"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить товар", callback_data="add_item")],
        [InlineKeyboardButton(text="✏️ Изменить товар", callback_data="edit_item")],
        [InlineKeyboardButton(text="❌ Удалить товар", callback_data="delete_item")],
        [InlineKeyboardButton(text="📄 Список товаров", callback_data="show_items_list_admin")],
        [InlineKeyboardButton(text="🚪 Назад", callback_data="admin_menu")]
    ])
    await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

async def send_balance_management_form(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Скрыть", callback_data="hide")]
        ])
    await callback.message.answer("Введите данные для изменения баланса пользователя в формате:\n\n<code>ID | Сумма</code>", 
                                  parse_mode="HTML", reply_markup=keyboard)

async def send_user_management_form(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Скрыть", callback_data="hide")]
        ])
    await callback.message.answer("Введите данные для блокировки/разблокировки пользователя в формате:\n\n<code>ID | Действие (бан/разбан)</code>", 
                                  parse_mode="HTML", reply_markup=keyboard)