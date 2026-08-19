import requests
import time

TELEGRAM_TOKEN = "8807059278:AAH-kpLAIUYSonacKjIsOFnBDY_mHCtzGCA"
CHAT_ID = "8331557493"  # ใส่ Chat ID ของคุณ

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("ส่งข้อความล้มเหลว:", e)

def get_gold_price():
    # ดึงราคา Real-time (ตัวอย่างใช้ Gold API)
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

    # === เงื่อนไขสัญญาณเทรด (ปรับเปลี่ยนตาม Strategy ของคุณ) ===
    # ตัวอย่าง: สั่งซื้อเมื่อราคาลงมาแตะแนวรับ หรือเกิด Breakout
    buy_zone = 2600.0  # สมมติแนวรับ
    
    # ตัวอย่างการวิเคราะห์ Sentiment / ปัจจัยข่าวเบื้องต้น
    signal_triggered = False
    message = ""

    if price <= buy_zone:
        signal_triggered = True
        message = (
            "🚀 **SIGNAL DETECTED: XAU/USD**\n"
            "-------------------------------------\n"
            f"💰 **Current Price:** ${price:.2f}\n"
            "📉 **Condition:** เข้าเขตแนวรับสำคัญ (Buy Zone)\n"
            "🧠 **Sentiment:** Risk-Off (แรงซื้อสินทรัพย์ปลอดภัย)\n"
            "-------------------------------------\n"
            "💡 **Action Suggestion:** พิจารณาเปิดออเดอร์ BUY"
        )

    if signal_triggered:
        send_telegram(message)
        print(f"[{time.strftime('%H:%M:%S')}] ส่งสัญญาณเรียบร้อย!")

# === เริ่มต้นการรันแบบอัตโนมัติ ===
print("🤖 เริ่มต้นระบบรันอัตโนมัติเพื่อเฝ้าสัญญาณทองคำ...")
send_telegram("🟢 **ระบบ Auto-Signal เริ่มทำงานแล้ว** (ระบบจะแจ้งเตือนเมื่อเกิดสัญญาณ)")

while True:
    check_signal()
    time.sleep(60)  # เช็คสัญญาณทุกๆ 60 วินาที (1 นาที)
