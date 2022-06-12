import sqlite3
from sqlite3 import Error

from Classes.Hasher import Hasher



class Database():

    inited = False

    @classmethod
    def check_init(cls):
        return cls.inited

    @classmethod
    def init(cls):
            conn = sqlite3.connect('basa.bd')
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                name TEXT,
                password TEXT,
                rank INTEGER,
                bal INTEGER,
                status TEXT,
                token TEXT,
                reg_date DATE
                );
                """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bans(
                name TEXT,
                reason TEXT,
                unban_date DATE,
                ban_date DATE
                );
                """)
            conn.commit()

            cursor.execute("SELECT * FROM bans WHERE unban_date >= ban_date")
            buf = cursor.fetchall()
            for i in buf:
                cursor.execute(f"SELECT * FROM users WHERE name = '{i[0]}'")
                buf1 = cursor.fetchall()
                if len(buf1) > 0:
                    print (buf1)
                    cursor.execute("""
                                UPDATE users SET status = "ACTIVE"
                                WHERE name = '""" + buf1[0][0] + """'
                                """)
                    cursor.execute("""
                                DELETE FROM bans
                                WHERE name = '""" + buf1[0][0] + """'
                                """)
            cursor.execute("""
                UPDATE users SET rank = 0
                WHERE rank = 1
                """)
            cursor.execute("""
                UPDATE users SET token = '0'
                """)

            conn.commit()
            cls.inited = True

    @classmethod
    def _new_user(cls, login, password):
        conn = sqlite3.connect('basa.bd')
        cursor = conn.cursor()
        if cls.inited:
            print (login, Hasher.hash(password))
            cursor.execute(f"""INSERT INTO users(name, password, rank, bal, status, token, reg_date)
                            VALUES('{login}', '{Hasher.hash(password)}', 0, 0, 'ACTIVE', '0', datetime(datetime()))""")
            conn.commit()
            return True
        else:
            NOT_INITED()

    @classmethod
    def _del_user(cls, login):
        conn = sqlite3.connect('basa.bd')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""
                DELETE FROM bans
                WHERE name = '""" + login + """'
                """)
            conn.commit()
            return True
        else:
            NOT_INITED()

    @classmethod
    def _find_with_name(cls, login):
        conn = sqlite3.connect('basa.bd')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}'")
            return cursor.fetchall()
        else:
            NOT_INITED()

    @classmethod
    def _ban_user(cls, login, reason, time):
        conn = sqlite3.connect('basa.bd')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""UPDATE users 
                    SET status = 'BANNED'
                    WHERE name = '""" + login + """' """)
            cursor.execute(f"""INSERT INTO bans(name, reason, unban_date, ban_date)
                    VALUES('{login}', '{reason}', datetime(datetime(), '+{time} seconds'), datetime())
                    """)
            conn.commit()
            return True
        else:
            NOT_INITED()

    @classmethod
    def _set_token(cls, login, token):
        conn = sqlite3.connect('basa.bd')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""
                UPDATE users SET token = '""" + token + """'
                WHERE name = '""" + login + """'
                """)
            conn.commit()
            return True
        else:
            NOT_INITED()

    @classmethod
    def _clear_token(cls, login):
        conn = sqlite3.connect('basa.bd')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute("""
                    UPDATE users SET token = '0'
                    WHERE name = '""" + u[0] + """'
                    """)
            conn.commit()
            return True
        else:
            NOT_INITED()
    
    @classmethod
    def _find_with_token(cls, token):
        conn = sqlite3.connect('basa.bd')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE token = '{token}'")
            return cursor.fetchall()
        else:
            NOT_INITED()

    @classmethod
    def _check_name_password(cls, login, password):
        conn = sqlite3.connect('basa.bd')
        cursor = conn.cursor()
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}' and password = '{Hasher.hash(password)}'")
            buf = cursor.fetchall()
            if len(buf) > 0:
                return True
            else:
                return False
        else:
            NOT_INITED()



            
