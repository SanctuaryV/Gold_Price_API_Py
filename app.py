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
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://th.investing.com/currencies/xau-usd", timeout=60000)
            page.wait_for_selector('div[data-test="instrument-price-last"]')

            data["gold price XAU/USD"]["lastPrice"] = page.query_selector('div[data-test="instrument-price-last"]').inner_text()

            spans = page.query_selector_all("div.mb-3.flex.justify-between.font-bold span")
            if len(spans) == 2:
                data["gold price XAU/USD"]["lowPrice"] = spans[0].inner_text()
                data["gold price XAU/USD"]["highPrice"] = spans[1].inner_text()

            data["gold price XAU/USD"]["openPrice"] = page.query_selector('dd[data-test="open"]').inner_text()

            browser.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(data)

@app.route("/")
def index():
    return "Gold Price API using Playwright is running!"

# สำหรับ Gunicorn, Flask สามารถรันได้โดยไม่ต้องการการตั้งค่าอะไรเพิ่มเติม
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
