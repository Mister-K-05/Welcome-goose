import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Ошибка при получении страницы: {e}")
        return None

def parse_product(product_element):
    try:
        # Название товара
        name = product_element.find('h3', class_='product-title').text.strip()
        
        # Характеристики
        specs = product_element.find('div', class_='product-specs')
        specs_text = specs.text.strip() if specs else "Характеристики не указаны"
        
        # Цена
        price_element = product_element.find('span', class_='price')
        price = price_element.text.strip() if price_element else "Цена не указана"
        
        # URL изображения
        img = product_element.find('img')
        img_url = urljoin('https://05.ru', img['src']) if img and 'src' in img.attrs else "Изображение не найдено"
        
        return [name, specs_text, price, img_url]
    except Exception as e:
        print(f"Ошибка при парсинге товара: {e}")
        return None

def main():
    base_url = 'https://05.ru/catalog/telefony-i-gadzhety/'
    products_data = []
    page = 1
    
    # Добавляем заголовки для CSV файла
    products_data.append(['Название товара', 'Основные характеристики', 'Цена', 'URL фотографии'])
    
    while True:
        url = f"{base_url}?PAGEN_1={page}"
        html = get_page(url)
        
        if not html:
            break
            
        soup = BeautifulSoup(html, 'lxml')
        products = soup.find_all('div', class_='product-item')
        
        if not products:
            break
            
        for product in products:
            product_data = parse_product(product)
            if product_data:
                products_data.append(product_data)
        
        print(f"Обработана страница {page}")
        page += 1
        time.sleep(1)  # Задержка между запросами
    
    # Сохранение в CSV
    if len(products_data) > 1:  # Проверяем, есть ли данные кроме заголовков
        with open('telefony_i_gadzhety.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(products_data)
        print("Данные успешно сохранены в файл 'telefony_i_gadzhety.csv'")
    else:
        print("Не удалось получить данные")

if __name__ == '__main__':
    main()