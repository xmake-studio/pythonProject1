import csv

def get_device_type_russian(device_type):
    mapping = {
        'mobile': 'мобильного',
        'tablet': 'планшетного',
        'laptop': 'ноутбучного',
        'desktop': 'ПК',
    }
    return mapping.get(device_type, device_type)

def format_user_description(user_data):
    name = user_data['name']
    sex = user_data['sex']
    age = user_data['age']
    device_type = user_data['device_type']
    browser = user_data['browser']
    bill = user_data['bill']
    region = user_data['region']

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

    return (
        f"Пользователь {name} {gender_description}, {age} лет "
        f"{action_description} покупку на {bill} у.е. с {device_russian} браузера {browser}. "
        f"Регион, из которого совершалась покупка: {region}."
    )

def main(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        for row in reader:
            description = format_user_description(row)
            outfile.write(description + '\n')

main('web_clients_correct.csv', 'output.txt')