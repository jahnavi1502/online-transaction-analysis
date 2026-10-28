import mysql.connector
from config import Config
def get_connection():
    return mysql.connector.connect(**Config.DB_CONFIG)
def fetch_all(sql, params=()):
    conn=get_connection()
    try:
        cur=conn.cursor(dictionary=True); cur.execute(sql,params); return cur.fetchall()
    finally:
        cur.close(); conn.close()
def execute(sql, params=()):
    conn=get_connection(); cur=conn.cursor()
    try:
        cur.execute(sql,params); conn.commit(); return cur.lastrowid
    except Exception:
        conn.rollback(); raise
    finally:
        cur.close(); conn.close()
