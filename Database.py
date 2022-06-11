import sqlite3
from sqlite3 import Error

from Hasher import Hasher

class Database():

    conn = sqlite3.connect('basa.bd')
    cursor = conn.cursor()
    inited = False

    @classmethod
    def check_init(cls):
        return cls.inited

    @classmethod
    def init(cls):

            cls.cursor.execute("""
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
            cls.cursor.execute("""
                CREATE TABLE IF NOT EXISTS bans(
                name TEXT,
                reason TEXT,
                unban_date DATE,
                ban_date DATE
                );
                """)
            cls.conn.commit()

            cls.cursor.execute("SELECT * FROM bans WHERE unban_date >= ban_date")
            buf = cls.cursor.fetchall()
            for i in buf:
                cls.cursor.execute(f"SELECT * FROM users WHERE name = '{i[0]}'")
                buf1 = cls.cursor.fetchall()
                if len(buf1) > 0:
                    print (buf1)
                    cls.cursor.execute("""
                                UPDATE users SET status = "ACTIVE"
                                WHERE name = '""" + buf1[0][0] + """'
                                """)
                    cls.cursor.execute("""
                                DELETE FROM bans
                                WHERE name = '""" + buf1[0][0] + """'
                                """)
            cls.cursor.execute("""
                UPDATE users SET rank = 0
                WHERE rank = 1
                """)
            cls.cursor.execute("""
                UPDATE users SET token = '0'
                """)

            cls.conn.commit()
            cls.inited = True

    @classmethod
    def new_user(cls, login, password):
        if cls.inited:
            cls.cursor.execute("""INSERT INTO users(name, password, rank, bal, status, token, reg_date)
                            VALUES('"""+ login + """', '"""+ Hasher.hash(password) + """', 0, 0, 'ACTIVE', '0', datetime(datetime())
                            """)
            cls.conn.commit()
            return True
        else:
            NOT_INITED()

    @classmethod
    def del_user(cls, login):
        if cls.inited:
            cls.cursor.execute("""
                DELETE FROM bans
                WHERE name = '""" + login + """'
                """)
            cls.conn.commit()
            return True
        else:
            NOT_INITED()

    @classmethod
    def find_with_name(cls, login):
        if cls.inited:
            cls.cursor.execute(f"SELECT * FROM users WHERE name = '{login}'")
            return cls.cursor.fetchall()
        else:
            NOT_INITED()

    @classmethod
    def ban_user(cls, login, reason, time):
        if cls.inited:
            cls.cursor.execute("""UPDATE users 
                    SET status = 'BANNED'
                    WHERE name = '""" + login + """' """)
            cls.cursor.execute(f"""INSERT INTO bans(name, reason, unban_date, ban_date)
                    VALUES('{login}', '{reason}', datetime(datetime(), '+{time} seconds'), datetime())
                    """)
            cls.conn.commit()
            return True
        else:
            NOT_INITED()

    @classmethod
    def set_token(cls, login, token):
        if cls.inited:
            cls.cursor.execute("""
                UPDATE users SET token = '""" + token + """'
                WHERE name = '""" + login + """'
                """)
            cls.conn.commit()
            return True
        else:
            NOT_INITED()

    @classmethod
    def clear_token(cls, login):
        if cls.inited:
            cls.cursor.execute("""
                    UPDATE users SET token = '0'
                    WHERE name = '""" + u[0] + """'
                    """)
            cls.conn.commit()
            return True
        else:
            NOT_INITED()
    
    @classmethod
    def find_with_token(cls, token):
        if cls.inited:
            cls.cursor.execute(f"SELECT * FROM users WHERE token = '{token}'")
            return cls.cursor.fetchall()
        else:
            NOT_INITED()

    @classmethod
    def check_name_password(cls, login, password):
        if cls.inited:
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}' and password = '{Hasher.hash(password)}'")
            buf = cursor.fetchall()
            if len(buf) > 0:
                return True
            else:
                return False
        else:
            NOT_INITED()



            
