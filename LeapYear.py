def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True  # делится на 400 → високосный
            else:
                return False  # делится на 100, но не на 400 → не високосный
        else:
            return True  # делится на 4, но не на 100 → високосный
    else:
        return False  # не делится на 4 → не високосный


year = 2025
print("Високосный год" if is_leap_year(year) else "Обычный год")
