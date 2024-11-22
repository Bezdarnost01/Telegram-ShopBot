import aiosqlite
import os

class Database:
    def __init__(self, db_user_path='data/data.db'):
        os.makedirs(os.path.dirname(db_user_path), exist_ok=True)
        self.db_user_path = db_user_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_user_path) as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    username TEXT,
                    balance REAL DEFAULT 0.0,
                    is_blocked TEXT DEFAULT False
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price INTEGER,
                    description TEXT,
                    data TEXT,
                    count INTEGER
                )
            ''')
            await conn.commit()

    async def add_user(self, user_id, username=None):
        async with aiosqlite.connect(self.db_user_path) as conn:
            await conn.execute('''
                INSERT OR IGNORE INTO users (user_id, username)
                VALUES (?, ?)
            ''', (user_id, username))

            await conn.commit()
            
    async def get_user_info(self, user_id):
        async with aiosqlite.connect(self.db_user_path) as conn:
            async with conn.execute('SELECT id, user_id, username, balance FROM users WHERE user_id = ?', (user_id,)) as cursor:
                user = await cursor.fetchone()
                if user:
                    id, user_id, username, balance = user
                    return id, user_id, username, balance
                else:
                    return None
                
    async def user_exists(self, user_id):
        async with aiosqlite.connect(self.db_user_path) as conn:
            async with conn.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,)) as cursor:
                return await cursor.fetchone() is not None

    async def block_user(self, user_id):
        async with aiosqlite.connect(self.db_user_path) as conn:
            await conn.execute('''
                INSERT OR REPLACE INTO users (user_id, username, balance, is_blocked)
                VALUES (?, (SELECT username FROM users WHERE user_id = ?), 0.0, True)
            ''', (user_id, user_id))

            await conn.execute('''
                UPDATE users
                SET balance = 0.0, is_blocked = True
                WHERE user_id = ?
            ''', (user_id,))
            await conn.commit()

    async def unblock_user(self, user_id):
        async with aiosqlite.connect(self.db_user_path) as conn:
            await conn.execute('''
                INSERT OR REPLACE INTO users (user_id, username, balance, is_blocked)
                VALUES (?, (SELECT username FROM users WHERE user_id = ?), 0.0, False)
            ''', (user_id, user_id))

            await conn.execute('''
                UPDATE users
                SET balance = 0.0, is_blocked = False
                WHERE user_id = ?
            ''', (user_id,))
            await conn.commit()

    async def is_user_blocked(self, user_id):
        async with aiosqlite.connect(self.db_user_path) as conn:
            cursor = await conn.execute("SELECT is_blocked FROM users WHERE user_id = ?", (user_id,))
            result = await cursor.fetchone()
            return result[0] == 'True' if result else False

    async def get_all_users(self):
        async with aiosqlite.connect(self.db_user_path) as conn:
            cursor = await conn.execute("SELECT user_id, username, balance, is_blocked FROM users")
            return await cursor.fetchall()

    async def get_balance(self, user_id):
        async with aiosqlite.connect(self.db_user_path) as conn:
            async with conn.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0.0
            
    async def update_balance(self, user_id, new_balance):
        async with aiosqlite.connect(self.db_user_path) as conn:
            await conn.execute('''
                UPDATE users
                SET balance = ?
                WHERE user_id = ?
            ''', (new_balance, user_id))
            await conn.commit()

    async def deduct_balance(self, user_id, amount):
        current_balance = await self.get_balance(user_id)
        if current_balance >= amount:
            await self.update_balance(user_id, current_balance - amount)
            return True
        return False
    
    async def add_item(self, name, price, description, data, count=0):
        async with aiosqlite.connect(self.db_user_path) as conn:
            await conn.execute('''
                INSERT OR IGNORE INTO items (name, price, description, data, count)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, price, description, data, count))

            await conn.commit()

    async def get_all_items(self):
        async with aiosqlite.connect(self.db_user_path) as conn:
            cursor = await conn.execute("SELECT id, name, price FROM items")
            return await cursor.fetchall()
        
    async def get_all_items_admin(self):
        async with aiosqlite.connect(self.db_user_path) as conn:
            cursor = await conn.execute("SELECT id, name, price, count FROM items")
            return await cursor.fetchall()

    async def get_all_item_ids_and_names(self):
        async with aiosqlite.connect(self.db_user_path) as conn:
            cursor = await conn.execute("SELECT id, name FROM items")
            return await cursor.fetchall()

    async def get_item_by_id(self, item_id):
        async with aiosqlite.connect(self.db_user_path) as conn:
            cursor = await conn.execute("SELECT * FROM items WHERE id = ?", (item_id,))
            return await cursor.fetchone()
        
    async def update_item_name_and_description(self, item_id, new_name, new_description):
        async with aiosqlite.connect(self.db_user_path) as conn:
            await conn.execute('''
                UPDATE items
                SET name = ?, description = ?
                WHERE id = ?
            ''', (new_name, new_description, item_id))
            await conn.commit()

    async def update_item(self, item_id, new_name, new_description, new_price, new_count):
        async with aiosqlite.connect(self.db_user_path) as conn:
            await conn.execute('''
                UPDATE items
                SET name = ?, description = ?, price = ?, count = ?
                WHERE id = ?
            ''', (new_name, new_description, new_price, new_count, item_id))
            await conn.commit()

    async def delete_item_by_id(self, item_id):
        async with aiosqlite.connect(self.db_user_path) as conn:
            await conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
            await conn.commit()

    async def update_item_count(self, item_id, new_count):
        async with aiosqlite.connect(self.db_user_path) as conn:
            if new_count <= 0:
                await conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
            else:
                await conn.execute('''
                    UPDATE items
                    SET count = ?
                    WHERE id = ?
                ''', (new_count, item_id))
            await conn.commit()