from environs import Env
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas
import collections
import argparse


def get_year_word(company_age):
    if company_age % 100 in (11, 12, 13, 14):
        return f'{company_age} лет'
    last_digit = company_age % 10
    if last_digit == 1:
        return f'{company_age} год'
    if 2 <= last_digit <= 4:
        return f'{company_age} года'
    return f'{company_age} лет'


def calculate_age_company():
    foundetion_year = 1920
    company_age = datetime.now().year - foundetion_year
    return company_age


def main():
    env = Env()
    env.read_env()
    excel_path = env.str('EXCEL_PATH', default='table_of_property_wine.xlsx')

    parser = argparse.ArgumentParser(description='''Введите путь до файла, либо же название файла, 
                                     если он уже находится в директории скрипта.''')
    parser.add_argument('--path', default=excel_path, help='Путь')
    args = parser.parse_args()

    wine_table = pandas.read_excel(args.path).fillna('')

    wines_by_category = collections.defaultdict(list)

    for _, row in wine_table.iterrows():
        category = row['Категория']
        wine_data = {
            'Картинка': row['Картинка'],
            'Категория': row['Категория'],
            'Название': row['Название'],
            'Сорт': row['Сорт'],
            'Цена': row['Цена'],
            'Акция': row['Акция']
        }
        wines_by_category[category].append(wine_data)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    company_age = calculate_age_company()

    rendered_page = template.render(
        age_text=f'Уже {get_year_word(company_age)} с вами',
        wine_catalog=wines_by_category
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
