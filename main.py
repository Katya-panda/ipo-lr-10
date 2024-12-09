import requests  # импортируем модуль для выполнения HTTP-запросов
from bs4 import BeautifulSoup  # импортируем BeautifulSoup для парсинга HTML-кода
import json  # импортируем модуль для работы с JSON
import os
def load_html_template(template_path): 
    with open(template_path, 'r', encoding='utf-8') as file: 
        return file.read()
def generate_quotes_rows(data): 
    return ''.join([f"<tr><td>{i+1}</td><td>{quote['quote']}</td><td>{quote['author']}</td></tr>" for i, quote in enumerate(data)])
def save_quotes_to_json(quotes_data, filename='data.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(quotes_data, file, ensure_ascii=False, indent=4)
def main():
    url = "https://quotes.toscrape.com/"  # URL страницы с цитатами
    response = requests.get(url)  # выполняем запрос к странице
    soup = BeautifulSoup(response.text, "html.parser")  # парсим HTML-код страницы
    quotes = soup.find_all('span', class_='text')  # находим все цитаты на странице
    authors = soup.find_all('small', class_='author')  # находим всех авторов на странице
    quotes_data = []
    for quote, author in zip(quotes, authors):
        quotes_data.append({"quote": quote.text.strip(), "author": author.text.strip()})
    save_quotes_to_json(quotes_data)
    print("Данные успешно сохранены в файл data.json.")
     # Загрузка данных из JSON-файла
    with open('data.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
    print("Данные успешно загружены из файла data.json.")
    # Загрузка HTML-шаблона 
    template_path = 'template.html'
    html_template = load_html_template(template_path)
    # Генерация строк таблицы с цитатами 
    quotes_rows = generate_quotes_rows(quotes_data) 
    # Подстановка строк таблицы в HTML-шаблон 
    html_content = html_template.format(quotes_rows=quotes_rows)
# Сохранение HTML-кода в файл index.html 
    with open('index.html', 'w', encoding='utf-8') as f: 
        f.write(html_content) 
        print("HTML-страница успешно сгенерирована и сохранена в файл index.html.")
if __name__ == "__main__":
    main()