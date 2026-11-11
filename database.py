import sqlite3

DB_NAME = "trading_data.db"

def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        buy_price REAL,
        sell_price REAL,
        profit REAL,
        trade_time TEXT
    )
    """)

    conn.commit()
    conn.close()
def clear_trades():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trades")
    conn.commit()
    conn.close()

def save_trade(buy_price, sell_price, profit, trade_time):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO trades
    (buy_price, sell_price, profit, trade_time)
    VALUES (?, ?, ?, ?)
    """, (buy_price, sell_price, profit, trade_time))

    conn.commit()
    conn.close()


def load_trades():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM trades")

    rows = cursor.fetchall()

    conn.close()

    return rows