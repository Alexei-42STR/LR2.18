#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
import json
import argparse
import os.path
from dotenv import load_dotenv


def get_human(name, surname, zodiak, date):
    """""
    Запросить данные о человеке.
    """""
    # Вернуть словарь.
    return {
            'surname': surname,
            'name': name,
            'zodiak': zodiak,
            'date': date
        }


def display_human(humans):
    """""
    Отобразить список людей
    """""
    # Проверить что список людей не пуст
    if humans:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Фамилия и имя",
                "Знак Зодиака",
                "Дата рождения"
            )
        )
        print(line)

        # Вывести данные о всех.
        for idx, worker in enumerate(humans, 1):
            date = worker.get('date', '')
            print(
                '| {:^4} | {:<14} {:<15} | {:<20} | {}{} |'.format(
                    idx,
                    worker.get('surname', ''),
                    worker.get('name', ''),
                    worker.get('zodiak', ''),
                    date,
                    ' ' * 5
                )
            )

        print(line)

    else:
        print("Список работников пуст.")


def select_humans(humans, addedzz):
    """""
    Выбрать людей с заданным ЗЗ
    """""
    # Инициализировать счетчик.
    count = 0
    # Сформировать список людей
    result = []
    # Проверить сведения людей из списка.
    for human in humans:
        if human.get('zodiak', '') == addedzz:
            count += 1
            result.append(human)

    return result


def save_humans(file_name, humans):
    with open(file_name, "w") as fout:
        json.dump(humans, fout, ensure_ascii=False, indent=4)


def load_humans(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--data",
        action="store",
        required=False,
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("humans")
    parser.add_argument(
        "--version",
        action="version",
        help="The main parser",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления человека.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new human"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The human's name"
    )
    add.add_argument(
        "-sn",
        "--surname",
        action="store",
        required=True,
        help="The human's surname"
    )
    add.add_argument(
        "-z",
        "--zodiak",
        action="store",
        required=True,
        help="The human's zodiak"
    )
    add.add_argument(
        "-d",
        "--date",
        action="store",
        required=True,
        help="The date of human's birth"
    )

    # Создать субпарсер для отображения всех людей.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all humans"
    )

    # Создать субпарсер для выбора людей.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the humans"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The required select"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    data_file = args.data
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    if not data_file:
        data_file = os.getenv("HUMANS_DATA")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    # Загрузить всех людей из файла, если файл существует.
    is_dirty = False
    if os.path.exists(data_file):
        humans = load_humans(data_file)
    else:
        humans = []

    # Добавить человека.
    if args.command == "add":
        human = get_human(
            args.name,
            args.surname,
            args.zodiak,
            args.date
        )
        humans.append(human)
        is_dirty = True

    # Отобразить всех людей.
    elif args.command == "display":
        display_human(humans)

    # Выбрать требуемых людей.
    elif args.command == "select":
        parts = args.command.split(' ', maxsplit=1)
        addedzz = parts[1]
        selected = select_humans(humans, addedzz)
        display_human(selected)

    # Сохранить данные в файл, если список людей был изменен.
    if is_dirty:
        save_humans(data_file, humans)


if __name__ == '__main__':
    main()
