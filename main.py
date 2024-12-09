import requests  # импортируем модуль для выполнения HTTP-запросов
from bs4 import BeautifulSoup  # импортируем BeautifulSoup для парсинга HTML-кода
import json  # импортируем модуль для работы с JSON
import os # импортируем модуль os для работы с файловой системой
# функция для загрузки HTML-шаблона
def load_html_template(template_path): 
    with open(template_path, 'r', encoding='utf-8') as file: # открываем файл шаблона для чтения в кодировке UTF-8
        return file.read() # читаем и возвращаем содержимое файла
# функция для генерации строк таблицы с цитатами
def generate_quotes_rows(data): 
    # генерируем HTML-строки для каждой цитаты и автора
    return ''.join([f"<tr><td>{i+1}</td><td>{quote['quote']}</td><td>{quote['author']}</td></tr>" for i, quote in enumerate(data)])
# функция для сохранения данных в JSON-файл
def save_quotes_to_json(quotes_data, filename='data.json'):
    with open(filename, 'w', encoding='utf-8') as file:  # открываем файл для записи в кодировке UTF-8
        json.dump(quotes_data, file, ensure_ascii=False, indent=4) # сохраняем данные в JSON-файл с отступами
# основная функция
def main():
    url = "https://quotes.toscrape.com/"  # URL страницы с цитатами
    response = requests.get(url)  # выполняем запрос к странице
    soup = BeautifulSoup(response.text, "html.parser")  # парсим HTML-код страницы
    quotes = soup.find_all('span', class_='text')  # находим все цитаты на странице
    authors = soup.find_all('small', class_='author')  # находим всех авторов на странице
    quotes_data = [] # инициализируем пустой список для хранения данных
    for quote, author in zip(quotes, authors):
        quotes_data.append({"quote": quote.text.strip(), "author": author.text.strip()}) # добавляем цитаты и авторов в список
    save_quotes_to_json(quotes_data) # сохраняем данные в файл data.json
    print("Данные успешно сохранены в файл data.json.") # выводим сообщение об успешном сохранении данных
     # загрузка данных из JSON-файла
    with open('data.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)  # читаем данные из файла data.json
    print("Данные успешно загружены из файла data.json.") # выводим сообщение об успешной загрузке данных
    # загрузка HTML-шаблона 
    template_path = 'template.html' # определяем путь к файлу шаблона
    html_template = load_html_template(template_path) # загружаем HTML-шаблон 
    quotes_rows = generate_quotes_rows(quotes_data)  # генерация строк таблицы с цитатами
    html_content = html_template.format(quotes_rows=quotes_rows) # подстановка строк таблицы в HTML-шаблон 
# сохранение HTML-кода в файл index.html 
    with open('index.html', 'w', encoding='utf-8') as f: 
        f.write(html_content) # записываем сгенерированный HTML-код в файл
        print("HTML-страница успешно сгенерирована и сохранена в файл index.html.") # выводим сообщение об успешном сохранении HTML
# запускаем основную функцию
if __name__ == "__main__": # проверяем, выполняется ли скрипт напрямую или импортируется как модуль в другой программе
    main() # вызываем основную функцию