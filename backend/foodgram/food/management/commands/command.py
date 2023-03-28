import json
import sys

from django.core.management.base import BaseCommand
from food.models import Ingredient


class Command(BaseCommand):
    """
    Команда для извлеения данных из csv.
    Запуск python manage.py command имя сsv файла.
    """
    help = 'Создает Данные из csv, параметр название файла'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Путь к файлу')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file']
        file = f'data/{file_name}.json'
        try:
            with open(file, "r", encoding="utf-8-sig") as json_file:
                data = json.load(json_file)
                for row in data:
                    Ingredient.objects.update_or_create(
                        **row
                    )
        except IOError:
            print("Нет файла!")
            sys.exit()
