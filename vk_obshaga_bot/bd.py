import sqlite3


admins = ['220588777']
zav = []

class DB:
    def __init__(self):
        conn = sqlite3.connect('user.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UserModel:
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     role VARCHAR(50),
                                     user_name VARCHAR(50),
                                     obshaga_number INT(10),
                                     date VARCHAR(50),
                                     vk_id VARCHAR(50),
                                     duty VARCHAR(50),
                                     last_action INT(10)
                                     )''')
        cursor.close()
        self.connection.commit()

    def insert(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (vk_id, last_action, role) 
                          VALUES (?,?,?)''', (id, 0, 1 if id in admins else 2 if id in zav else 0))
        cursor.close()
        self.connection.commit()

    def set_name(self, vk_id, user_name):
        cursor = self.connection.cursor()
        print(user_name, vk_id)
        cursor.execute('''
            UPDATE users
                SET user_name = ?
            WHERE vk_id = ?;
        ''', (user_name, vk_id))
        self.connection.commit()
        cursor.close()

        cursor = self.connection.cursor()
        cursor.execute(''' UPDATE users
                SET last_action = 1
            WHERE vk_id = ?;
        ''', (vk_id,))
        cursor.close()
        self.connection.commit()

    def set_obshaga(self, vk_id, num):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE users
                SET last_action = 2, obshaga_number = ?
            WHERE vk_id = ?;
        ''', (num, vk_id))
        cursor.close()
        self.connection.commit()

    def set_date(self, vk_id, date):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE users
                SET last_action = 3, date = ?
            WHERE vk_id = ?;
        ''', (date, vk_id))
        cursor.close()
        self.connection.commit()

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(user_id)))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_vkid(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE vk_id = ?", (id,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, rfid):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE rfid = ?", (rfid))
        except Exception as e:
            print(e)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def edit(self, user_id, user_name):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE users
                SET user_name = ?
            WHERE id = ?;
        ''', (user_name, user_id))
        cursor.close()
        self.connection.commit()

    def set_duty(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE users SET duty = 0 WHERE id = ?;
        """, (user_id,))
        cursor.close()
        self.connection.commit()
