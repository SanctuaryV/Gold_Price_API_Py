
# Gold Price API

โปรเจกต์นี้เป็น API ที่สร้างขึ้นด้วย Flask และ Selenium สำหรับดึงข้อมูลราคาทองคำ (XAU/USD) จากเว็บไซต์ Investing.com API นี้ถูก deploy บน Render และสามารถเข้าถึงได้ผ่าน URL สาธารณะ

## คุณสมบัติ

- ดึงข้อมูลราคาทองคำ (XAU/USD) ปัจจุบัน
- ให้ข้อมูลราคาสูงสุด ราคาต่ำสุด และราคาเปิดของวัน
- ส่งคืนข้อมูลในรูปแบบ JSON ที่มีโครงสร้าง

## Endpoints

### `GET /gold-price`

คืนค่าข้อมูลราคาทองคำในรูปแบบ JSON:

**ตัวอย่าง Response:**

```json
{
  "gold price XAU/USD": {
    "lastPrice": "2,345.67",
    "lowPrice": "2,310.00",
    "highPrice": "2,355.00",
    "openPrice": "2,320.00"
  }
}
```

## การติดตั้ง

หากต้องการรันโปรเจกต์นี้ในเครื่องของคุณ สามารถทำตามขั้นตอนดังนี้:

### 1. โคลน repository

```bash
git clone https://github.com/yourusername/gold-price-api.git
cd gold-price-api
```

### 2. ติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

### 3. รันแอป Flask

```bash
python app.py
```

แอปจะรันที่ `http://127.0.0.1:5000` โดยค่าเริ่มต้น

### 4. เข้าถึง API

คุณสามารถเข้าถึง endpoint `/gold-price` ที่ `http://127.0.0.1:5000/gold-price` เพื่อรับข้อมูลราคาทองคำ

## การ deploy บน Render

แอปนี้ถูก deploy บน Render และสามารถเข้าถึงได้ผ่าน URL สาธารณะที่ให้มา แอปนี้รันบน Flask server พร้อมกับการใช้ Selenium ในการดึงข้อมูลราคาทองจากเว็บไซต์ Investing.com

### ขั้นตอนการ Deploy:

1. ไปที่ [Render](https://render.com) และสร้าง Web Service ใหม่
2. เชื่อมต่อ repository ของคุณกับ Render
3. ตั้งค่า build command ให้เป็น:

   ```bash
   pip install -r requirements.txt
   ```

4. ตั้งค่า start command ให้เป็น:

   ```bash
   python app.py
   ```

5. คลิก "Create Web Service" เพื่อ deploy แอป

## License

โปรเจกต์นี้ใช้ลิขสิทธิ์แบบ MIT - ดูรายละเอียดเพิ่มเติมที่ไฟล์ [LICENSE](LICENSE)
