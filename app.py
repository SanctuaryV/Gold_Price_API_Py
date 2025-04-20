from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os
import time

app = Flask(__name__)

def install_chromium():
    subprocess.run("apt-get update", shell=True, check=True)
    subprocess.run("apt-get install -y chromium", shell=True, check=True)
    os.environ["CHROME_BIN"] = "/usr/bin/chromium"

@app.route("/gold-price")
def get_gold_price():
    try:
        install_chromium()
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/chromium"
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
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

        price_element = driver.find_element(By.CSS_SELECTOR, 'div[data-test="instrument-price-last"]')
        data["gold price XAU/USD"]["lastPrice"] = price_element.text

        range_div = driver.find_element(By.CSS_SELECTOR, 'div.mb-3.flex.justify-between.font-bold')
        spans = range_div.find_elements(By.TAG_NAME, 'span')
        if len(spans) == 2:
            data["gold price XAU/USD"]["lowPrice"] = spans[0].text
            data["gold price XAU/USD"]["highPrice"] = spans[1].text

        open_element = driver.find_element(By.CSS_SELECTOR, 'dd[data-test="open"]')
        data["gold price XAU/USD"]["openPrice"] = open_element.text

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            driver.quit()
        except:
            pass

@app.route("/")
def index():
    return "Gold Price API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
