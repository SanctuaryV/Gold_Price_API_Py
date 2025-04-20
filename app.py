from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

app = Flask(__name__)

@app.route("/gold-price")
def get_gold_price():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://th.investing.com/currencies/xau-usd")
    
    try:
        # รอให้ข้อมูลโหลด
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="instrument-price-last"]'))
        )

        data = {
            "ราคาทองคำ XAU/USD": {
                "ราคาล่าสุด": None,
                "ราคาต่ำสุด": None,
                "ราคาสูงสุด": None,
                "ราคาเปิด": None
            }
        }

        # ดึงราคาล่าสุด
        price_element = driver.find_element(By.CSS_SELECTOR, 'div[data-test="instrument-price-last"]')
        data["ราคาทองคำ XAU/USD"]["ราคาล่าสุด"] = price_element.text

        # ดึงราคาต่ำสุดและสูงสุด
        range_div = driver.find_element(By.CSS_SELECTOR, 'div.mb-3.flex.justify-between.font-bold')
        spans = range_div.find_elements(By.TAG_NAME, 'span')
        if len(spans) == 2:
            data["ราคาทองคำ XAU/USD"]["ราคาต่ำสุด"] = spans[0].text
            data["ราคาทองคำ XAU/USD"]["ราคาสูงสุด"] = spans[1].text

        # ดึงราคาเปิด
        open_element = driver.find_element(By.CSS_SELECTOR, 'dd[data-test="open"]')
        data["ราคาทองคำ XAU/USD"]["ราคาเปิด"] = open_element.text

    except (NoSuchElementException, TimeoutException) as e:
        return jsonify({"error": f"เกิดข้อผิดพลาดในการดึงข้อมูล: {str(e)}"}), 500
    finally:
        driver.quit()

    return jsonify(data)

# รัน Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
