from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from utils.database import Database

router = Router()
db = Database()

class AdminStates(StatesGroup):
    manage_items = State()
    add_item = State()
    edit_item_id = State()
    edit_item_data = State()
    delete_item = State()
    update_balance = State()
    manage_users = State()
    ban_unban_user = State()

@router.message(AdminStates.add_item)
async def add_item(message: Message, state: FSMContext):
    try:
        name, description, price, count = map(str.strip, message.text.split("|"))
        price, count = int(price), int(count)
        await db.add_item(name, price, description, count)
        await message.answer(f"✅ Товар '{name}' успешно добавлен!")
        await state.clear()
    except ValueError:
        await message.answer("❌ Неверный формат данных. Попробуйте снова.")

@router.message(AdminStates.edit_item_id)
async def edit_item_id(message: Message, state: FSMContext):
    try:
        item_id = int(message.text)
        item = await db.get_item_by_id(item_id)
        if item:
            await message.answer(f"Введите новые данные для товара '{item[1]}' в формате:\n\n<code>Название | Описание | Цена | Количество</code>", parse_mode="HTML")
            await state.update_data(item_id=item_id)
            await state.set_state(AdminStates.edit_item_data)
        else:
            await message.answer("❌ Товар с таким ID не найден.")
    except ValueError:
        await message.answer("❌ ID должен быть числом.")

@router.message(AdminStates.edit_item_data)
async def edit_item_data(message: Message, state: FSMContext):
    try:
        data = message.text.strip()
        item_id = (await state.get_data()).get("item_id")
        name, description, price, count = map(str.strip, data.split("|"))
        price, count = int(price), int(count)
        await db.update_item_name_and_description(item_id, name, description)
        await db.update_item_count(item_id, count)
        await message.answer(f"✅ Товар с ID {item_id} успешно обновлён!")
        await state.clear()
    except ValueError:
        await message.answer("❌ Неверный формат данных. Попробуйте снова.")

@router.message(AdminStates.delete_item)
async def delete_item_by_id(message: Message, state: FSMContext):
    try:
        item_id = int(message.text)
        await db.delete_item_by_id(item_id)
        await message.answer(f"✅ Товар с ID {item_id} успешно удалён!")
        await state.clear()
    except ValueError:
        await message.answer("❌ ID должен быть числом.")

@router.message(AdminStates.update_balance)
async def update_user_balance(message: Message, state: FSMContext):
    try:
        user_id, amount = map(str.strip, message.text.split("|"))
        user_id, amount = int(user_id), float(amount)
        await db.update_balance(user_id, amount)
        await message.answer(f"✅ Баланс пользователя с ID {user_id} успешно изменён на {amount} ₽.")
        await state.clear()
    except ValueError:
        await message.answer("❌ Неверный формат данных. Попробуйте снова.")

@router.message(AdminStates.ban_unban_user)
async def manage_user_block(message: Message, state: FSMContext):
    try:
        user_id, action = map(str.strip, message.text.split("|"))
        user_id = int(user_id)
        if action.lower() == "бан":
            await db.block_user(user_id)
            await message.answer(f"✅ Пользователь с ID {user_id} успешно заблокирован.")
            await state.clear()
        elif action.lower() == "разбан":
            await db.unblock_user(user_id)
            await message.answer(f"✅ Пользователь с ID {user_id} успешно разблокирован.")
            await state.clear()
        else:
            await message.answer("❌ Действие должно быть 'бан' или 'разбан'.")
    except ValueError:
        await message.answer("❌ Неверный формат данных. Попробуйте снова.")