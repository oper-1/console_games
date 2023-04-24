# Шифр Цезаря
import sys

SYMBOLS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя 1234567890!@#$%^&*()'
MAX_KEY_SIZE = len(SYMBOLS)


def get_mode():
    # Предлагаем выбрать действие
    print('Вы хотите зашифровать(з), расшифровать(р) или взломать(в) текст?')
    print('Для выхода введите "вых"')
    while True:
        mode = input().lower()
        # Проверяем, что введена правильная команда
        if mode == 'вых':
            sys.exit()
        elif mode in ['зашифровать', 'з', 'расшифровать', 'р', 'взломать', 'в']:
            return mode
        else:
            print('Введите корректную команду (з, р или в).')


def get_message():
    # Получаем текст для шифрования или дешифрования
    print('Введите текст')
    return input()


def get_key():
    # Получаем ключ шифрования
    key = 0
    while True:
        print(f'Введите ключ шифрования (1-{MAX_KEY_SIZE})')
        key = int(input())

        if 1 <= key <= MAX_KEY_SIZE:
            return key


def get_translated_message(mode, message, key):
    if mode.startswith('р'):
        key = -key

    translated = ''

    for symbol in message:
        symbol_index = SYMBOLS.find(symbol)
        if symbol_index == -1: # Символ не найден в SYMBOLS
            # Просто добавить этот символ без изменений
            translated += symbol
        else:
            # Зашифровать или расшифровать
            symbol_index += key

            if symbol_index >= len(SYMBOLS):
                symbol_index -= len(SYMBOLS)
            elif symbol_index < 0:
                symbol_index += len(SYMBOLS)

            translated += SYMBOLS[symbol_index]

    return translated


while True:
    mode = get_mode()
    message = get_message()

    if not mode.startswith('в'):
        key = get_key()

    print('Преобразованный текст:')
    if not mode.startswith('в'):
        print(get_translated_message(mode, message, key))
    else:
        for key in range(1, MAX_KEY_SIZE + 1):
            print(key, get_translated_message('р', message, key))































