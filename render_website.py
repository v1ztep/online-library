from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked
import os
import math


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('templates/template.html')

    for page_current_number, twenty_books_list in enumerate(grouped_by_twenty_books_list, 1):
        grouped_by_two_books_list = list(chunked(twenty_books_list, 2))

        rendered_page = template.render(
            grouped_by_two_books_list=grouped_by_two_books_list,
            pages_amount=pages_amount,
            page_current_number=page_current_number,
        )

        with open(f'pages/index{page_current_number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)
    print("Site rebuilded")


with open("media/description.json", "r", encoding="utf8") as my_file:
    books_json = my_file.read()
books_list = json.loads(books_json)
grouped_by_twenty_books_list = list(chunked(books_list, 20))
pages_amount = math.ceil(len(books_list)/20)


os.makedirs('pages', exist_ok=True)

on_reload()

server = Server()

server.watch('templates/template.html', on_reload)

server.serve(root='.')

