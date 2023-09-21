import requests
from bs4 import BeautifulSoup as BS
import csv

csv_filename = 'mashina.kg_data.csv'
csv_file = open(csv_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.DictWriter(csv_file, fieldnames=['Название', 'Цена', 'Изображение', 'Описание'])
csv_writer.writeheader()

base_url = 'https://www.mashina.kg/search/all/'

response = requests.get(base_url)

if response.status_code == 200:
    soup = BS(response.text, 'lxml')
    category_links = soup.find_all('a', class_='cat-item')
    for category_link in category_links:
        category_name = category_link.text.strip()
        category_url = category_link['href']
        category_response = requests.get(category_url)
        if category_response.status_code == 200:
            category_soup = BS(category_response.text, 'html.parser')
            model_items = category_soup.find_all('div', class_='item-inner')
            
            for model_item in model_items:
                model_name = model_item.find('div', class_='name').text.strip()
                model_price = model_item.find('div', class_='block price').text.strip()
                model_image = model_item.find('image-wrap')['src']
                model_description = model_item.find('div', class_='block info-wrapper item-info-wrapper').text.strip()

                csv_writer.writerow({'Название': model_name, 'Цена': model_price, 'Изображение': model_image, 'Описание': model_description})
        else:
            print("Ошибка при запросе к странице с моделями:", category_response.status_code)
else:
    print("Ошибка при запросе к базовой странице:", response.status_code)

csv_file.close()
        
    
    
    
    
    
    
    
