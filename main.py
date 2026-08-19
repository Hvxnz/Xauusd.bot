import requests
import time

TELEGRAM_TOKEN = "8807059278:AAH-kpLAIUYSonacKjIsOFnBDY_mHCtzGCA"
CHAT_ID = "8331557493"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("ส่งข้อความล้มเหลว:", e)

def get_gold_price():
    url = "https://api.gold-api.com/price/XAU"
    try:
        res = requests.get(url).json()
        return float(res['price'])
    except Exception:
        return None

# เก็บราคาย้อนหลังเพื่อคำนวณ dynamic zone
price_history = []

def calculate_dynamic_zones(prices, window=20, deviation=1.5):
    """คำนวณแนวรับ-แนวต้านไดนามิกตามความผันผวนของราคาจริง"""
    if len(prices) < window:
        return None, None
    
    recent_prices = prices[-window:]
    sma = sum(recent_prices) / window
    variance = sum((x - sma) ** 2 for x in recent_prices) / window
    std_dev = variance ** 0.5
    
    # Dynamic Support (Buy) / Resistance (Sell)
    buy_zone = sma - (std_dev * deviation)
    sell_zone = sma + (std_dev * deviation)
    
    return buy_zone, sell_zone

def check_signal():
    price = get_gold_price()
    if price is None:
        return

    price_history.append(price)
    # จำกัดขนาดประวัติราคาไว้ที่ 100 ค่า
    if len(price_history) > 100:
        price_history.pop(0)

    # คำนวณแนวรับ-แนวต้านแบบขยับตามจริง (ใช้ข้อมูล 20 แท่งล่าสุด)
    buy_zone, sell_zone = calculate_dynamic_zones(price_history, window=20)
    
    # หากข้อมูลยังไม่พอคำนวณ ให้ข้ามไปก่อน
    if buy_zone is None or sell_zone is None:
        print(f"[{time.strftime('%H:%M:%S')}] กำลังสะสมข้อมูลราคา ({len(price_history)}/20)...")
        return

    message = ""

    if price <= buy_zone:
        message = (
            "🚀 **DYNAMIC SIGNAL: BUY XAU/USD**\n"
            "-------------------------------------\n"
            f"💰 **Current Price:** ${price:.2f}\n"
            f"📉 **Dynamic Support:** ${buy_zone:.2f}\n"
            "-------------------------------------\n"
            "💡 **Action Suggestion:** พิจารณาเปิดออเดอร์ BUY"
        )
    elif price >= sell_zone:
        message = (
            "🔻 **DYNAMIC SIGNAL: SELL XAU/USD**\n"
            "-------------------------------------\n"
            f"💰 **Current Price:** ${price:.2f}\n"
            f"📈 **Dynamic Resistance:** ${sell_zone:.2f}\n"
            "-------------------------------------\n"
            "💡 **Action Suggestion:** พิจารณาเปิดออเดอร์ SELL"
        )

    if message != "":
        send_telegram(message)
        print(f"[{time.strftime('%H:%M:%S')}] ส่งสัญญาณเรียบร้อย!")

print("🤖 เริ่มต้นระบบ Dynamic Auto-Signal (BUY/SELL)...")
send_telegram("🟢 **ระบบ Dynamic Auto-Signal เริ่มทำงานแล้ว**")

while True:
    check_signal()
    time.sleep(60)
        
