from database import create_database, save_trade, load_trades

create_database()

save_trade(
    buy_price=100,
    sell_price=110,
    profit=10,
    trade_time="2026-06-29 19:00"
)

print(load_trades())