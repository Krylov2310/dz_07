import os
import platform
import time


def info():
    print('\033[33mДомашнее задание 7\n'
          '"Хеш-функция"\n'
          'Студент Крылов Эдуард Васильевич\n'
          'Дата: 18.12.2025г.\033[0m')


# Очистка консоли
def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')  # From Linux


# Переход по заданиям
def any_key():
    input('\n\033[33mНажмите "Enter" для продолжения...\033[0m\n')


# 01 Класс HashTable с методом resize
class HashTable:
    print(f'1. Класс HashTable с методом resize')

    def __init__(self, size):
        self.size = size
        self.count = 0  # количество элементов
        self.table = [None] * self.size

    def _hash(self, key):
        # Простая хеш-функция для строк (сумма ASCII-кодов)
        return sum(ord(char) for char in str(key)) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        # Линейное пробирование при коллизии
        while self.table[index] is not None:
            if self.table[index][0] == key:  # ключ уже существует
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.size

        self.table[index] = (key, value)
        self.count += 1
        # Проверяем коэффициент заполнения
        if self.count > self.size * 0.7:  # 70% заполнения
            self.resize()

    def search(self, key):
        index = self._hash(key)

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]  # возвращаем значение
            index = (index + 1) % self.size
        return None

    def delete(self, key):
        index = self._hash(key)

        while True:
            current = self.table[index]

            # Проверяем, что ячейка занята и содержит кортеж
            if current is None:
                break  # Свободная ячейка — ключа нет

            if (isinstance(current, tuple)
                    and len(current) == 2
                    and current[0] == key):

                self.table[index] = None  # Удаляем элемент
                self.count -= 1

                # Перестраиваем последующие элементы
                next_index = (index + 1) % self.size
                while True:
                    next_item = self.table[next_index]
                    if next_item is None:
                        break  # Конец цепочки

                    if (isinstance(next_item, tuple)
                            and len(next_item) == 2):
                        key_to_reinsert, value_to_reinsert = next_item
                        self.table[next_index] = None
                        self.insert(key_to_reinsert, value_to_reinsert)
                    else:
                        # Невалидный элемент — прерываем перестройку
                        break
                    next_index = (next_index + 1) % self.size

                return True

            index = (index + 1) % self.size

        return False  # Ключ не найден

    def resize(self):
        old_table = self.table
        old_size = self.size

        self.size *= 2  # увеличиваем размер вдвое
        self.count = 0
        self.table = [None] * self.size

        # Перераспределяем все элементы
        for item in old_table:
            if item is not None:
                self.insert(item[0], item[1])

    def display(self):
        # Вывод содержимого таблицы
        print(f'HashTable(size = {self.size}, count = {self.count}):')
        for i, item in enumerate(self.table):
            print(f'Элементы: {i}: {item}')


# 03 Словарь на основе хеш-функции
class StringHashDict:
    def __init__(self):
        self._data = {}  # внутренний словарь для хранения данных

    def add(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Ключ должен быть строкой")

        hash_value = string_hash(key)
        self._data[key] = {
            "value": value,
            "hash": hash_value
        }

    def get(self, key):
        if key in self._data:
            return self._data[key]["value"]
        return None

    def remove(self, key):
        if key in self._data:
            del self._data[key]
            return True
        return False

    def contains(self, key):
        # Проверяет наличие ключа в словаре
        return key in self._data

    def keys(self):
        # Возвращает список всех ключей
        return list(self._data.keys())

    def values(self):
        # Возвращает список всех значений
        return [item["value"] for item in self._data.values()]

    def items(self):
        # Возвращает список пар (ключ, значение)
        return [(k, v["value"]) for k, v in self._data.items()]

    def size(self):
        # Возвращает количество элементов в словаре
        return len(self._data)


# 01
def insert_table(t):
    print('Тестирование resize:')
    print(f'\033[32mСоздаём хеш-таблицу с начальным размером: \033[0m{t}')
    ht = HashTable(t)
    ht.display()


# 02
def add_table(t):
    print(f'\033[32mДобавляем \033[0m{10} \033[32mэлементов\033[0m')
    ht = HashTable(t)
    for i in range(t):
        ht.insert(f'key{i}', f'value{i}')
    print('После добавления 10 элементов:')
    ht.display()


def string_hash(s):
    return sum(ord(char) for char in s)


# 03
def test_string_hash():
    print(f'\033[34m02 Функция для вычисления хеш-значения строки\033[0m')
    print('Тестирование')
    print(f'Хеш-значение "hello": {string_hash("hello")}')  # например, 532
    print(f'Хеш-значение "world": {string_hash("world")}')  # например, 552


# 04
def test_hash_dict():
    print(f'\033[34m03 Словарь на основе хеш-функции\033[0m')
    # Создаём словарь
    # hash_dict = StringHashDict()

    print('\033[32mДобавляем элементы\033[0m')
    print(f'("apple", 100) {hash_dict.add('apple', 100)}')
    print(f'("banana", 200) {hash_dict.add('banana', 200)}')
    print(f'("cherry", 300) {hash_dict.add('cherry', 300)}')

    print('\033[32mПоиск значений\033[0m')
    print(f'Значение "apple": {hash_dict.get('apple')}')
    print(f'Значение "grape": {hash_dict.get('grape')}')

    print('\033[32mПроверка наличия\033[0m')
    print(f'Значение "banana": {hash_dict.contains('banana')}')  # True


def print_all():
    # Вывод всех элементов
    print('\033[32mСписок всех элементов:\033[0m')
    for key, value in hash_dict.items():
        print(f'{key}: {value}')


def delete_hash(d):
    print(f'\033[32mУдаление элемента: \033[0m{d}')
    hash_dict.remove(d)
    print(f'\033[34mПосле удаления \033[0m"{d}":', hash_dict.keys())


if __name__ in '__main__':
    hash_dict = StringHashDict()
    clear_screen()
    info()
    print(f'\033[34m01 Класс HashTable с методом resize\033[0m')
    insert_table(5)
    any_key()
    add_table(10)
    any_key()
    test_string_hash()
    any_key()
    test_hash_dict()
    any_key()
    print_all()
    any_key()
    delete_hash('banana')

print('\n\033[33mДомашнее задание закончено.\033[0m')
