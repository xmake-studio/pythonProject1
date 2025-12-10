def read_csv_file(file_path):
    """Читает CSV-файл и возвращает список строк (включая заголовок)"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = []
        for line in file:
            # Убираем символы новой строки и разбиваем по запятым
            row = []
            current_field = ''
            in_quotes = False
            for char in line:
                if char == '"':
                    in_quotes = not in_quotes
                elif char == ',' and not in_quotes:
                    row.append(current_field.strip())
                    current_field = ''
                else:
                    current_field += char
            row.append(current_field.strip().rstrip('\n\r'))
            lines.append(row)
    return lines


def parse_csv_header(data_rows):
    """Извлекает заголовки из первой строки CSV"""
    if not data_rows:
        return []
    return data_rows[0]


def parse_csv_records(data_rows):
    """Извлекает записи (без заголовка) из CSV-данных"""
    if len(data_rows) < 2:
        return []
    return data_rows[1:]


def map_record_to_dict(headers, record):
    """Преобразует строку данных в словарь с ключами из заголовков"""
    record_dict = {}
    for i in range(len(headers)):
        if i < len(record):
            record_dict[headers[i]] = record[i]
        else:
            record_dict[headers[i]] = ''
    return record_dict


def get_device_type_russian(device_type):
    """Возвращает русское описание типа устройства"""
    if device_type == 'mobile':
        return 'мобильного'
    elif device_type == 'tablet':
        return 'планшетного'
    elif device_type == 'laptop':
        return 'ноутбучного'
    elif device_type == 'desktop':
        return 'ПК'
    else:
        return device_type


def format_user_description(user_data):
    """Формирует текстовое описание пользователя по шаблону"""
    name = user_data['name']
    sex = user_data['sex']
    age = user_data['age']
    device_type = user_data['device_type']
    browser = user_data['browser']
    bill = user_data['bill']
    region = user_data['region']

    # Определяем род для описания пола
    if sex == 'female':
        gender_description = 'женского пола'
        action_description = 'совершила'
    elif sex == 'male':
        gender_description = 'мужского пола'
        action_description = 'совершил'
    else:
        gender_description = 'неопределенного пола'
        action_description = 'совершил(а)'

    device_russian = get_device_type_russian(device_type)

    description = f"Пользователь {name} {gender_description}, {age} лет {action_description} покупку на {bill} у.е. с {device_russian} браузера {browser}. Регион, из которого совершалась покупка: {region}."
    return description


def process_csv_to_descriptions(csv_data):
    """Обрабатывает CSV-данные и возвращает список описаний пользователей"""
    headers = parse_csv_header(csv_data)
    records = parse_csv_records(csv_data)

    descriptions = []
    for record in records:
        user_dict = map_record_to_dict(headers, record)
        description = format_user_description(user_dict)
        descriptions.append(description)

    return descriptions


def write_descriptions_to_file(descriptions, output_file_path):
    """Записывает список описаний в TXT-файл"""
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for description in descriptions:
            file.write(description + '\n')


def main(input_file_path, output_file_path):
    """Основная функция для выполнения полного цикла обработки"""
    csv_data = read_csv_file(input_file_path)
    descriptions = process_csv_to_descriptions(csv_data)
    write_descriptions_to_file(descriptions, output_file_path)

# Пример вызова (для тестирования)
main('web_clients_correct.csv', 'output.txt')