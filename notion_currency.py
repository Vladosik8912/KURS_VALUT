import os
import requests
from datetime import datetime

# Конфигурация
NOTION_TOKEN = os.getenv('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')
DATABASE_ID = os.getenv('20879c7a7931808491dfd5f04815a2ee')

def get_usd_rate():
    """Получаем курс USD от ЦБ РФ"""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    data = response.json()
    return data['Valute']['USD']['Value']

def update_notion_table():
    """Обновляем все строки в таблице Notion"""
    # Получаем текущий курс
    usd_rate = get_usd_rate()
    print(f"Current USD rate: {usd_rate}")
    
    # Настройка запросов к Notion API
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # 1. Получаем все записи таблицы (с пагинацией)
    all_pages = []
    next_cursor = None
    
    while True:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
            
        response = requests.post(
            f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
            headers=headers,
            json=payload
        )
        data = response.json()
        all_pages.extend(data.get('results', []))
        
        next_cursor = data.get('next_cursor')
        if not next_cursor or not data.get('has_more', False):
            break
    
    print(f"Found {len(all_pages)} pages to update")
    
    # 2. Обновляем каждую запись
    for page in all_pages:
        page_id = page['id']
        
        update_response = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=headers,
            json={
                "properties": {
                    "Курс USD": {  # ⚠️ ЗАМЕНИТЕ НА ВАШЕ НАЗВАНИЕ СТОЛБЦА
                        "number": usd_rate
                    },
                    "Обновлено": {
                        "date": {
                            "start": datetime.now().isoformat(),
                            "time_zone": "Europe/Moscow"
                        }
                    }
                }
            }
        )
        
        if update_response.status_code != 200:
            print(f"Error updating page {page_id}: {update_response.text}")

if __name__ == "__main__":
    update_notion_table()
    print("Notion table updated successfully!")
