import json
import csv

# Словарь для хранения соответствия user_id -> category
user_category_map = {}

# Читаем файл purchase_log.txt построчно
with open('purchase_log.txt', 'r', encoding='utf-8') as purchase_file:
    for line in purchase_file:
        line = line.strip()
        if not line:
            continue

        # Парсим JSON строку
        try:
            data = json.loads(line)
            user_id = data.get('user_id')
            category = data.get('category')

            # Пропускаем заголовок или неполные строки
            if user_id and category and user_id != 'user_id':
                user_category_map[user_id] = category
        except json.JSONDecodeError:
            continue

# Открываем файлы для чтения и записи
with open('visit_log.csv', 'r', encoding='utf-8') as visit_file, \
        open('funnel.csv', 'w', encoding='utf-8', newline='') as funnel_file:
    # Создаем объекты для чтения и записи
    reader = csv.reader(visit_file)
    writer = csv.writer(funnel_file)

    # Читаем заголовок из visit_log.csv
    header = next(reader)
    # Добавляем столбец category к заголовку
    writer.writerow(header + ['category'])

    # Обрабатываем каждую строку
    for row in reader:
        if len(row) < 2:  # Проверяем, что строка содержит как минимум user_id и source
            continue

        user_id = row[0]
        # Проверяем, есть ли у этого user_id покупка
        if user_id in user_category_map:
            # Добавляем категорию к строке и записываем в файл
            writer.writerow(row + [user_category_map[user_id]])