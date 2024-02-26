from pymongo import MongoClient
from mongoengine import *
import json

# Підключення до бази даних MongoDB
connect('test_data', host='mongodb://Sasha_Lenko:<Aaddon776899>@federateddatabaseinstance0-rvbaa.a.query.mongodb.net/?ssl=true&authSource=admin&appName=FederatedDatabaseInstance0')

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

# Модель для цитат
class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

# Функція для завантаження даних з JSON-файлів у базу даних
def load_data_from_json(authors_file, quotes_file):
    with open(authors_file, 'r') as f:
        authors_data = json.load(f)

    with open(quotes_file, 'r') as f:
        quotes_data = json.load(f)

    # Завантаження даних про авторів
    for author_info in authors_data:
        author = Author(
            fullname=author_info['fullname'],
            born_date=author_info['born_date'],
            born_location=author_info['born_location'],
            description=author_info['description']
        )
        author.save()

    # Завантаження даних про цитати
    for quote_info in quotes_data:
        author = Author.objects(fullname=quote_info['author']).first()
        quote = Quote(
            tags=quote_info['tags'],
            author=author,
            quote=quote_info['quote']
        )
        quote.save()

# Функція для пошуку цитат за тегом, ім'ям автора або набором тегів
def search_quotes(command):
    parts = command.split(':')
    if len(parts) != 2:
        print("Invalid command format")
        return

    key, value = parts[0].strip(), parts[1].strip()

    if key == 'name':
        author = Author.objects(fullname=value).first()
        if author:
            quotes = Quote.objects(author=author)
            for q in quotes:
                print(f"Author: {q.author.fullname}, Quote: {q.quote}")
        else:
            print("Author not found")
    elif key == 'tag':
        quotes = Quote.objects(tags=value)
        for q in quotes:
            print(f"Author: {q.author.fullname}, Quote: {q.quote}")
    elif key == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
        for q in quotes:
            print(f"Author: {q.author.fullname}, Quote: {q.quote}")
    else:
        print("Invalid command")

# Основна функція
if __name__ == "__main__":
    # Завантаження даних з JSON-файлів
    load_data_from_json('authors.json', 'quotes.json')

    # Виконання скрипту пошуку цитат
    while True:
        command = input("Enter command (name:<author_name>, tag:<tag_name>, tags:<tag1,tag2>, exit to quit): ")
        if command == 'exit':
            break
        search_quotes(command)
