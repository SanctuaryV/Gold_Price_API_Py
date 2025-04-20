from flask import Flask, jsonify
from pyngrok import ngrok
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

# เปิด tunnel ngrok ไปยังพอร์ต 5000
public_url = ngrok.connect(5000)
print("🚀 Public URL:", public_url)

@app.route("/gold-price")
def get_gold_price():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://th.investing.com/currencies/xau-usd")
    time.sleep(5)

    data = {
        "gold price XAU/USD": {
            "lastPrice": None,
            "lowPrice": None,
            "highPrice": None,
            "openPrice": None
        }
    }

    try:
        price_element = driver.find_element(By.CSS_SELECTOR, 'div[data-test="instrument-price-last"]')
        data["gold price XAU/USD"]["lastPrice"] = price_element.text

        range_div = driver.find_element(By.CSS_SELECTOR, 'div.mb-3.flex.justify-between.font-bold')
        spans = range_div.find_elements(By.TAG_NAME, 'span')
        if len(spans) == 2:
            data["gold price XAU/USD"]["lowPrice"] = spans[0].text
            data["gold price XAU/USD"]["highPrice"] = spans[1].text

        open_element = driver.find_element(By.CSS_SELECTOR, 'dd[data-test="open"]')
        data["gold price XAU/USD"]["openPrice"] = open_element.text

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.quit()

    return jsonify(data)

# รัน Flask app
app.run(host="0.0.0.0", port=5000)
