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

def check_signal():
    price = get_gold_price()
    if price is None:
        return

    # === ตั้งค่ากรอบแนวรับ-แนวต้าน (ปรับตัวเลขตามต้องการ) ===
    buy_zone = 2600.0   # แนวรับ: ถ้าราคาต่ำกว่าหรือเท่ากับจุดนี้ ให้เปิด BUY
    sell_zone = 2650.0  # แนวต้าน: ถ้าราคาสูงกว่าหรือเท่ากับจุดนี้ ให้เปิด SELL
    
    message = ""

    # 1. เงื่อนไขสัญญาณ BUY (เก็งกำไรขาขึ้น)
    if price <= buy_zone:
        message = (
            "🚀 **SIGNAL DETECTED: BUY XAU/USD**\n"
            "-------------------------------------\n"
            f"💰 **Current Price:** ${price:.2f}\n"
            f"📉 **Condition:** เข้าเขตแนวรับสำคัญ (<= ${buy_zone})\n"
            "🧠 **Sentiment:** Risk-Off (แรงซื้อสินทรัพย์ปลอดภัย)\n"
            "-------------------------------------\n"
            "💡 **Action Suggestion:** พิจารณาเปิดออเดอร์ BUY"
        )

    # 2. เงื่อนไขสัญญาณ SELL (เก็งกำไรขาลง)
    elif price >= sell_zone:
        message = (
            "🔻 **SIGNAL DETECTED: SELL XAU/USD**\n"
            "-------------------------------------\n"
            f"💰 **Current Price:** ${price:.2f}\n"
            f"📈 **Condition:** เข้าเขตแนวต้านสำคัญ (>= ${sell_zone})\n"
            "🧠 **Sentiment:** Overbought / ติดแนวต้าน\n"
            "-------------------------------------\n"
            "💡 **Action Suggestion:** พิจารณาเปิดออเดอร์ SELL"
        )

    # ส่งแจ้งเตือนถ้าตรงเงื่อนไขข้อใดข้อหนึ่ง
    if message != "":
        send_telegram(message)
        print(f"[{time.strftime('%H:%M:%S')}] ส่งสัญญาณเรียบร้อย!")

# === เริ่มต้นการรันระบบ ===
print("🤖 เริ่มต้นระบบรันอัตโนมัติเพื่อเฝ้าสัญญาณทองคำ (BUY & SELL)...")
send_telegram("🟢 **ระบบ Auto-Signal (BUY/SELL) เริ่มทำงานแล้ว**")

while True:
    check_signal()
    time.sleep(60)  # เช็คราคาทุกๆ 60 วินาที
