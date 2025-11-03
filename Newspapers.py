from datetime import datetime


def parse_date(date_str, newspaper_name):
    try:
        if newspaper_name == "The Moscow Times":
            return datetime.strptime(date_str, "%A, %B %d, %Y")
        elif newspaper_name == "The Guardian":
            return datetime.strptime(date_str, "%A, %d.%m.%y")
        elif newspaper_name == "Daily News":
            return datetime.strptime(date_str, "%A, %d %B %Y")
        else:
            return None
    except ValueError:
        return None


def main():
    print("Программа для парсинга дат газет")
    print("Доступные газеты: The Moscow Times, The Guardian, Daily News")
    print("Для выхода введите 'quit' или 'exit'")
    print("-" * 50)

    examples = [
        ("The Moscow Times", "Wednesday, October 2, 2002"),
        ("The Guardian", "Friday, 11.10.13"),
        ("Daily News", "Thursday, 18 August 1977")
    ]

    print("Примеры из условия:")
    for newspaper, date_str in examples:
        result = parse_date(date_str, newspaper)
        if result:
            print(f"{newspaper}: {date_str} -> {result}")
        else:
            print(f"{newspaper}: {date_str} -> Ошибка парсинга")
    print("-" * 50)

    while True:
        print("\nВведите данные (формат: 'Название газеты, дата')")
        user_input = input("Или 'quit' для выхода: ").strip()

        if user_input.lower() in ['quit', 'exit', 'выход']:
            print("Завершение программы...")
            break

        parts = user_input.split(',', 1)
        if len(parts) != 2:
            print("Ошибка: неверный формат ввода. Используйте: 'Название газеты, дата'")
            continue

        newspaper_name = parts[0].strip()
        date_str = parts[1].strip()

        result = parse_date(date_str, newspaper_name)

        if result:
            print(f"Успешно распарсено: {result}")
        else:
            print("Ошибка: не удалось распарсить дату. Проверьте формат и название газеты.")
            print("Форматы дат:")
            print("  - The Moscow Times: 'Wednesday, October 2, 2002'")
            print("  - The Guardian: 'Friday, 11.10.13'")
            print("  - Daily News: 'Thursday, 18 August 1977'")


if __name__ == "__main__":
    main()