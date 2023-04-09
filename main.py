from random import randint
import json

def gen():
    master_card, new_card = randint(511111, 551111), randint(111111111, 999999999)
    card_number = str(master_card) + str(new_card)
    return card_number

def luhn(card_number):
    summa = 0
    for number in card_number[0::2]:
        if int(number) * 2 > 9:
            number = int(number) * 2 - 9
        else:
            number = int(number) * 2
        summa += int(number)

    for number in card_number[1::2]:
        summa += int(number)

    if (summa % 10) != 0:
        summa2 = (summa + 10) - (summa % 10)
        last = summa2 - summa
        card_number += str(last)
    else:
        card_number += '0'

    return str(card_number)

def start():
    while True:
        choice = input('Здравствуйте! Это банковское приложение на языке Python. Если вы имеете аккаунт, введите "Войти", иначе "Регистрация", для регистрации '
                       '\nчтобы выйти из приложения введите "Выход" ')
        match choice.lower():
            case 'регистрация':
                register()
                auth()
            case 'войти':
                auth()
                break
            case 'выход':
                break
            case _: print('Вы ввели неправильное значение')

def register():
    name = str(input('Регистрация \nВведите Ваше имя для регистрации '))
    with open("users.json", encoding="utf-8") as file:
        bankbook = json.load(file)
        bankbook = dict(bankbook)
        if name in bankbook:
            print('Аккаунт с таким именем уже существует')
            return
        else:
            password = str(input('Придумайте и введите пароль '))
            user = dict()
            user[name] = {
                'password': password,
                'card_number': luhn(gen()),
                'balance': 0
            }
    with open("users.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
    data.update(user)
    with open("users.json", "r+", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def auth():
    username = input(str('Авторизация \nВведите ваше имя '))
    with open("users.json", encoding="utf-8") as file:
        bankbook = json.load(file)
        bankbook = dict(bankbook)
        if username in bankbook:
            password = str(input('Введите пароль от аккаунта '))
            if password == bankbook[username]['password']:
                mainmenu(username)
            else:
                print('Вы ввели неправильный пароль')
                return
        else:
            print('Аккаунт не найден в системе.')

def mainmenu(username):
    with open("users.json", encoding="utf-8") as file:
        bankbook = json.load(file)
        bankbook = dict(bankbook)
        while True:
            choice = input(f'Страница входа! Ваш баланс = {bankbook[username]["balance"]} \nВыберите действие \nПополнить - Пополнить счет, '
                           'Снять - Снять деньги, Выход - Выйти из системы ')
            match choice.lower():
                case 'пополнить':
                    balance = int(bankbook[username].get('balance'))
                    try:
                        money = int(input('Введите сумму для пополнения счета '))
                    except ValueError:
                        print('Вы ввели не число! Ошибка!')
                        continue
                    balance += money
                    bankbook[f"{username}"]["balance"] = balance
                    print(f'Вы успешно пополнили счет на {money} рублей')
                    with open('users.json', "w", encoding="utf-8") as file:
                        json.dump(bankbook, file, indent=4, ensure_ascii=False)
                case 'снять':
                    balance = int(bankbook[username].get('balance'))
                    try:
                        money = int(input('Введите сумму для пополнения счета '))
                    except ValueError:
                        print('Вы ввели не число! Ошибка!')
                        continue
                    if money > balance:
                        print('Недостаточно денег для снятия. Вы были возвращены на главную страницу')
                        break
                    else:
                        balance -= money
                        bankbook[f"{username}"]["balance"] = balance
                        print(f'Вы успешно списали сумму {money}')
                    with open('users.json', "w", encoding="utf-8") as file:
                        json.dump(bankbook, file, indent=4, ensure_ascii=False)
                case 'выход':
                    start()
                    break
def main():
    start()

if __name__ == '__main__':
    main()