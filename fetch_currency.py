import requests
import json

# Получаем курс от ЦБ РФ
url = "https://www.cbr-xml-daily.ru/daily_json.js"
response = requests.get(url)
data = response.json()
usd_rate = data["Valute"]["USD"]["Value"]

# Сохраняем в JSON
with open("usd_rub_rate.json", "w", encoding="utf-8") as f:
    json.dump({"usd_rub": usd_rate}, f, ensure_ascii=False, indent=2)

print(f"✅ Курс USD/RUB: {usd_rate} ₽")
