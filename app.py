from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/gold-price")
def get_gold_price():
    data = {
        "gold price XAU/USD": {
            "lastPrice": None,
            "lowPrice": None,
            "highPrice": None,
            "openPrice": None
        }
    }

    try:
        with sync_playwright() as p:
            # เปิด Chromium browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://th.investing.com/currencies/xau-usd", timeout=60000)  # ตั้งเวลา timeout เป็น 60 วินาที

            # รอให้ selector โหลดเสร็จ
            page.wait_for_selector('div[data-test="instrument-price-last"]')

            # ดึงราคาทองคำ
            last_price_element = page.query_selector('div[data-test="instrument-price-last"]')
            if last_price_element:
                data["gold price XAU/USD"]["lastPrice"] = last_price_element.inner_text()

            # ดึงราคาต่ำสุดและสูงสุด
            spans = page.query_selector_all("div.mb-3.flex.justify-between.font-bold span")
            if len(spans) == 2:
                data["gold price XAU/USD"]["lowPrice"] = spans[0].inner_text()
                data["gold price XAU/USD"]["highPrice"] = spans[1].inner_text()

            # ดึงราคาเปิด
            open_price_element = page.query_selector('dd[data-test="open"]')
            if open_price_element:
                data["gold price XAU/USD"]["openPrice"] = open_price_element.inner_text()

            # ปิด browser
            browser.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(data)

@app.route("/")
def index():
    return "Gold Price API using Playwright is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
